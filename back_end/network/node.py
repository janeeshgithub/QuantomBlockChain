# network/node.py

import asyncio
import json
import uuid
import logging
import argparse
import sys
import os
import time
from datetime import datetime

# --- Add project root to the path for imports ---
# This allows the script to find the 'core', 'consensus', and 'crypto' folders
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..')
sys.path.append(parent_dir)

# --- Your Core Blockchain Imports ---
from core.block import Block
from core.blockchain import Blockchain
from core.wallet import Wallet
from core.public_ledger import PublicKeyLedger
from consensus.dpol import DPoLConsensus
from core.transaction import Transaction

# --- Basic Logging Setup ---
# Configures a logger to print timestamped informational messages to the console.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# In network/node.py

# In network/node.py

class P2PNode:
    """
    Manages all peer-to-peer network operations for a single blockchain node.
    """
    def __init__(self, host: str, port: int, node_wallet: Wallet, blockchain: Blockchain, consensus: DPoLConsensus, ledger: PublicKeyLedger):
        self.host = host
        self.port = port
        self.node_wallet = node_wallet
        self.blockchain = blockchain
        self.consensus = consensus
        self.ledger = ledger
        
        # --- UPDATED: The dictionary now maps peer_addr -> (reader, writer, address_string) ---
        self.peers = {}
        
        self.server = None
        self.seen_messages = set()

    def create_message(self, msg_type: str, payload: dict = None) -> dict:
        return {"id": str(uuid.uuid4()), "type": msg_type, "payload": payload or {}}

    async def start(self):
        try:
            self.server = await asyncio.start_server(self.handle_connection, self.host, self.port)
            logging.info(f"Node listening on {self.host}:{self.port}")
            logging.info(f"Node address: {self.node_wallet.address}")
            await self.server.serve_forever()
        except Exception as e:
            logging.error(f"Error starting node: {e}")
        finally:
            await self.stop()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for addr, (reader, writer, _) in self.peers.items():
            writer.close()
            await writer.wait_closed()
        self.peers.clear()

    async def connect_to_peer(self, peer_host: str, peer_port: int):
        try:
            reader, writer = await asyncio.open_connection(peer_host, peer_port)
            peer_addr = writer.get_extra_info('peername')
            self.peers[peer_addr] = (reader, writer, None)
            logging.info(f"Successfully connected to peer {peer_addr}")
            handshake_msg = self.create_message("HANDSHAKE", {"address": self.node_wallet.address})
            await self.send_message(writer, handshake_msg)
            get_chain_msg = self.create_message("GET_CHAIN")
            await self.send_message(writer, get_chain_msg)
            asyncio.create_task(self.handle_connection(reader, writer))
        except Exception as e:
            logging.error(f"Failed to connect to {peer_host}:{peer_port}: {e}")

    # --- UPDATED: This now works with address strings ---
    def update_consensus_nodes(self):
        """Updates the consensus algorithm with the current list of known peer addresses."""
        peer_addresses = [addr_str for _, _, addr_str in self.peers.values() if addr_str]
        all_addresses = peer_addresses + [self.node_wallet.address]
        self.consensus.all_nodes = list(set(all_addresses)) # Ensure uniqueness
        logging.info(f"Consensus nodes updated. Total unique nodes: {len(self.consensus.all_nodes)}")

    async def handle_connection(self, reader, writer):
        peer_addr = writer.get_extra_info('peername')
        try:
            self.peers[peer_addr] = (reader, writer, None) 
            
            logging.info(f"Accepted connection from {peer_addr}")

            while True:
                len_data = await reader.readexactly(4)
                msg_len = int.from_bytes(len_data, 'big')
                msg_data = await reader.readexactly(msg_len)
                message = json.loads(msg_data.decode())
                await self.handle_message(message, writer)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            logging.warning(f"Peer {peer_addr} disconnected.")
        finally:
            if peer_addr in self.peers:
                del self.peers[peer_addr]
            self.update_consensus_nodes()
            writer.close()
            await writer.wait_closed()

    # --- UPDATED: The HANDSHAKE handler is now much simpler and more robust ---
    async def handle_message(self, message: dict, writer):
        msg_type = message.get("type")
        originator_addr = writer.get_extra_info('peername')
        
        # Prevent infinite broadcast loops for most messages
        if msg_type not in ["GET_CHAIN", "CHAIN_RESPONSE"]:
            if message.get("id") in self.seen_messages:
                return
            self.seen_messages.add(message.get("id"))

        logging.info(f"Received '{msg_type}' from {originator_addr}")

        if msg_type == "GET_CHAIN":
            chain_data = [block.__dict__ for block in self.blockchain.chain]
            response = self.create_message("CHAIN_RESPONSE", {"chain": chain_data})
            await self.send_message(writer, response)
        
        elif msg_type == "CHAIN_RESPONSE":
            chain_data = message.get("payload", {}).get("chain", [])
            if self.blockchain.replace_chain(chain_data):
                self.ledger.update_from_chain(self.blockchain)
        
        elif msg_type == "HANDSHAKE":
            peer_wallet_address_hex = message.get("payload", {}).get("address")
            if peer_wallet_address_hex:
                # We just store the peer's address string, not a full Wallet object.
                if originator_addr in self.peers:
                    reader, writer, _ = self.peers[originator_addr]
                    self.peers[originator_addr] = (reader, writer, peer_wallet_address_hex)
                logging.info(f"Handshake complete. Peer {originator_addr} address loaded.")
                self.update_consensus_nodes()
        
        elif msg_type == "NEW_TRANSACTION":
            if self.blockchain.add_transaction(message['payload']['transaction_dict'], message['payload']['signature_hex']):
                await self.broadcast(message, originator_writer=writer)

        elif msg_type == "NEW_BLOCK":
            block_data = message.get("payload")
            new_block = Block.from_dict(block_data)
            if new_block.index == self.blockchain.last_block.index + 1 and new_block.previous_hash == self.blockchain.last_block.hash:
                self.blockchain.chain.append(new_block)
                self.blockchain.pending_transactions = []
                logging.info(f"✅ Appended new block #{new_block.index} from peer.")
                self.ledger.update_from_chain(self.blockchain)
                self.scan_block_for_messages(new_block)
                await self.broadcast(message, originator_writer=writer)
            elif new_block.index > self.blockchain.last_block.index:
                logging.warning(f"Received block ahead of us. Requesting chain sync from {originator_addr}.")
                get_chain_msg = self.create_message("GET_CHAIN")
                await self.send_message(writer, get_chain_msg)
            else:
                logging.info(f"Ignoring old or irrelevant block #{new_block.index}.")

    def scan_block_for_messages(self, block: Block):
        my_address = self.node_wallet.address
        for signed_tx in block.transactions:
            tx = signed_tx['transaction_dict']
            if tx.get('tx_type') == 'message' and tx.get('recipient_address') == my_address:
                logging.info("!!! You have a new message in this block !!!")
                encrypted_content = tx.get('content')
                decrypted_message = self.node_wallet.decrypt_message(encrypted_content)
                if decrypted_message:
                    sender_address = tx.get('sender_address')
                    sender_name = self.ledger.get_user_for_address(sender_address) or f"{sender_address[:10]}..."
                    print(f"\n[NEW MESSAGE] From: {sender_name}")
                    print(f" > '{decrypted_message}'\n")
                else:
                    print("Found a message for you, but FAILED to decrypt.")

    async def send_message(self, writer, message):
        try:
            msg_bytes = json.dumps(message, default=str).encode()
            len_bytes = len(msg_bytes).to_bytes(4, 'big')
            writer.write(len_bytes + msg_bytes)
            await writer.drain()
        except ConnectionResetError:
            pass

    async def broadcast(self, message: dict, originator_writer=None):
        all_writers = [w for _, w, _ in self.peers.values() if w is not originator_writer]
        for writer in all_writers:
            await self.send_message(writer, message)


