# core/public_ledger.py

class PublicKeyLedger:
    """
    Scans the blockchain to build a user-friendly, in-memory registry of 
    usernames mapped to their public keys.
    """
    def __init__(self):
        # This dictionary will be our address book: username -> {address, encryption_key}
        self.users = {}

    def update_from_chain(self, blockchain):
        """
        Iterates through the entire blockchain to find key registrations
        and updates the user registry.
        """
        print("Updating public key ledger from blockchain...")
        for block in blockchain.chain:
            for signed_tx in block.transactions:
                tx = signed_tx.get('transaction_dict', {})
                if tx.get('tx_type') == 'key_registration':
                    username = tx.get('username')
                    address = tx.get('sender_address')
                    enc_key = tx.get('content', {}).get('encryption_key')
                    if username and address and enc_key:
                        self.users[username] = {"address": address, "encryption_key": enc_key}
        print(f"Ledger updated. Found {len(self.users)} registered users.")

    def get_keys_for_user(self, username: str) -> dict | None:
        """Retrieves the address and encryption key for a given username."""
        return self.users.get(username)

    def get_user_for_address(self, address: str) -> str | None:
        """
        Performs a reverse lookup to find a username from a public address.
        """
        for username, data in self.users.items():
            if data['address'] == address:
                return username
        return None

    def list_users(self) -> list[str]:
        """Returns a list of all registered usernames."""
        return list(self.users.keys())