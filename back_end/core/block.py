import hashlib
import json
from time import time

class Block:
    def __init__(self, index: int, transactions: list, previous_hash: str, proposer_address: str):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions # A list of signed transaction dicts
        self.previous_hash = previous_hash
        self.proposer_address = proposer_address
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculates the SHA-256 hash of the block's content.
        """
        # Ensure transactions are sorted for a consistent hash
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "proposer_address": self.proposer_address
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()