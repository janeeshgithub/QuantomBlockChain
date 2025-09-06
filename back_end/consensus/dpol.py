import hashlib
import time
import json

# --- PQ-DPoL Consensus Module ---

class PqDpolConsensus:
    """
    Implements the PQ-DPoL consensus mechanism.
    This class is responsible for delegate selection and block validation.
    """

    def __init__(self, nodes, num_delegates=21):
        """
        Initializes the consensus mechanism with the network participants.
        
        Args:
            nodes (list): A list of all node objects participating in the network.
                          Each node object must have a '.node_id' attribute.
            num_delegates (int): The number of delegates to select in each round.
        """
        self.all_nodes = nodes
        self.num_delegates = num_delegates

    def _simulate_ivrf_generation(self, node_id, previous_hash):
        """
        *** SIMULATION of iVRF Generation ***
        In a real system, this would use a post-quantum iVRF library.
        It generates a verifiable random number and a proof.
        """
        vrf_input = f"{node_id}-{previous_hash}".encode()
        random_value = hashlib.sha256(vrf_input).hexdigest()
        proof = True  # In reality, this would be a complex cryptographic proof.
        return random_value, proof

    def _simulate_ivrf_verification(self, proof):
        """
        *** SIMULATION of iVRF Verification ***
        In a real system, this would verify the proof using the node's public key.
        """
        return proof

    def select_delegates(self, previous_block_hash):
        """
        Runs the fair lottery to select the delegate committee for the round.

        Args:
            previous_block_hash (str): The hash of the latest block in the chain.

        Returns:
            list: A sorted list of delegate node IDs, with the primary at index 0.
        """
        print("\n--- Starting Delegate Election ---")
        node_scores = {}

        # 1. All nodes generate and "broadcast" their VRF values
        for node in self.all_nodes:
            random_value, proof = self._simulate_ivrf_generation(node.node_id, previous_block_hash)
            
            # 2. Each node verifies the values and calculates scores
            if self._simulate_ivrf_verification(proof):
                # Score is the absolute difference between the random value and the hash
                score = abs(int(previous_block_hash, 16) - int(random_value, 16))
                node_scores[node.node_id] = score
                # print(f"  - Calculated score for {node.node_id}: {score}")

        # 3. Sort nodes by score to find the "luckiest" ones
        if not node_scores:
            print("Error: No scores were calculated. Cannot select delegates.")
            return []
            
        sorted_nodes = sorted(node_scores.keys(), key=lambda id: node_scores[id])
        
        delegates = sorted_nodes[:self.num_delegates]
        print(f"--- Election Complete. Primary Delegate: {delegates[0]} ---")
        print(f"Full Delegate Committee: {delegates}")
        return delegates

    def create_new_block(self, delegates, pending_transactions, last_block, BlockClass):
        """
        Simulates the block creation and PBFT consensus among delegates.

        Args:
            delegates (list): The list of selected delegate node IDs.
            pending_transactions (list): The transactions to be included in the block.
            last_block (Block): The current last block of your blockchain.
            BlockClass (class): Your own Block class for instantiation.

        Returns:
            Block: A new, validated block, or None if consensus fails.
        """
        if not delegates:
            print("Consensus Error: Cannot create a block without delegates.")
            return None
        
        primary_delegate_id = delegates[0]
        print(f"\nPrimary Delegate '{primary_delegate_id}' is proposing a new block...")

        # The primary delegate creates the block
        # In a real system, the block's contents would be compressed (e.g., with Snappy)
        # before being sent to other delegates.
        proposed_block = BlockClass(
            timestamp=time.time(),
            transactions=pending_transactions,
            previous_hash=last_block.hash
        )

        # *** SIMULATION of PBFT Consensus ***
        # The primary sends the proposed_block to the other delegates.
        # They would vote in "prepare" and "commit" phases.
        # Here, we assume the consensus is successful if at least 2/3 of delegates agree.
        num_votes = len(delegates)
        required_votes = (2 * num_votes // 3) + 1
        print(f"Simulating PBFT: requires {required_votes} of {num_votes} votes to agree.")
        print("Consensus reached!")
        
        # All messages (proposals, votes) in a real PBFT system would be signed
        # using a post-quantum signature scheme like Falcon.
        
        return proposed_block

# --- Example of How to Use This Module ---

if __name__ == '__main__':
    # 1. SETUP: Create dummy classes and objects that you would already have.
    
    # Your Block class (dummy version for this example)
    class DummyBlock:
        def __init__(self, timestamp, transactions, previous_hash):
            self.timestamp = timestamp
            self.transactions = transactions
            self.previous_hash = previous_hash
            # In your real class, the hash calculation would be more robust
            self.hash = hashlib.sha256(str(time.time()).encode()).hexdigest()

    # Your Node/Wallet class (dummy version)
    class DummyNode:
        def __init__(self, name):
            # Your key generation would create a unique ID (like a public key)
            self.node_id = f"node_id_{name}_{hashlib.sha256(name.encode()).hexdigest()[:8]}"

    # Create a dummy network of nodes
    NODE_COUNT = 50
    network_nodes = [DummyNode(f"Node-{i}") for i in range(NODE_COUNT)]
    
    # Create a dummy last block
    last_block = DummyBlock(time.time(), [], "0")
    print(f"Starting with last block hash: {last_block.hash}")

    # A list of pending transactions you've collected
    pending_txs = [{"from": "Alice", "to": "Bob", "amount": 10}]

    # 2. INITIALIZE the consensus mechanism with your nodes
    consensus_protocol = PqDpolConsensus(nodes=network_nodes, num_delegates=21)

    # 3. RUN one full consensus round
    
    # a. Select delegates for this round
    delegates = consensus_protocol.select_delegates(last_block.hash)
    
    # b. Propose and validate a new block
    new_block = consensus_protocol.create_new_block(
        delegates=delegates,
        pending_transactions=pending_txs,
        last_block=last_block,
        BlockClass=DummyBlock  # Pass your actual Block class here
    )

    # 4. GET the result
    if new_block:
        print("\n--- Consensus Successful: New Block Ready to be Added ---")
        print(f"  - Hash: {new_block.hash}")
        print(f"  - Previous Hash: {new_block.previous_hash}")
        print(f"  - Transactions: {len(new_block.transactions)}")
        # Now you would add this block to your blockchain instance:
        # my_blockchain.add_block(new_block)