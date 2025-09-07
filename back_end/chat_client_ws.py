# chat_client_ws.py

import asyncio
import websockets
import json
import threading
import sys

# --- Project Imports ---
from core.wallet import Wallet
from core.transaction import Transaction
from crypto import dilithium_utils, kyber_utils

# --- Client Setup ---
client_wallet = Wallet()
NODE_URL = "" # Set via command line argument

async def listen_for_messages(websocket):
    """Listens for incoming messages from the server and prints them."""
    async for message in websocket:
        data = json.loads(message)
        
        if data['type'] == 'info':
            print(f"\n[Node Info]: {data['message']}")
        
        elif data['type'] == 'new_block':
            block = data['block']
            print(f"\n[Network]: New Block #{block['index']} has been mined!")
            
            # Check for messages addressed to us
            for signed_tx in block['transactions']:
                tx_data = signed_tx['data']
                if tx_data.get('tx_type') == 'message' and tx_data.get('recipient_address') == client_wallet.address:
                    print("\n--- 📥 New Message Received! ---")
                    try:
                        content = tx_data['content']
                        ciphertext = bytes.fromhex(content['ciphertext'])
                        nonce = bytes.fromhex(content['nonce'])
                        payload = bytes.fromhex(content['payload'])
                        shared_secret = kyber_utils.decapsulate_key(client_wallet.encryption_secret_key, ciphertext)
                        decrypted_message = kyber_utils.decrypt_message(shared_secret, nonce, payload)
                        print(f"From: {tx_data['sender_address'][:12]}...")
                        print(f"Message: {decrypted_message}")
                    except Exception as e:
                        print(f"Could not decrypt message: {e}")
                    finally:
                        print("---------------------------------")


async def user_interface(websocket):
    """Handles user input for sending messages and other actions."""
    loop = asyncio.get_event_loop()
    while True:
        # Run the blocking input() in a separate thread to not block the event loop
        command = await loop.run_in_executor(None, input, "\nChoose an action:\n1. Register Key\n2. Send Message\n> ")
        
        if command == '1':
            print("\nRegistering your public key on the network...")
            tx = Transaction(sender_wallet=client_wallet, message="", tx_type="key_registration")
            tx_dict = tx.to_dict()
            signature = dilithium_utils.sign_data(client_wallet.signing_secret_key, tx_dict)
            payload = {
                "type": "new_transaction",
                "transaction_dict": tx_dict,
                "signature_hex": signature.hex()
            }
            await websocket.send(json.dumps(payload))
            print("Key registration sent. Awaiting next block to be mined.")

        elif command == '2':
            # This part is simplified - in a real app you'd get the key from the chain
            # For this simulation, we'll ask for it.
            recipient_address = await loop.run_in_executor(None, input, "Enter recipient's Address: ")
            recipient_enc_key = await loop.run_in_executor(None, input, "Enter recipient's Encryption Key: ")
            message = await loop.run_in_executor(None, input, "Enter your message: ")

            recipient_public_keys = {"address": recipient_address, "encryption_key": recipient_enc_key}
            
            tx = Transaction(sender_wallet=client_wallet, message=message, recipient_public_keys_hex=recipient_public_keys)
            tx_dict = tx.to_dict()
            signature = dilithium_utils.sign_data(client_wallet.signing_secret_key, tx_dict)
            payload = {
                "type": "new_transaction",
                "transaction_dict": tx_dict,
                "signature_hex": signature.hex()
            }
            await websocket.send(json.dumps(payload))
            print("Message sent. Awaiting next block to be mined.")

async def main():
    uri = f"ws://{NODE_URL}/ws"
    async with websockets.connect(uri) as websocket:
        print("--- Quantum Messenger Client ---")
        print(f"Your Address: {client_wallet.address}")
        print(f"Your Encryption Key: {client_wallet.encryption_public_key.hex()}")
        
        # Run listener and UI concurrently
        listener_task = asyncio.create_task(listen_for_messages(websocket))
        ui_task = asyncio.create_task(user_interface(websocket))
        
        await asyncio.gather(listener_task, ui_task)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chat_client_ws.py <host:port>")
        sys.exit(1)
    NODE_URL = sys.argv[1]
    asyncio.run(main())