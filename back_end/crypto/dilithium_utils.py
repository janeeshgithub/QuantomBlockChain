import oqs

# Define the signature algorithm to use
SIG_ALGORITHM = "Dilithium2"

def generate_keys():
    """Generates a new CRYSTALS-Dilithium key pair."""
    with oqs.Signature(SIG_ALGORITHM) as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
        return public_key, secret_key

def sign(secret_key: bytes, message: bytes) -> bytes:
    """Signs a message using a Dilithium secret key."""
    # This function now correctly accepts bytes and performs no JSON conversion
    with oqs.Signature(SIG_ALGORITHM, secret_key) as signer:
        signature = signer.sign(message)
        return signature

def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    """Verifies a signature against a message and a public key."""
    try:
        with oqs.Signature(SIG_ALGORITHM) as verifier:
            return verifier.verify(message, signature, public_key)
    except oqs.Error:
        return False