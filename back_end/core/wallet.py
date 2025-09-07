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