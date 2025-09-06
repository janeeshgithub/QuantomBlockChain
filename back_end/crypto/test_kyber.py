# test_kyber.py

from kyber_utils import (
    generate_keys,
    encapsulate_key,
    decapsulate_key,
    encrypt_message,
    decrypt_message
)

def run_kyber_test():
    """
    Simulates a full end-to-end encrypted communication using Kyber and AES.
    """
    print("--- 1. Recipient: Generating Kyber Key Pair 🔑 ---")
    try:
        # The recipient generates their key pair and shares the public key.
        recipient_public_key, recipient_secret_key = generate_keys()
        print("✅ Success: Key pair generated.")

        # --- ADDED LINES TO PRINT KEYS ---
        print(f"   - Public Key (hex): {recipient_public_key.hex()}")
        print(f"   - Secret Key (hex): {recipient_secret_key.hex()}\n")
        # ------------------------------------

    except Exception as e:
        print(f"❌ Failure: Key generation failed. Error: {e}")
        return

    # --- SENDER'S ACTIONS ---
    print("--- 2. Sender: Encrypting a Message 🔒 ---")
    try:
        ciphertext, shared_secret_sender = encapsulate_key(recipient_public_key)
        print("   - Shared secret encapsulated successfully.")
        message_to_send = "This is a secret message for the blockchain!"
        nonce, encrypted_payload = encrypt_message(shared_secret_sender, message_to_send)
        print(f"   - Original Message: '{message_to_send}'")
        print("✅ Success: Message encrypted with AES-GCM.\n")
    except Exception as e:
        print(f"❌ Failure: Encryption process failed. Error: {e}")
        return

    # --- RECIPIENT'S ACTIONS ---
    print("--- 3. Recipient: Decrypting the Message 🔓 ---")
    try:
        shared_secret_recipient = decapsulate_key(recipient_secret_key, ciphertext)
        print("   - Shared secret decapsulated successfully.")
        decrypted_message = decrypt_message(shared_secret_recipient, nonce, encrypted_payload)
        print(f"   - Decrypted Message: '{decrypted_message}'")
        print("✅ Success: Message decrypted with AES-GCM.\n")
    except Exception as e:
        print(f"❌ Failure: Decryption process failed. Error: {e}")
        return

    # --- FINAL VERIFICATION ---
    print("--- 4. Final Verification ---")
    if message_to_send == decrypted_message:
        print("✅ SUCCESS: The original and decrypted messages match!")
    else:
        print("❌ FAILURE: The messages DO NOT match.")

if __name__ == "__main__":
    run_kyber_test()