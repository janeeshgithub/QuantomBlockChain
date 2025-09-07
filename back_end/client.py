# client.py
from core.wallet import Wallet
from core.transaction import Transaction
from crypto import dilithium_utils
import json

alice = Wallet()
bob = Wallet() 
tx = Transaction(alice, bob.get_public_keys_hex(), "test message")
tx_dict = tx.to_dict()
signature = dilithium_utils.sign_data(alice.signing_secret_key, tx_dict)
payload = {"transaction_dict": tx_dict, "signature_hex": signature.hex()}
print(json.dumps(payload, indent=4))