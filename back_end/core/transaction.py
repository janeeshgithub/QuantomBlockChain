# core/transaction.py

import time
from crypto import kyber_utils
from core.wallet import Wallet

class Transaction:
    # Note the 'username: str = None' argument has been added here
    def __init__(self, sender_wallet: Wallet, message: str, recipient_public_keys_hex: dict = None, tx_type: str = "message", username: str = None):
        """
        Creates a new transaction. Can be a 'message' or 'key_registration'.
        """
        self.sender_address = sender_wallet.address
        self.timestamp = time.time()
        self.tx_type = tx_type
        self.username = username # Store username at the top level

        if self.tx_type == "message":
            if not recipient_public_keys_hex:
                raise ValueError("Recipient keys required for a message.")
            self.recipient_address = recipient_public_keys_hex['address']
            recipient_enc_pub_key = bytes.fromhex(recipient_public_keys_hex['encryption_key'])
            ciphertext, shared_secret = kyber_utils.encapsulate_key(recipient_enc_pub_key)
            nonce, payload = kyber_utils.encrypt_message(shared_secret, message)
            self.content = {"ciphertext": ciphertext.hex(), "nonce": nonce.hex(), "payload": payload.hex()}
        
        elif self.tx_type == "key_registration":
            if not self.username:
                raise ValueError("Username is required for key registration.")
            self.recipient_address = None
            self.content = {
                "message": f"Registering username '{self.username}'",
                "encryption_key": sender_wallet.encryption_public_key.hex()
            }

    def to_dict(self) -> dict:
        """Returns the transaction data as a dictionary for signing."""
        tx_dict = {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "timestamp": self.timestamp,
            "tx_type": self.tx_type,
            "content": self.content
        }
        # Only add username to the signed data if it's a key registration
        if self.tx_type == "key_registration":
            tx_dict['username'] = self.username
        
        return tx_dict