import hashlib
import json
from time import time

class Block:
    def __init__(self, index: int, transactions: list, previous_hash: str, proposer_address: str, timestamp: float = None, a_hash: str = None):
        """
        Initializes a block.
        If timestamp or a_hash are provided, they are used. Otherwise, they are generated.
        This allows for both creating new blocks and reconstructing existing ones.
        """
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proposer_address = proposer_address
        
        # Use provided timestamp or create a new one
        self.timestamp = timestamp if timestamp is not None else time()
        
        # Use provided hash or calculate a new one
        # This is the crucial fix: we preserve the original hash when reconstructing
        self.hash = a_hash if a_hash is not None else self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculates the SHA-256 hash of the block's content.
        """
        # Create a dictionary of the block's data for hashing
        # IMPORTANT: We only include the data that defines the block, not the hash itself.
        block_data_for_hashing = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'proposer_address': self.proposer_address
        }
        
        # Ensure the data is sorted for a consistent hash
        block_string = json.dumps(block_data_for_hashing, sort_keys=True, default=str).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    @classmethod
    def from_dict(cls, block_data: dict):
        """Creates a Block object from a dictionary, preserving its original values."""
        return cls(
            index=block_data['index'],
            transactions=block_data['transactions'],
            previous_hash=block_data['previous_hash'],
            proposer_address=block_data['proposer_address'],
            # Pass the original timestamp and hash to the constructor
            timestamp=block_data.get('timestamp'),
            a_hash=block_data.get('hash')
        )