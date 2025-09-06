import os
import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Define the Key Encapsulation Mechanism (KEM) to use.
KEM_ALGORITHM = "Kyber512"

def generate_keys():
    """
    Generates a new CRYSTALS-Kyber key pair.

    Returns:
        tuple: A tuple containing the public key (bytes) and secret key (bytes).
    """
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
        return public_key, secret_key

def encapsulate_key(public_key: bytes) -> tuple[bytes, bytes]:
    """
    Generates a shared secret and a ciphertext for a recipient's public key.
    This is called by the SENDER.

    Args:
        public_key (bytes): The recipient's public Kyber key.

    Returns:
        tuple: A tuple containing the ciphertext (bytes) and the shared secret (bytes).
    """
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as kem:
        ciphertext, shared_secret = kem.encap_secret(public_key)
        return ciphertext, shared_secret

def decapsulate_key(secret_key: bytes, ciphertext: bytes) -> bytes:
    """
    Derives the shared secret from a ciphertext using the recipient's secret key.
    This is called by the RECIPIENT.

    Args:
        secret_key (bytes): The recipient's private Kyber key.
        ciphertext (bytes): The ciphertext received from the sender.

    Returns:
        bytes: The derived shared secret.
    """
    with oqs.KeyEncapsulation(KEM_ALGORITHM, secret_key) as kem:
        shared_secret = kem.decap_secret(ciphertext)
        return shared_secret

def encrypt_message(shared_secret: bytes, message: str) -> tuple[bytes, bytes]:
    """
    Encrypts a message using AES-GCM with the derived shared secret.
    (This function remains unchanged as it uses the 'cryptography' library).

    Args:
        shared_secret (bytes): The key for the symmetric cipher.
        message (str): The plaintext message to encrypt.

    Returns:
        tuple: A tuple containing the nonce (bytes) and the encrypted message (bytes).
    """
    aesgcm = AESGCM(shared_secret)
    nonce = os.urandom(12)  # GCM standard nonce size is 12 bytes
    message_bytes = message.encode('utf-8')
    encrypted_payload = aesgcm.encrypt(nonce, message_bytes, None)
    return nonce, encrypted_payload

def decrypt_message(shared_secret: bytes, nonce: bytes, encrypted_payload: bytes) -> str:
    """
    Decrypts a message using AES-GCM with the derived shared secret.
    (This function also remains unchanged).

    Args:
        shared_secret (bytes): The key for the symmetric cipher.
        nonce (bytes): The nonce used during encryption.
        encrypted_payload (bytes): The encrypted message content.

    Returns:
        str: The decrypted plaintext message.
    """
    aesgcm = AESGCM(shared_secret)
    decrypted_bytes = aesgcm.decrypt(nonce, encrypted_payload, None)
    return decrypted_bytes.decode('utf-8')