import hashlib
import time
import json
import sys
import os

# --- This part is to make the script runnable from the consensus directory ---
# It adds the parent directory (your project's root) to the Python path
# so we can import modules from the 'core' directory.
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..')
sys.path.append(parent_dir)
# --------------------------------------------------------------------------

from core.block import Block
from core.wallet import Wallet

class DPoLConsensus:
    """
    Implements a simulation of a Delegated Proof of Luck (dPoL) consensus mechanism.
    This class is responsible for delegate selection and block creation proposal.
    """

    def __init__(self, nodes: list[Wallet], num_delegates: int = 21):
        """
        Initializes the consensus mechanism.
        
        Args:
            nodes (list[Wallet]): A list of all Wallet objects participating.
            num_delegates (int): The number of delegates to select in each round.
        """
        self.all_nodes = nodes
        self.num_delegates = num_delegates

    def _simulate_ivrf_generation(self, node_address: str, previous_hash: str) -> tuple[str, bool]:
        """
        *** SIMULATION of iVRF Generation ***
        In a real system, this would use a post-quantum iVRF library.
        It generates a verifiable random number and a proof.
        """
        vrf_input = f"{node_address}-{previous_hash}".encode()
        random_value = hashlib.sha256(vrf_input).hexdigest()
        proof = True  # In reality, this would be a complex cryptographic proof.
        return random_value, proof

    def _simulate_ivrf_verification(self, proof: bool) -> bool:
        """
        *** SIMULATION of iVRF Verification ***
        In a real system, this would verify the proof using the node's public key.
        """
        return proof

    def select_delegates(self, previous_block_hash: str) -> list[str]:
        """
        Runs the fair lottery to select the delegate committee for the round.

        Args:
            previous_block_hash (str): The hash of the latest block in the chain.

        Returns:
            list: A sorted list of delegate addresses, with the primary at index 0.
        """
        print("\n--- Starting Delegate Election ---")
        node_scores = {}

        # 1. All nodes generate and "broadcast" their VRF values
        for node in self.all_nodes:
            random_value, proof = self._simulate_ivrf_generation(node.address, previous_block_hash)
            
            # 2. Each node verifies the values and calculates scores
            if self._simulate_ivrf_verification(proof):
                # Score is the absolute difference between the random value and the hash
                score = abs(int(previous_block_hash, 16) - int(random_value, 16))
                node_scores[node.address] = score
        
        # 3. Sort nodes by score to find the "luckiest" ones
        if not node_scores:
            print("Error: No scores were calculated. Cannot select delegates.")
            return []
            
        sorted_addresses = sorted(node_scores.keys(), key=lambda addr: node_scores[addr])
        
        delegates = sorted_addresses[:self.num_delegates]
        print(f"--- Election Complete. Primary Delegate: {delegates[0][:10]}...")
        # print(f"Full Delegate Committee: {delegates}")
        return delegates

    def create_new_block(self, delegates: list[str], pending_transactions: list, last_block: Block) -> Block:
        """
        Simulates the block creation and PBFT consensus among delegates.

        Args:
            delegates (list): The list of selected delegate addresses.
            pending_transactions (list): The transactions to be included.
            last_block (Block): The current last block of the blockchain.

        Returns:
            Block: A new, validated block, or None if consensus fails.
        """
        if not delegates:
            print("Consensus Error: Cannot create a block without delegates.")
            return None
        
        primary_delegate_address = delegates[0]
        print(f"\nPrimary Delegate '{primary_delegate_address[:10]}...' is proposing a new block...")

        # The primary delegate creates the block
        # *** CORRECTED to include index and proposer_address ***
        proposed_block = Block(
            index=last_block.index + 1,
            transactions=pending_transactions,
            previous_hash=last_block.hash,
            proposer_address=primary_delegate_address
        )

        # *** SIMULATION of PBFT Consensus ***
        # The primary sends the proposed_block to other delegates for voting.
        # We assume the consensus is successful.
        num_votes = len(delegates)
        required_votes = (2 * num_votes // 3) + 1
        print(f"Simulating PBFT: requires {required_votes} of {num_votes} votes. Consensus reached!")
        
        return proposed_block

# --- Example of How to Use and Test This Module ---

if __name__ == '__main__':
    print("--- Running DPoL Consensus Simulation ---")
    
    # 1. SETUP: Create a dummy network and blockchain state
    NODE_COUNT = 50
    network_wallets = [Wallet() for i in range(NODE_COUNT)]
    
    # Use the genesis block as the last known block
    genesis_block = Block(index=0, transactions=[], previous_hash="0", proposer_address="genesis")
    print(f"Starting with last block hash: {genesis_block.hash}")

    # Create some dummy pending transactions
    pending_txs = [{"data": {"from": "Alice", "to": "Bob"}, "signature": "..."}]

    # 2. INITIALIZE the consensus mechanism
    consensus_protocol = DPoLConsensus(nodes=network_wallets, num_delegates=21)

    # 3. RUN one full consensus round
    
    # a. Select delegates for this round
    delegates = consensus_protocol.select_delegates(genesis_block.hash)
    
    # b. Propose and validate a new block using the selected delegates
    new_block = consensus_protocol.create_new_block(
        delegates=delegates,
        pending_transactions=pending_txs,
        last_block=genesis_block,
    )

    # 4. REVIEW the result
    if new_block:
        print("\n--- Consensus Successful: New Block Ready to be Added ---")
        print(f" - Index: {new_block.index}")
        print(f" - Hash: {new_block.hash}")
        print(f" - Proposer: {new_block.proposer_address[:10]}...")
        print(f" - Previous Hash: {new_block.previous_hash}")
        print(f" - Transactions included: {len(new_block.transactions)}")