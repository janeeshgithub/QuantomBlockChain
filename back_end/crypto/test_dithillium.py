from dilithium_utils import generate_keys, sign_data, verify_signature

def run_test():
    """
    Executes a full cycle test of the Dilithium utility functions.
    """
    print("--- 1. Testing Key Generation ---")
    try:
        public_key, secret_key = generate_keys()
        print(" Success: Key pair generated.")
        # Optional: print key lengths to see they're not empty
        print(f"   - Public Key Length: {len(public_key)} bytes")
        print(f"   - Secret Key Length: {len(secret_key)} bytes\n")
    except Exception as e:
        print(f" Failure: Key generation failed. Error: {e}")
        return

    print("--- 2. Testing Data Signing ---")
    # Create some sample data, like a simple transaction
    sample_data = {
        "from": "Alice",
        "to": "Bob",
        "amount": 10,
        "message": "Here are the funds!"
    }
    try:
        signature = sign_data(secret_key, sample_data)
        print("Success: Data signed.")
        print(f"   - Signature Length: {len(signature)} bytes\n")
    except Exception as e:
        print(f"Failure: Signing failed. Error: {e}")
        return

    print("--- 3. Testing Signature Verification (Success Case) ---")
    # Verify the signature with the correct data
    is_valid = verify_signature(public_key, sample_data, signature)
    if is_valid:
        print("Success: Signature verified correctly as VALID.\n")
    else:
        print("Failure: Signature was incorrectly marked as INVALID.\n")

    print("--- 4. Testing Signature Verification (Failure Case) ---")
    # Create tampered data to simulate an attack
    tampered_data = {
        "from": "Alice",
        "to": "Mallory",  # Changed the recipient
        "amount": 1000,   # Changed the amount
        "message": "Here are the funds!"
    }
    is_tampered_valid = verify_signature(public_key, tampered_data, signature)
    if not is_tampered_valid:
        print("Success: Signature on tampered data correctly identified as INVALID.\n")
    else:
        print("Failure: Signature on tampered data was incorrectly marked as VALID.\n")

# This block ensures the test runs when the script is executed directly
if __name__ == "__main__":
    run_test()