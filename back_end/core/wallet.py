from crypto import dilithium_utils, kyber_utils

class Wallet:
    def __init__(self):
        """
        Initializes a new wallet by generating two sets of quantum-resistant key pairs.
        """
        # Generate keys for digital signatures (identity)
        self.signing_public_key, self.signing_secret_key = dilithium_utils.generate_keys()
        
        # Generate keys for message encryption
        self.encryption_public_key, self.encryption_secret_key = kyber_utils.generate_keys()

    @property
    def address(self) -> str:
        """
        Returns the wallet's public address (the public signing key).
        We use hex format for readability.
        """
        return self.signing_public_key.hex()

    def get_public_keys_hex(self) -> dict:
        """Returns a dictionary of the public keys in hex format."""
        return {
            "address": self.address,
            "encryption_key": self.encryption_public_key.hex()
        }