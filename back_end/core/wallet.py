import json
from crypto import dilithium_utils, kyber_utils

class Wallet:
    def __init__(self):
        """Initializes a new wallet by generating quantum-resistant key pairs."""
        self.signing_public_key, self.signing_secret_key = dilithium_utils.generate_keys()
        self.encryption_public_key, self.encryption_secret_key = kyber_utils.generate_keys()

    @property
    def address(self) -> str:
        """Returns the wallet's public address (the public signing key)."""
        return self.signing_public_key.hex()

    def get_public_keys_hex(self) -> dict:
        """Returns a dictionary of the public keys in hex format."""
        return {
            "address": self.address,
            "encryption_key": self.encryption_public_key.hex()
        }

    def sign_transaction(self, transaction_data: dict) -> bytes:
        """Generates a digital signature for a transaction using Dilithium."""
        # 1. Create a consistent, ordered string from the dictionary
        ordered_tx_string = json.dumps(transaction_data, sort_keys=True)
        
        # 2. Convert the string to bytes
        tx_bytes = ordered_tx_string.encode('utf-8')
        
        # 3. Sign the bytes using the corrected utility function
        signature = dilithium_utils.sign(self.signing_secret_key, tx_bytes)
        
        return signature
    
    def decrypt_message(self, encrypted_content: dict) -> str | None:
        """
        Decrypts a message using the wallet's Kyber secret key.

        Args:
            encrypted_content (dict): A dictionary containing 'ciphertext','nonce', and 'payload' as hex strings.

        Returns:
            str: The decrypted message, or None if decryption fails.
        """
        try:
            # 1. Convert the hex strings from the transaction back into bytes
            ciphertext_bytes = bytes.fromhex(encrypted_content['ciphertext'])
            nonce_bytes = bytes.fromhex(encrypted_content['nonce'])
            payload_bytes = bytes.fromhex(encrypted_content['payload'])

            # 2. Use our secret key to "decapsulate" the ciphertext and get the shared secret
            shared_secret = kyber_utils.decapsulate_key(self.encryption_secret_key, ciphertext_bytes)

            # 3. Use the shared secret to decrypt the main payload
            decrypted_message_bytes = kyber_utils.decrypt_message(shared_secret, nonce_bytes, payload_bytes)
            
            # 4. Decode the decrypted bytes back into a human-readable string
            return decrypted_message_bytes

        except (KeyError, ValueError, Exception) as e:
            # Catch errors from missing keys, bad hex, or a failed decryption
            print(f"Decryption failed: {e}")
            return None