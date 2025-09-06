from core.wallet import Wallet
from core.transaction import Transaction
from core.blockchain import Blockchain
from crypto import dilithium_utils, kyber_utils

def main():
    """
    Runs a full simulation of the blockchain communication process.
    """
    # --- 1. SETUP ---
    print("--- 1. Initializing Blockchain and Wallets ---")
    my_blockchain = Blockchain()
    alice_wallet = Wallet()
    bob_wallet = Wallet()
    delegate_wallet = Wallet() # Represents the block proposer

    print(f"Alice's Address: {alice_wallet.address}")
    print(f"Bob's Address:   {bob_wallet.address}\n")

    # --- 2. ALICE CREATES AND SIGNS A TRANSACTION ---
    print("--- 2. Alice is creating and signing a transaction for Bob ---")
    message = "Meet me at the usual place at 5 PM. This is a secret."
    
    # Alice creates the transaction, which automatically encrypts the message for Bob
    tx = Transaction(
        sender_wallet=alice_wallet, 
        recipient_public_keys_hex=bob_wallet.get_public_keys_hex(),
        message=message
    )
    print(f"Original message: '{message}'")
    print("Transaction created and message encrypted using Kyber.")

    # Alice signs the transaction data with her Dilithium private key
    transaction_dict = tx.to_dict()
    signature = dilithium_utils.sign_data(alice_wallet.signing_secret_key, transaction_dict)
    print("Transaction signed with Dilithium.\n")

    # --- 3. TRANSACTION IS VERIFIED AND MINED ---
    print("--- 3. Submitting transaction to the blockchain's pending pool ---")
    # The transaction and signature are submitted to the network
    my_blockchain.add_transaction(transaction_dict, signature.hex())
    print("\nMining a new block...")
    
    # A delegate chosen by the consensus algorithm mines the block
    my_blockchain.mine_block(delegate_wallet.address)
    print(f"Blockchain now has {len(my_blockchain.chain)} blocks.\n")

    # --- 4. BOB DECRYPTS THE MESSAGE ---
    print("--- 4. Bob finds the transaction and decrypts the message ---")
    # Bob scans the latest block for transactions addressed to him
    latest_block = my_blockchain.last_block
    for signed_tx in latest_block.transactions:
        tx_data = signed_tx['data']
        if tx_data['recipient_address'] == bob_wallet.address:
            print("Bob found a transaction addressed to him.")
            
            # Get the encrypted content from the transaction data
            encrypted_content = tx_data['encrypted_content']
            
            # Convert hex data back to bytes
            ciphertext = bytes.fromhex(encrypted_content['ciphertext'])
            nonce = bytes.fromhex(encrypted_content['nonce'])
            payload = bytes.fromhex(encrypted_content['payload'])

            # Bob uses his PRIVATE encryption key to decapsulate the shared secret
            shared_secret = kyber_utils.decapsulate_key(bob_wallet.encryption_secret_key, ciphertext)
            
            # Bob uses the shared secret to decrypt the message
            decrypted_message = kyber_utils.decrypt_message(shared_secret, nonce, payload)

            print(f"Decrypted message: '{decrypted_message}'\n")

            # --- 5. FINAL VERIFICATION ---
            print("--- 5. Verifying message integrity ---")
            if message == decrypted_message:
                print("✅ SUCCESS: The decrypted message matches the original secret message!")
            else:
                print("❌ FAILURE: The messages do not match.")

# This ensures the main function is called when you run the script
if __name__ == "__main__":
    main()