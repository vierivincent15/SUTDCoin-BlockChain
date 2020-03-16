# implement blockchain class here
import hashlib
from json import dumps, loads

import block
from transaction import Transaction
from block import Block


class Blockchain():

    # target = b"\x00\x00\x0f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    target = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

    def __init__(self):
        self.blockchains = [[]]
        self.tx_pool = []
        self.tids = set()
        self.balance = {}

    def add_block(self, block):
        idxs = self.trace_prev_header(block.header["prev_header"])
        if self.validate_block(block, idxs):
            bc_idx, b_idx = idxs
            if (b_idx != len(self.blockchains[bc_idx]) - 1):
                temp_blockchain = self.blockchains[bc_idx][:b_idx+1].copy()
                temp_blockchain.append(block)
                self.blockchains.append(temp_blockchain)
            else:
                self.blockchains[bc_idx].append(block)

            self.remove_transaction(block)
            self.add_tids(block)
            if (idxs[1] != len(self.blockchains[idxs[0]]) - 1):
                new_balance = self.aggregate_balance(bc_idx, b_idx)
                new_balance = self.update_balance(new_balance, block)
                self.balance[bc_idx] = new_balance
            else:
                self.balance[bc_idx] = self.update_balance(self.balance[bc_idx], block)
        else:
            raise ValueError("Could Not Add Block")

    def validate_block(self, block, idxs):
        # Check if it satisfy Block class validation
        if not block.validate():
            return False
        
        # Check if the hash of the header is less than the assigned target
        header = block.serialize_header()
        hasher = hashlib.sha256()
        hasher.update(header.encode())
        if not hasher.digest() < Blockchain.target:
            return False

        # check genesis block then don't need to check for prev header
        if not any(self.blockchains):
            return True

        # check for prev_header existence
        if idxs == -1:
            return False

        # check for non-negative balance
        temp_balance = self.aggregate_balance(idxs[0], idxs[1])
        temp_balance = self.update_balance(temp_balance, block)
        for val in temp_balance.values():
            if val < 0:
                return False

        return True


    def validate(self):
        for blockchain in self.blockchains:
            for block in blockchain:
                if not block.validate():
                    return False
        return True
    
    def add_transaction(self, transaction):
        if transaction.validate() and (transaction.tid not in self.tids) and (transaction.tid not in self.tx_pool):
            self.tx_pool.append(transaction)

    # to add in to add block later
    def remove_transaction(self, block):
        for transaction in block.transactions:
            try:
                self.tx_pool.remove(transaction)
            except ValueError:
                continue

    # to add in to add block later
    def add_tids(self, block):
        for transaction in block.transactions:
            self.tids.add(transaction.tid)

    # to add in to add block later
    def update_balance(self, balance, block):
        temp_dict = balance.copy()
        for transaction in block.transactions:
            temp_dict[transaction.sender] -= transaction.amount
            if transaction.receiver not in temp_dict:
                temp_dict[transaction.receiver] = transaction.amount
            else:
                temp_dict[transaction.receiver] += transaction.amount
        
        return temp_dict
        

    def aggregate_balance(self, blockchain_idx, block_idx):
        # I need the blockchain index as well as the block index for this function
        # If block header is given, the index will be recomputed twice

        temp_dict = {}
        for transaction in self.blockchains[blockchain_idx][:block_idx+1]:
            temp_dict[transaction.sender] -= transaction.amount
            if transaction.receiver not in temp_dict:
                temp_dict[transaction.receiver] = transaction.amount
            else:
                temp_dict[transaction.receiver] += transaction.amount
        
        return temp_dict

    def resolve_fork(self):
        if len(self.blockchains) > 1:
            max_length = max([len(blockchain) for blockchain in self.blockchains])
            new = []
            for blockchain in self.blockchains:
                if len(blockchain) == max_length:
                    new.append(blockchain)

            self.blockchains = new

    def trace_prev_header(self,prev_header):
        for i in range (len(self.blockchains)):
            for j in range (len(self.blockchains[i])):
                if self.blockchains[i][j].hash_header() == prev_header:
                    return (i,j)
                    
        #meaning prev_header not found in chain
        return -1

# to test implementation
if __name__ == "__main__":
    pass