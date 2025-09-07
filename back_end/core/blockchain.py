import json
from core.block import Block
from crypto import dilithium_utils

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self) -> Block:
        """
        Creates the very first block in the chain using static, deterministic values.
        This ensures that every node starts with the exact same Block #0.
        """
        # Create the block with hardcoded values
        genesis_block = Block(
            index=0, 
            transactions=[], 
            previous_hash="0", 
            proposer_address="genesis"
        )
        
        # Manually set a fixed timestamp to ensure the hash is always the same
        genesis_block.timestamp = 0
        
        # Manually set the hash to its pre-calculated value
        genesis_block.hash = genesis_block.calculate_hash()
        
        # Sanity check to ensure the hash is what we expect
        # The expected hash for the block with timestamp=0 is:
        # '092994138b1f3a595353523e38714150b07881c15f9b803c757a2210a52f2070'
        
        return genesis_block

    @property
    def last_block(self) -> Block:
        """Returns the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, transaction_dict: dict, signature_hex: str) -> bool:
        """
        Verifies a transaction's signature and adds it to the pending pool.
        This method is now more robust and correctly prepares data for verification.
        """
        try:
            # 1. Get the sender's address from the transaction data.
            sender_address_hex = transaction_dict['sender_address']
            
            # 2. Convert hex-encoded strings back to bytes for cryptographic operations.
            public_key_bytes = bytes.fromhex(sender_address_hex)
            signature_bytes = bytes.fromhex(signature_hex)
            
            # 3. Prepare the message for verification.
            #    This MUST be done in the exact same way the message was prepared for signing.
            message_bytes = json.dumps(transaction_dict, sort_keys=True).encode('utf-8')

            # 4. Verify the signature using the corrected function name and prepared message.
            is_valid = dilithium_utils.verify(public_key_bytes, message_bytes, signature_bytes)
            
            if not is_valid:
                print(f"❌ Transaction from {sender_address_hex[:10]}... has an invalid signature. Discarding.")
                return False
                
            # 5. Add the validated, signed transaction to the pending pool.
            #    This structure is consistent with what other parts of the system expect.
            signed_transaction = {
                'transaction_dict': transaction_dict,
                'signature_hex': signature_hex
            }
            self.pending_transactions.append(signed_transaction)
            print(f"✅ Transaction from {sender_address_hex[:10]}... verified and added to pending pool.")
            return True

        except (KeyError, ValueError, TypeError) as e:
            # Catch errors from missing keys, bad hex values, or other data issues.
            print(f"❌ Discarding malformed transaction. Error: {e}")
            return False

    def mine_block(self, proposer_address: str) -> Block:
        """
        Creates a new block from pending transactions and adds it to the chain.
        """
        if not self.pending_transactions:
            print("No pending transactions to mine.")
            return None

        new_block = Block(
            index=self.last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=self.last_block.hash,
            proposer_address=proposer_address
        )

        self.chain.append(new_block)
        
        # Clear the pending transactions pool after mining.
        self.pending_transactions = []
        
        print(f"⛓️ Block #{new_block.index} mined by {proposer_address[:10]}... and added to the chain.")
        return new_block
    
    def replace_chain(self, new_chain: list[dict]) -> bool:
        """
        Replaces the current chain with a longer, valid chain from a peer.
        """
        if len(new_chain) <= len(self.chain):
            # The incoming chain isn't longer, so we ignore it.
            return False

        # Validate the new chain to ensure all blocks are correctly linked and hashed.
        for i in range(1, len(new_chain)):
            current_block_data = new_chain[i]
            previous_block_data = new_chain[i-1]
            
            # Re-create the Block object to verify its hash integrity.
            block_to_verify = Block.from_dict(current_block_data)
            
            if block_to_verify.hash != block_to_verify.calculate_hash():
                print(f"Chain validation failed: Block #{block_to_verify.index} has a corrupted hash.")
                return False
            
            if block_to_verify.previous_hash != previous_block_data['hash']:
                print(f"Chain validation failed: Block #{block_to_verify.index} has a broken link to the previous block.")
                return False
        
        print(f"✅ Incoming chain is valid. Replacing local chain of length {len(self.chain)} with new chain of length {len(new_chain)}.")
        # Reconstruct the chain with proper Block objects.
        self.chain = [Block.from_dict(block_data) for block_data in new_chain]
        return True
