import asyncio
import json
import uuid
import logging
import argparse
import sys
import os
import random
import time

# --- Add project root to the path for imports ---
script_dir = os.path.dirname(__file__)

parent_dir = os.path.join(script_dir, '..')

sys.path.append(parent_dir)

# --- Your Core Blockchain Imports ---
from core.block import Block
from core.blockchain import Blockchain
from core.wallet import Wallet
from consensus.dpol import DPoLConsensus
from core.transaction import Transaction


# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class P2PNode:
    def __init__(self, host, port, node_wallet, blockchain, consensus):
        self.host = host
        self.port = port
        self.node_wallet = node_wallet
        self.blockchain = blockchain
        self.consensus = consensus
        
        # Peers dict now stores: peer_addr -> (reader, writer, peer_wallet_address)
        self.peers = {}  
        self.server = None
        self.seen_messages = set()

    def create_message(self, msg_type, payload=None):
        """Helper to create a standardized message dictionary."""
        return {
            "id": str(uuid.uuid4()),
            "type": msg_type,
            "payload": payload or {}
        }

    async def start(self):
        """Starts the node's server and main loop."""
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, self.host, self.port
            )
            logging.info(f"Node listening on {self.host}:{self.port}")
            logging.info(f"Node address: {self.node_wallet.address}")
            await self.server.serve_forever()
        except Exception as e:
            logging.error(f"Error starting node: {e}")
        finally:
            await self.stop()

    async def stop(self):
        """Gracefully stops the node."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for addr, (reader, writer, _) in self.peers.items():
            writer.close()
            await writer.wait_closed()
        self.peers.clear()

    async def connect_to_peer(self, peer_host, peer_port):
        """Initiates a connection, performs handshake, and requests the peer's chain."""
        try:
            reader, writer = await asyncio.open_connection(peer_host, peer_port)
            peer_addr = writer.get_extra_info('peername') # Use the confirmed address
            
            # --- THE FIX IS HERE ---
            # Immediately add the new peer to our dictionary.
            # We don't know their wallet address yet, so we'll store None for now.
            # The HANDSHAKE message from them will fill this in later.
            self.peers[peer_addr] = (reader, writer, None)
            logging.info(f"Successfully connected to peer {peer_addr}")
            # --- END FIX ---
            
            # Send our identity in a handshake
            handshake_msg = self.create_message("HANDSHAKE", {"address": self.node_wallet.address})
            await self.send_message(writer, handshake_msg)

            # Request the peer's chain to sync up
            get_chain_msg = self.create_message("GET_CHAIN")
            await self.send_message(writer, get_chain_msg)
            
            # Start listening for messages from this new peer
            asyncio.create_task(self.handle_connection(reader, writer))
            
        except ConnectionRefusedError:
            logging.warning(f"Connection refused by {peer_host}:{peer_port}")
        except Exception as e:
            logging.error(f"Failed to connect to {peer_host}:{peer_port}: {e}")


    def update_consensus_nodes(self):
        """Updates the consensus mechanism with the current list of Wallet objects."""
        peer_wallets = [wallet for _, _, wallet in self.peers.values() if wallet]
        all_wallets = peer_wallets + [self.node_wallet]
        
        # We create a dictionary to ensure uniqueness based on the wallet address
        unique_wallets = {wallet.address: wallet for wallet in all_wallets}
        
        self.consensus.all_nodes = list(unique_wallets.values())
        logging.info(f"Consensus nodes updated. Total unique nodes: {len(self.consensus.all_nodes)}")

    async def handle_connection(self, reader, writer):
        """Handles all incoming data from a single connection."""
        peer_addr = writer.get_extra_info('peername')

        try:
            while True:
                len_data = await reader.readexactly(4)
                msg_len = int.from_bytes(len_data, 'big')
                msg_data = await reader.readexactly(msg_len)
                message = json.loads(msg_data.decode())
                
                await self.handle_message(message, writer)

        except (asyncio.IncompleteReadError, ConnectionResetError):
            logging.warning(f"Peer {peer_addr} disconnected.")
        except Exception as e:
            logging.error(f"Error handling connection from {peer_addr}: {e}")
        finally:
            if peer_addr in self.peers:
                del self.peers[peer_addr]
            self.update_consensus_nodes()
            writer.close()
            await writer.wait_closed()
            logging.info(f"Connection with {peer_addr} closed.")

    async def handle_message(self, message, writer):
        """The main message router, now with chain resolution logic."""
        msg_id, msg_type = message.get("id"), message.get("type")
        originator_addr = writer.get_extra_info('peername')

        if msg_id in self.seen_messages:
            return
        self.seen_messages.add(msg_id)
        
        logging.info(f"Received '{msg_type}' from {originator_addr}")

        if msg_type == "PING":
            # Received a ping, send a pong right back to the sender
            pong_message = self.create_message("PONG", message.get("payload"))
            await self.send_message(writer, pong_message)
            return # Stop processing here

        elif msg_type == "PONG":
            # Received a pong, log it
            sent_time = message.get("payload", {}).get("time")
            if sent_time:
                rtt = (time.time() - sent_time) * 1000
                logging.info(f"PONG received from {originator_addr}. Round-trip time: {rtt:.2f} ms")
            return

        elif msg_type == "HANDSHAKE":
            peer_wallet_address_hex = message.get("payload", {}).get("address")
            if peer_wallet_address_hex:
                peer_wallet = Wallet()
                try:
                    peer_wallet.public_key = bytes.fromhex(peer_wallet_address_hex)
                    self.peers[originator_addr] = (writer.get_extra_info('stream'), writer, peer_wallet)
                    logging.info(f"Handshake complete. Peer {originator_addr} wallet loaded.")
                    self.update_consensus_nodes()
                except Exception as e:
                    logging.error(f"Failed to load peer wallet from public key hex: {e}")
            else:
                logging.warning(f"Received invalid handshake from {originator_addr}")

        elif msg_type == "NEW_TRANSACTION":
            values = message.get("payload")
            success = self.blockchain.add_transaction(
                values['transaction_dict'], values['signature_hex']
            )
            if success:
                logging.info("Transaction valid. Added to mempool and broadcasting.")
                await self.broadcast(message, originator_writer=writer)
            else:
                logging.warning("Received invalid transaction from peer. Rejected.")

        elif msg_type == "NEW_BLOCK":
            block_data = message.get("payload")
            last_block = self.blockchain.last_block

            # --- UPGRADED LOGIC ---
            # 1. Standard case: The new block extends our current chain
            if block_data['index'] == last_block.index + 1 and block_data['previous_hash'] == last_block.hash:
                # We should still validate the block before appending
                new_block = Block.from_dict(block_data)
                if new_block.hash == new_block.calculate_hash(): # Basic validation
                    self.blockchain.chain.append(new_block)
                    self.blockchain.pending_transactions = []
                    logging.info(f"✅ Appended new block #{block_data['index']} from peer.")
                    await self.broadcast(message, originator_writer=writer)
                else:
                    logging.warning(f"❌ Received block #{block_data['index']} with invalid hash.")

            # 2. Conflict case: The new block's index is the same as our last block, indicating a split
            elif block_data['index'] == last_block.index:
                logging.info(f"Chain split detected at index {last_block.index}. Querying peer for its full chain.")
                 # We don't need to do anything here, the node that mines the *next* block will resolve this
                pass

            # 3. Catch-up case: We are behind
            elif block_data['index'] > last_block.index:
                logging.warning(f"We seem to be behind. Our index: {last_block.index}, Peer's index: {block_data['index']}.")
                # This is a simplified catch-up. A real implementation would request the full chain.
                # For now, we accept it if the previous hash matches our last block, assuming we just missed one block.
                # A more robust implementation would be needed for larger gaps.
                if block_data['previous_hash'] == last_block.hash:
                    self.blockchain.chain.append(Block.from_dict(block_data))
                    self.blockchain.pending_transactions = []
                    logging.info(f"✅ Caught up by appending block #{block_data['index']}.")
            else:
                # The block is old and irrelevant
                logging.info(f"Ignoring old block #{block_data.get('index')}.")

    async def send_message(self, writer, message):
        """Encodes and sends a message to a specific writer with length-prefixing."""
        try:
            msg_bytes = json.dumps(message).encode()
            len_bytes = len(msg_bytes).to_bytes(4, 'big')
            writer.write(len_bytes + msg_bytes)
            await writer.drain()
        except ConnectionResetError:
            pass # Cleanup is handled in the main connection loop

    async def broadcast(self, message, originator_writer=None):
        """Sends a message to all connected peers except the originator."""
        all_writers = [w for _, w, _ in self.peers.values()]
        for writer in all_writers:
            if writer is not originator_writer:
                await self.send_message(writer, message)

    async def trigger_consensus_and_mine(self):
        """Replicates the logic of your /mine endpoint using the blockchain's own method."""
        if not self.blockchain.pending_transactions:
            logging.info('No pending transactions to create a block.')
            return

        logging.info("Triggering DPoL consensus to select a block proposer...")
        delegates = self.consensus.select_delegates(self.blockchain.last_block.hash)
        
        if not delegates:
            logging.error("Consensus failed to select delegates.")
            return

        primary_delegate_address = delegates[0]
        if primary_delegate_address == self.node_wallet.address:
            logging.info(f"✅ This node WON consensus and will create the block.")
            
            # Now we call your blockchain's own robust mine_block method.
            new_block = self.blockchain.mine_block(
                proposer_address=self.node_wallet.address
            )
            
            if new_block:
                # Broadcast the new block to the network
                block_message = self.create_message("NEW_BLOCK", new_block.__dict__)
                await self.broadcast(block_message)
        else:
            logging.info(f"Consensus complete. Block proposer is {primary_delegate_address[:10]}...")
            logging.info("Waiting for the new block from the winner.")

