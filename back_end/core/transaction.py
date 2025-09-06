# core/transaction.py

import time
from crypto import kyber_utils
from core.wallet import Wallet

class Transaction:
    def __init__(self, sender_wallet: Wallet, recipient_public_keys_hex: dict, message: str):
        """
        Creates a new transaction containing an encrypted message.

        Args:
            sender_wallet (Wallet): The wallet object of the sender.
            recipient_public_keys_hex (dict): A dict of the recipient's hex-encoded public keys.
            message (str): The plaintext message to be encrypted and sent.
        """
        self.sender_address = sender_wallet.address
        self.recipient_address = recipient_public_keys_hex['address']
        self.timestamp = time.time()
        
        # --- Encryption Process ---
        # 1. Get recipient's public encryption key from hex
        recipient_enc_pub_key = bytes.fromhex(recipient_public_keys_hex['encryption_key'])
        
        # 2. Encapsulate a secret for the recipient
        ciphertext, shared_secret = kyber_utils.encapsulate_key(recipient_enc_pub_key)
        
        # 3. Encrypt the message with the shared secret
        nonce, payload = kyber_utils.encrypt_message(shared_secret, message)

        # 4. Store the encrypted parts in the transaction
        self.encrypted_content = {
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "payload": payload.hex()
        }

    def to_dict(self) -> dict:
        """Returns the transaction data as a dictionary (for signing)."""
        return {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "timestamp": self.timestamp,
            "encrypted_content": self.encrypted_content
        }