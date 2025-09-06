import hashlib
import time
import json
import sys
import os

# --- This part allows the script to import from the 'core' directory ---
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..')
sys.path.append(parent_dir)
# ----------------------------------------------------------------------

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
    