async def main(args):
    # (The setup part of this function remains the same)
    node_wallet = Wallet()
    blockchain = Blockchain()
    consensus = DPoLConsensus(nodes=[], num_delegates=5)
    ledger = PublicKeyLedger()
    ledger.update_from_chain(blockchain)

    node = P2PNode(args.host, args.port, node_wallet, blockchain, consensus, ledger)
    
    server_task = asyncio.create_task(node.start())
    await asyncio.sleep(1)

    if args.peers:
        for peer in args.peers.split(','):
            await node.connect_to_peer(peer.split(':')[0], int(peer.split(':')[1]))

    while True:
        try:
            cmd = await asyncio.to_thread(input, "\nCommands: users, register_key <user>, send_msg <user> <msg>, read_msgs, mempool, mine, chain, exit\n> ")
            
            # --- START OF CORRECTED BLOCK ---
            if cmd == 'read_msgs':
                print("\n--- Manually checking blockchain for your messages ---")
                my_address = node.node_wallet.address
                messages_found = 0
                
                # Iterate through every block in the chain
                for block in node.blockchain.chain:
                    # Iterate through every transaction in the block
                    for signed_tx in block.transactions:
                        tx = signed_tx['transaction_dict']
                        
                        # Check if the transaction is a 'message' and if it's addressed to us
                        if tx.get('tx_type') == 'message' and tx.get('recipient_address') == my_address:
                            encrypted_content = tx.get('content')
                            
                            # Use our wallet to try and decrypt the content
                            decrypted_message = node.node_wallet.decrypt_message(encrypted_content)
                            
                            if decrypted_message:
                                messages_found += 1
                                sender_address = tx.get('sender_address')
                                sender_name = ledger.get_user_for_address(sender_address) or f"{sender_address[:10]}..."
                                time_formatted = datetime.fromtimestamp(tx.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')

                                print(f"\nMessage #{messages_found}:")
                                print(f"  From:      {sender_name}")
                                print(f"  At:        {time_formatted}")
                                print(f"  Message:   '{decrypted_message}'")
                            else:
                                print(f"Found a message from {tx.get('sender_address')[:12]} but FAILED to decrypt.")
                
                # After checking all blocks, if we haven't found any messages, say so.
                if messages_found == 0:
                    print("No messages found for you on the blockchain.")
            # --- END OF CORRECTED BLOCK ---

            elif cmd == 'users':
                print(f"Registered Users: {ledger.list_users()}")

            elif cmd.startswith('register_key'):
                parts = cmd.split()
                if len(parts) < 2: print("Usage: register_key <username>"); continue
                username = parts[1]
                tx_obj = Transaction(sender_wallet=node.node_wallet, tx_type="key_registration", username=username, message="")
                tx_dict = tx_obj.to_dict()
                signature = node.node_wallet.sign_transaction(tx_dict)
                payload = {'transaction_dict': tx_dict, 'signature_hex': signature.hex()}
                if node.blockchain.add_transaction(tx_dict, signature.hex()):
                    tx_message = node.create_message("NEW_TRANSACTION", payload)
                    await node.broadcast(tx_message)

            elif cmd.startswith('send_msg'):
                parts = cmd.split()
                if len(parts) < 3: print("Usage: send_msg <username> <message>"); continue
                recipient_name, message_text = parts[1], " ".join(parts[2:])
                recipient_keys = ledger.get_keys_for_user(recipient_name)
                if not recipient_keys: print(f"Could not find user '{recipient_name}'."); continue
                print(f"Found user '{recipient_name}'. Creating encrypted message...")
                tx_obj = Transaction(sender_wallet=node.node_wallet, message=message_text, recipient_public_keys_hex=recipient_keys)
                tx_dict = tx_obj.to_dict()
                signature = node.node_wallet.sign_transaction(tx_dict)
                payload = {'transaction_dict': tx_dict, 'signature_hex': signature.hex()}
                if node.blockchain.add_transaction(tx_dict, signature.hex()):
                    tx_message = node.create_message("NEW_TRANSACTION", payload)
                    await node.broadcast(tx_message)
            
            elif cmd == 'mempool':
                print(f"Pending transactions: {len(node.blockchain.pending_transactions)}")
                print(json.dumps(node.blockchain.pending_transactions, indent=2))

            elif cmd == 'mine':
                if not node.blockchain.pending_transactions: logging.info('No pending transactions to create a block.'); continue
                logging.info("--- (TESTING) Bypassing DPoL, this node is the automatic winner. ---")
                new_block = node.blockchain.mine_block(proposer_address=node.node_wallet.address)
                if new_block:
                    block_message = node.create_message("NEW_BLOCK", new_block.__dict__)
                    await node.broadcast(block_message)
                    ledger.update_from_chain(node.blockchain)

            elif cmd == 'chain':
                print(json.dumps([b.__dict__ for b in node.blockchain.chain], indent=2, default=str))
            elif cmd == 'exit':
                break
        except (EOFError, KeyboardInterrupt):
            break

    server_task.cancel()
    await node.stop()

# This is the entry point when you run "python network/node.py ..."
if __name__ == "__main__":
    # Set up command-line argument parsing.
    parser = argparse.ArgumentParser(description="Run a P2P blockchain node.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help="The host address to listen on.")
    parser.add_argument('--port', type=int, required=True, help="The port to listen on.")
    parser.add_argument('--peers', type=str, help="A comma-separated list of initial peers to connect to (e.g., localhost:8001,localhost:8002).")
    args = parser.parse_args()
    
    try:
        # Start the asyncio event loop.
        asyncio.run(main(args))
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user.")