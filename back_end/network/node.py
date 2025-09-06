# network/node.py

import sys
import os
import requests
from uuid import uuid4
from flask import Flask, jsonify, request

# --- Add project root to path to allow imports ---
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..')
sys.path.append(parent_dir)
# ---------------------------------------------------

from core.blockchain import Blockchain
from core.wallet import Wallet
from consensus.dpol import DPoLConsensus

# --- Node Setup ---
app = Flask(__name__)

# A globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# This node's personal wallet
node_wallet = Wallet()
print(f"Node starting with address: {node_wallet.address[:10]}...")

# Instantiate the Blockchain
blockchain = Blockchain()

# Store the addresses of other nodes in the network
network_nodes = set()

# Initialize the DPoL Consensus
# In a real system, the list of nodes would be discovered and updated dynamically.
# For our simulation, we'll manage it via the /nodes/register endpoint.
consensus = DPoLConsensus(nodes=[], num_delegates=5)


# --- API Endpoints ---

@app.route('/chain', methods=['GET'])
def get_full_chain():
    """Returns the node's full blockchain."""
    response = {
        'chain': [block.__dict__ for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Receives a new transaction, verifies it, and adds it to the pool."""
    values = request.get_json()
    required = ['transaction_dict', 'signature_hex']
    if not all(k in values for k in required):
        return 'Missing values', 400

    success = blockchain.add_transaction(values['transaction_dict'], values['signature_hex'])

    if success:
        # Broadcast the new transaction to all other known nodes
        for node_url in network_nodes:
            try:
                requests.post(f"{node_url}/transactions/new", json=values, timeout=1)
            except requests.exceptions.RequestException:
                print(f"Warning: Could not broadcast transaction to {node_url}")

        response = {'message': 'Transaction will be added to the next block.'}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid transaction.'}
        return jsonify(response), 400


@app.route('/mine', methods=['GET'])
def mine_block_endpoint():
    """Triggers the consensus mechanism to create a new block."""
    last_block = blockchain.last_block
    
    # Run the delegate election
    delegates = consensus.select_delegates(last_block.hash)
    
    if not delegates:
        return jsonify({'message': 'Delegate selection failed.'}), 500

    # The winner (primary delegate) creates the block
    primary_delegate_address = delegates[0]
    
    # In a real network, only the winning node would proceed.
    # Here, we simulate this by checking if WE are the winner.
    if primary_delegate_address == node_wallet.address:
        print(f"This node ({node_wallet.address[:10]}...) won the election and will propose a block.")
        
        new_block = consensus.create_new_block(
            delegates=delegates,
            pending_transactions=blockchain.pending_transactions,
            last_block=last_block
        )

        # Broadcast the new block to the network
        for node_url in network_nodes:
            try:
                requests.post(f"{node_url}/block/add", json=new_block.__dict__)
            except requests.exceptions.RequestException:
                print(f"Warning: Could not broadcast new block to {node_url}")

        # Add the block to our own chain and clear pending transactions
        blockchain.chain.append(new_block)
        blockchain.pending_transactions = []
        
        response = {
            'message': "New block proposed and broadcasted.",
            'block': new_block.__dict__
        }
        return jsonify(response), 200
    else:
        message = f"This node lost the election. Winner: {primary_delegate_address[:10]}..."
        return jsonify({'message': message}), 200

@app.route('/block/add', methods=['POST'])
def add_block():
    """Receives a new block broadcasted by a winning delegate."""
    block_data = request.get_json()
    
    # A simple validation: check if the previous hash matches our last block
    last_block = blockchain.last_block
    if block_data['previous_hash'] != last_block.hash:
        return jsonify({'message': 'Received block rejected.'}), 400
    
    # Note: In a real system, we'd do a full validation of the block here.
    
    # Create a block object from the received data
    block_to_add = Block(
        index=block_data['index'],
        transactions=block_data['transactions'],
        previous_hash=block_data['previous_hash'],
        proposer_address=block_data['proposer_address']
    )
    block_to_add.timestamp = block_data['timestamp']
    block_to_add.hash = block_data['hash'] # Trust the hash from the proposer

    blockchain.chain.append(block_to_add)
    # Important: Clear our pending transactions that are now in the block
    blockchain.pending_transactions = [] 
    
    return jsonify({'message': 'New block added to the chain.'}), 201


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Registers new nodes with this node."""
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        network_nodes.add(node)
    
    # Update the consensus mechanism with the full list of participants
    # This part is a simplification for our simulation.
    node_wallets = [Wallet() for _ in network_nodes] # Create dummy wallets for consensus
    consensus.all_nodes = [node_wallet] + node_wallets # Include self

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(network_nodes),
    }
    return jsonify(response), 201


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)