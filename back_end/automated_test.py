import requests
import time
import json
from core.wallet import Wallet

def create_signed_transaction(wallet, recipient_address, content):
    """Creates and signs a simple message transaction."""
    tx_data = {
        'sender_address': wallet.address,
        'recipient_address': recipient_address,
        'tx_type': 'message',
        'content': content,
        'timestamp': time.time()
    }
    signature = wallet.sign_transaction(tx_data)
    return {
        'transaction_dict': tx_data,
        'signature_hex': signature.hex()
    }

if __name__ == '__main__':
    client_wallet = Wallet()
    recipient = Wallet().address

    print(f"Client Wallet Address: {client_wallet.address}")

    signed_tx = create_signed_transaction(
        client_wallet,
        recipient,
        "Hello, Blockchain!"
    )

    node_url = "http://127.0.0.1:5001/transactions/new"
    print(f"Submitting transaction to: {node_url}")

    try:
        response = requests.post(node_url, json=signed_tx)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: Could not connect to the node.")
        print(f"Please ensure your blockchain network is running before executing this script.")
        print(f"Details: {e}")