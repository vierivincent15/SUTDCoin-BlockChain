# implement blockchain class here
import hashlib
from json import dumps, loads

import block
from transaction import Transaction
from block import Block


class Blockchain():

    # target = b"\x00\x00\x0f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    target = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    difficulty = 2

    def __init__(self):
        self.blockchain = []
        self.chain_length = 0

    def add_block(self, block):
        if self.validate_block(block):
            self.blockchain.append(block)
            self.chain_length += 1
        else:
            raise ValueError("Could Not Add Block")

    def validate_block(self, block):
        # Check if it satisfy Block class validation

        # check genesis block then don't need to check for prev header
        if len(self.blockchain) == 0:
            return True

        # check if previous header
        prev_hash = self.blockchain[-1]
        if prev_hash != block.hash_header():
            return False 

        # blockchain is not valid
        if not block.validate():
            return False
        # Check if the stored hash of previous header is the same as the actual hash of previous header in the blockchain
        # if not self.blockchain[self.chain_length-1].serialize_header() == block.header["hash_prev_header"]:
        #     return False

        # Check if the hash of the header is less than the assigned target
        header = block.serialize_header()
        hasher = hashlib.sha256()
        hasher.update(header.encode())
        if not hasher.digest() < Blockchain.target:
            return False
        return True

    def validate(self):
        for block in self.blockchain:
            if not block.validate():
                return False
        return True



# to test implementation
if __name__ == "__main__":
    pass