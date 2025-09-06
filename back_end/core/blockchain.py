import json
from urllib.parse import urlparse
import requests
from time import time
from .block import Block
from .transaction import Transaction

class Blockchain:
	def __init__(self, crypto_suite):
		self.current_transactions = []
		self.chain = []
		self.nodes = set()
		self.crypto = crypto_suite
		self.new_block(previous_hash='1', proof=100)

	def register_node(self, address):
		parsed_url = urlparse(address)
		if parsed_url.netloc:
			self.nodes.add(parsed_url.netloc)
		elif parsed_url.path:
			self.nodes.add(parsed_url.path)
		else:
			raise ValueError('Invalid URL')

	def valid_chain(self, chain):
		last_block = chain[0]
		current_index = 1
		while current_index < len(chain):
			block = chain[current_index]
			if block['previous_hash'] != self.hash(last_block):
				return False
			if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
				return False
			last_block = block
			current_index += 1
		return True

	def resolve_conflicts(self):
		neighbours = self.nodes
		new_chain = None
		max_length = len(self.chain)
		for node in neighbours:
			try:
				response = requests.get(f'http://{node}/chain')
				if response.status_code == 200:
					length = response.json()['length']
					chain = response.json()['chain']
					if length > max_length and self.valid_chain(chain):
						max_length = length
						new_chain = chain
			except requests.exceptions.ConnectionError:
				continue
		if new_chain:
			self.chain = new_chain
			return True
		return False

	def new_block(self, proof, previous_hash):
		block = Block(
			index=len(self.chain) + 1,
			transactions=self.current_transactions,
			proof=proof,
			previous_hash=previous_hash or self.hash(self.chain[-1]),
		)
		self.current_transactions = []
		self.chain.append(block.to_dict())
		return block.to_dict()

	def new_transaction(self, sender, recipient, amount):
		transaction = Transaction(sender, recipient, amount)
		self.current_transactions.append(transaction.to_dict())
		return self.last_block['index'] + 1

	@property
	def last_block(self):
		return self.chain[-1]

	def hash(self, block):
		block_string = json.dumps(block, sort_keys=True)
		return self.crypto.hash(block_string)

	def proof_of_work(self, last_block):
		last_proof = last_block['proof']
		previous_hash = self.hash(last_block)
		proof = 0
		while self.valid_proof(last_proof, proof, previous_hash) is False:
			proof += 1
		return proof

	def valid_proof(self, last_proof, proof, previous_hash):
		guess = f'{last_proof}{proof}{previous_hash}'
		guess_hash = self.crypto.hash(guess)
		return guess_hash[:4] == "0000"
