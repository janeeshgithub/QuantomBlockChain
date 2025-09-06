from core.wallet import Wallet
from core.transaction import Transaction
from core.blockchain import Blockchain
from crypto import dilithium_utils, kyber_utils
from consensus.dpol import DPoLConsensus

def main():
    """
    Runs a full simulation of the blockchain, including DPoL consensus.
    """
    # --- 1. NETWORK SETUP ---
    print("--- 1. Setting up the simulated network and blockchain ---")
    
    # Create a network of 50 nodes (wallets)
    NODE_COUNT = 50
    network_nodes = [Wallet() for _ in range(NODE_COUNT)]
    
    # Assign Alice and Bob from the pool of nodes
    alice_wallet = network_nodes[0]
    bob_wallet = network_nodes[1]

    my_blockchain = Blockchain()
    consensus_protocol = DPoLConsensus(nodes=network_nodes, num_delegates=21)

    print(f"Network created with {len(network_nodes)} nodes.")
    print(f"Alice's Address: {alice_wallet.address[:10]}...")
    print(f"Bob's Address:   {bob_wallet.address[:10]}...\n")

    # --- 2. ALICE CREATES AND SIGNS A TRANSACTION ---
    print("--- 2. Alice creates and signs an encrypted transaction for Bob ---")
    message = "Project QuantumLeap is a go. Initiate phase 2."
    
    tx = Transaction(
        sender_wallet=alice_wallet, 
        recipient_public_keys_hex=bob_wallet.get_public_keys_hex(),
        message=message
    )
    print(f"Original message: '{message}'")

    transaction_dict = tx.to_dict()
    signature = dilithium_utils.sign_data(alice_wallet.signing_secret_key, transaction_dict)
    print("Transaction signed with Dilithium.\n")

    # --- 3. TRANSACTION IS SUBMITTED TO THE PENDING POOL ---
    print("--- 3. Transaction submitted to the network's pending pool ---")
    my_blockchain.add_transaction(transaction_dict, signature.hex())

    # --- 4. DPoL CONSENSUS ROUND ---
    print("\n--- 4. Initiating DPoL consensus round to create a new block ---")
    
    # a. The network runs the lottery to select delegates for this round
    last_block = my_blockchain.last_block
    delegates = consensus_protocol.select_delegates(last_block.hash)
    
    # b. The primary delegate proposes and validates a new block
    if delegates:
        new_block = consensus_protocol.create_new_block(
            delegates=delegates,
            pending_transactions=my_blockchain.pending_transactions,
            last_block=last_block,
        )
    else:
        new_block = None

    # --- 5. NEW BLOCK IS ADDED TO THE CHAIN ---
    if new_block:
        # The blockchain accepts the new block from the consensus winner
        my_blockchain.chain.append(new_block)
        my_blockchain.pending_transactions = [] # Clear the pool
        print("\n--- 5. New block successfully added to the blockchain! ---")
        print(f"   - Block #{new_block.index} proposed by {new_block.proposer_address[:10]}...")
        print(f"   - Blockchain now has {len(my_blockchain.chain)} blocks.\n")
    else:
        print("\n--- 5. Consensus failed. No new block was added. ---\n")
        return # End simulation if no block was created

    # --- 6. BOB DECRYPTS THE MESSAGE FROM THE BLOCKCHAIN ---
    print("--- 6. Bob scans the new block and decrypts his message ---")
    
    latest_block = my_blockchain.last_block
    for signed_tx in latest_block.transactions:
        tx_data = signed_tx['data']
        if tx_data['recipient_address'] == bob_wallet.address:
            print("Bob found a transaction for him.")
            
            encrypted_content = tx_data['encrypted_content']
            
            ciphertext = bytes.fromhex(encrypted_content['ciphertext'])
            nonce = bytes.fromhex(encrypted_content['nonce'])
            payload = bytes.fromhex(encrypted_content['payload'])

            shared_secret = kyber_utils.decapsulate_key(bob_wallet.encryption_secret_key, ciphertext)
            decrypted_message = kyber_utils.decrypt_message(shared_secret, nonce, payload)

            print(f"Decrypted message: '{decrypted_message}'")

            # Final check
            if message == decrypted_message:
                print("\n✅ SUCCESS: End-to-end test complete! The system works.")
            else:
                print("\n❌ FAILURE: Decrypted message does not match the original.")
            break

if __name__ == "__main__":
    main()