async def main(args):
    # (The setup part of this function remains the same)
    node_wallet = Wallet()
    blockchain = Blockchain()
    consensus = DPoLConsensus(nodes=[], num_delegates=5)
    node = P2PNode(args.host, args.port, node_wallet, blockchain, consensus)
    server_task = asyncio.create_task(node.start())
    await asyncio.sleep(1)
    if args.peers:
        for peer in args.peers.split(','):
            try:
                peer_host, peer_port = peer.split(':')
                await node.connect_to_peer(peer_host, int(peer_port))
            except ValueError:
                logging.error(f"Invalid peer format: {peer}. Use HOST:PORT.")

    def find_encryption_key(address):
        for block in reversed(node.blockchain.chain):
            for signed_tx in block.transactions:
                tx = signed_tx['transaction_dict']
                if tx.get('tx_type') == 'key_registration' and tx.get('sender_address') == address:
                    return tx['content']['encryption_key']
        return None

    while True:
        try:
            # --- NEW: Added 'ping' to the list of commands ---
            cmd = await asyncio.to_thread(input, "\nCommands: ping, register_key, send_msg, mempool, mine, peers, chain, exit\n> ")
            
            # --- NEW: ping command ---
            if cmd == 'ping':
                ping_message = node.create_message("PING", {"time": time.time()})
                await node.broadcast(ping_message)
            
            # (The rest of the commands like register_key, send_msg, etc. remain the same)
            elif cmd == 'register_key':
                tx_obj = Transaction(sender_wallet=node.node_wallet, message="", tx_type="key_registration")
                tx_dict = tx_obj.to_dict()
                signature = node.node_wallet.sign_transaction(tx_dict)
                payload = {'transaction_dict': tx_dict, 'signature_hex': signature.hex()}
                if node.blockchain.add_transaction(tx_dict, signature.hex()):
                    tx_message = node.create_message("NEW_TRANSACTION", payload)
                    await node.broadcast(tx_message)
            elif cmd.startswith('send_msg'):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Usage: send_msg <recipient_address> <message>")
                    continue
                recipient_addr = parts[1]
                message_text = " ".join(parts[2:])
                recipient_enc_key = find_encryption_key(recipient_addr)
                if not recipient_enc_key:
                    print("Could not find recipient's encryption key on the blockchain. They must register it first.")
                    continue
                recipient_keys = {"address": recipient_addr, "encryption_key": recipient_enc_key}
                tx_obj = Transaction(sender_wallet=node.node_wallet, message=message_text, recipient_public_keys_hex=recipient_keys, tx_type="message")
                tx_dict = tx_obj.to_dict()
                signature = node.node_wallet.sign_transaction(tx_dict)
                payload = {'transaction_dict': tx_dict, 'signature_hex': signature.hex()}
                if node.blockchain.add_transaction(tx_dict, signature.hex()):
                    tx_message = node.create_message("NEW_TRANSACTION", payload)
                    await node.broadcast(tx_message)
            elif cmd == 'mempool':
                print(f"Node has {len(node.blockchain.pending_transactions)} pending transactions:")
                print(json.dumps(node.blockchain.pending_transactions, indent=2))
            elif cmd == 'mine':
                if not node.blockchain.pending_transactions:
                    logging.info('No pending transactions to create a block.')
                    continue
                logging.info("--- (TESTING) Bypassing DPoL, this node is the automatic winner. ---")
                new_block = node.blockchain.mine_block(proposer_address=node.node_wallet.address)
                if new_block:
                    block_message = node.create_message("NEW_BLOCK", new_block.__dict__)
                    await node.broadcast(block_message)
            elif cmd == 'peers':
                logging.info(f"Connected to {len(node.peers)} peers: {list(node.peers.keys())}")
            elif cmd == 'chain':
                print(json.dumps([b.__dict__ for b in node.blockchain.chain], indent=2, default=str))
            elif cmd == 'exit':
                break
        except (EOFError, KeyboardInterrupt):
            break

    server_task.cancel()
    await node.stop()
    logging.info("Node shut down.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a P2P blockchain node.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to listen on.')
    parser.add_argument('--port', type=int, required=True, help='Port to listen on.')
    parser.add_argument('--peers', type=str, help='Comma-separated list of bootstrap peers (e.g., localhost:8001).')
    
    args = parser.parse_args()
    
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user.")