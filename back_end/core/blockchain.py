# core/blockchain.py

from core.block import Block
from crypto import dilithium_utils

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self) -> Block:
        """Creates the very first block in the chain."""
        return Block(index=0, transactions=[], previous_hash="0", proposer_address="genesis")

    @property
    def last_block(self) -> Block:
        """Returns the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, transaction_dict: dict, signature_hex: str) -> bool:
        """
        Verifies and adds a transaction to the list of pending transactions.
        """
        # 1. Get the sender's public key (address) to verify the signature
        sender_address_hex = transaction_dict['sender_address']
        public_key = bytes.fromhex(sender_address_hex)
        signature = bytes.fromhex(signature_hex)
        
        # 2. Verify the signature
        is_valid = dilithium_utils.verify_signature(public_key, transaction_dict, signature)
        
        if not is_valid:
            print(f"Transaction from {sender_address_hex} has an invalid signature. Discarding.")
            return False
            
        # 3. Add the signed transaction to the pending pool
        signed_transaction = {
            "data": transaction_dict,
            "signature": signature_hex
        }
        self.pending_transactions.append(signed_transaction)
        print(f"Transaction from {sender_address_hex} added to pending pool.")
        return True

    def mine_block(self, proposer_address: str) -> Block:
        """
        Creates a new block from pending transactions and adds it to the chain.
        In a real system, the proposer would be chosen by the consensus algorithm (dPoL).
        """
        if not self.pending_transactions:
            print("No pending transactions to mine.")
            return None

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block.hash,
            proposer_address=proposer_address
        )

        # In a real network, this block would be broadcast for validation
        self.chain.append(new_block)
        
        # Clear the pending transactions pool
        self.pending_transactions = []
        
        print(f"Block #{new_block.index} mined by {proposer_address} and added to the chain.")
        return new_block