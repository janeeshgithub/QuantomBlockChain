# crypto/dilithium_utils.py

import oqs
import json

# Define the signature algorithm to use.
# Other options: 'Dilithium3', 'Dilithium5'
SIG_ALGORITHM = "Dilithium2"

def generate_keys():
    """
    Generates a new CRYSTALS-Dilithium key pair.
    
    Returns:
        tuple: A tuple containing the public key (bytes) and secret key (bytes).
    """
    # Create an instance of the signature mechanism
    with oqs.Signature(SIG_ALGORITHM) as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
        print(public_key, secret_key)
        return public_key, secret_key

def sign_data(secret_key: bytes, data: dict) -> bytes:
    """
    Signs a data payload using a Dilithium secret key.

    Args:
        secret_key (bytes): The private signing key.
        data (dict): The Python dictionary to be signed.

    Returns:
        bytes: The resulting signature.
    """
    # Convert dict to a consistent JSON string to ensure a deterministic hash
    message = json.dumps(data, sort_keys=True).encode('utf-8')
    
    # Create an instance of the signature mechanism to sign
    with oqs.Signature(SIG_ALGORITHM, secret_key) as signer:
        signature = signer.sign(message)
        return signature

def verify_signature(public_key: bytes, data: dict, signature: bytes) -> bool:
    """
    Verifies a signature against the data and a public key.

    Args:
        public_key (bytes): The public key for verification.
        data (dict): The original data payload (as a dictionary).
        signature (bytes): The signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    try:
        message = json.dumps(data, sort_keys=True).encode('utf-8')
        
        # Create an instance of the signature mechanism to verify
        with oqs.Signature(SIG_ALGORITHM) as verifier:
            # The verify method returns True on success, raises OQS.Error on failure
            is_valid = verifier.verify(message, signature, public_key)
            return is_valid
    except oqs.Error:
        # liboqs raises an OQS.Error on verification failure
        return False