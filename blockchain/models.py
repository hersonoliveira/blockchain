import hashlib
import json
from time import time
import requests


class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous block
        :return: <dict> New block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transation
        """

        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> Block
        :return: <str>
        """

        # Dictionary must be ordered to avoid inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Proof of Work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False if not.
        """

        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f"{last_block}")
            print(f"{block}")
            print("\n----------\n")

            # Check that the hash of the block is correct
            if block["previous_hash"] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False
            
            last_block = block
            current_index += 1

        return True
    
    def resolve_conflicts(self):
        """
        This is our Consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        # Replace our chain if we discovered  a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False
