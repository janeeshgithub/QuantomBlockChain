# client.py

# This script simulates a user creating and signing a transaction.
# We will copy its output to use in Postman.

from core.wallet import Wallet
from core.transaction import Transaction
from crypto import dilithium_utils
import json

def generate_postman_payload():
    print("--- Generating Transaction Payload for Postman ---")
    
    # 1. Simulate Alice and Bob
    alice = Wallet()
    bob = Wallet()

    print(f"Alice's Address: {alice.address[:10]}...")
    print(f"Bob's Address:   {bob.address[:10]}...")
    
    # 2. Create an encrypted transaction
    message = "Quantum network is live. Awaiting your signal."
    tx = Transaction(
        sender_wallet=alice,
        recipient_public_keys_hex=bob.get_public_keys_hex(),
        message=message
    )
    
    # 3. Sign the transaction
    tx_dict = tx.to_dict()
    signature = dilithium_utils.sign_data(alice.signing_secret_key, tx_dict)
    
    # 4. Prepare the final payload for the API
    api_payload = {
        "transaction_dict": tx_dict,
        "signature_hex": signature.hex()
    }
    
    print("\n✅ Payload ready. Copy the JSON below and paste it into the Postman body:\n")
    # Print the JSON payload in a nicely formatted way
    print(json.dumps(api_payload, indent=4))

if __name__ == "__main__":
    generate_postman_payload()