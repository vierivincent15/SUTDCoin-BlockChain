try:
    from transaction import Transaction
    from block import Block
    from merkletree import MerkleTree
    from config import TARGET
except:
    from utils.transaction import Transaction
    from utils.block import Block
    from utils.merkletree import MerkleTree
    from utils.config import TARGET
from json import dumps, loads
import hashlib
import random

class Blockchain:

    def __init__(self):
        self.blockchains = [[]]
        self.true_blockchain = 0
        self.tx_pool = []
        self.tids = set()
        self.balance = {self.true_blockchain: {}}
        self.prev_header = [b'genesis block']

    def add_block(self, block, resolve=True, print_idx=False):
        idxs = self.trace_prev_header(block.header["prev_header"])
        if self.validate_block(block, idxs):
            bc_idx, b_idx = 0, -1
            if idxs != -1:
                bc_idx, b_idx = idxs
            if print_idx:
                print("Block found on:")
                print("Chain {}".format(bc_idx))
                print("Block {}".format(b_idx+1))
            # print(idxs,len(self.blockchains[bc_idx]))
            if (b_idx == len(self.blockchains[bc_idx]) - 1) or b_idx == -1:
                self.blockchains[bc_idx].append(block)
            else:
                temp_blockchain = self.blockchains[bc_idx][:b_idx+1].copy()
                temp_blockchain.append(block)
                self.blockchains.append(temp_blockchain)

            self.remove_transaction(block)
            self.add_tids(block)
            if (b_idx == len(self.blockchains[bc_idx]) - 1) or b_idx == -1:
                self.balance[bc_idx] = self.update_balance(
                    self.balance[bc_idx], block)
            else:
                # print(bc_idx, b_idx)
                new_balance = self.aggregate_balance(bc_idx, b_idx)
                new_balance = self.update_balance(new_balance, block)
                # self.balance.append(new_balance)
                self.balance[bc_idx] = new_balance 

            if resolve:
                self.resolve_fork()
        else:
            raise ValueError("Could Not Add Block")

    def validate_block(self, block, idxs):
        global TARGET
        # Check if it satisfy Block class validation
        if not block.validate():
            return False

        # Check if the hash of the header is less than the assigned target
        header_hash = block.hash_header()
        if not header_hash < TARGET:
            return False

        # check genesis block then don't need to check for prev header
        if not any(self.blockchains):
            return True

        # check for prev_header existence
        if idxs == -1:
            print("prev_header does not exist")
            # print(block.hash_header())
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
        if transaction.validate() and (transaction.tid not in self.tids) and (transaction not in self.tx_pool):
            if transaction.sender is not None:
                sender = transaction.sender.to_string().hex()
                if self.balance[self.true_blockchain][sender] > int(transaction.amount):
                    self.tx_pool.append(transaction)
                else:
                    raise ValueError("Could Not Add Transaction")
            else:
                self.tx_pool.append(transaction)
        else:
            raise ValueError("Could Not Add Transaction")

    def remove_transaction(self, block):
        for transaction in block.transactions:
            try:
                self.tx_pool.remove(transaction)
            except ValueError:
                continue

    def add_tids(self, block):
        for transaction in block.transactions:
            self.tids.add(transaction.tid)

    def update_balance(self, balance, block):
        temp_dict = balance.copy()
        for transaction in block.transactions:
            if transaction.sender is not None:
                sender = transaction.sender.to_string().hex()
                temp_dict[sender] -= int(transaction.amount)
            receiver = transaction.receiver.to_string().hex()
            if receiver not in temp_dict:
                temp_dict[receiver] = int(transaction.amount)
            else:
                temp_dict[receiver] += int(transaction.amount)

        return temp_dict

    def aggregate_balance(self, blockchain_idx, block_idx):

        temp_dict = {}
        for block in self.blockchains[blockchain_idx][:block_idx+1]:
            for transaction in block.transactions:
                if transaction.sender is not None:
                    sender = transaction.sender.to_string().hex()
                    temp_dict[sender] -= int(transaction.amount)
                receiver = transaction.receiver.to_string().hex()
                if receiver not in temp_dict:
                    temp_dict[receiver] = int(transaction.amount)
                else:
                    temp_dict[receiver] += int(transaction.amount)

        return temp_dict

    def resolve_fork(self):
        if len(self.blockchains[0]) == 0:
            return b'genesis block'
        chain_length = [len(chain) for chain in self.blockchains]
        indices = [idx for idx, val in enumerate(chain_length) if val == max(chain_length)]
        max_index = random.choice(indices)

        # max_chain = self.blockchains[max_index]

        self.true_blockchain = max_index

        prev_header = []
        for chain in self.blockchains:
            prev_header.append(chain[-1].hash_header())
        self.prev_header = prev_header.copy()

    def trace_prev_header(self, prev_header):
        for i in range(len(self.blockchains)):
            for j in range(len(self.blockchains[i])):
                if self.blockchains[i][j].hash_header() == prev_header:
                    return (i, j)

        # meaning prev_header not found in chain
        return -1

    def get_prev_header(self, bc_idx, b_idx):
        if bc_idx < len(self.blockchains):
            if b_idx < len(self.blockchains[bc_idx]):
                return self.blockchains[bc_idx][b_idx].hash_header()
            else:
                raise IndexError
        else:
            raise IndexError

    def get_transaction_proof(self, transaction):
        for block in self.blockchains[self.true_blockchain]:
            if transaction in block.transactions:
                mt = MerkleTree(block.transactions)
                return (mt.get_proof(transaction), mt.get_root())



    def __str__(self):
        out = ""
        for i in range(len(self.blockchains)):
            chain = [str(block.hash_header()) for block in self.blockchains[i]]
            out += "Chain" + str(i+1) + ": \n"
            out += '\n'.join(chain)
            out += '\n'

        out += "\nTrue balance:\n"

        balance = self.balance[self.true_blockchain]
        for user in balance:
            out += user + ": " + str(balance[user])

        return out


# to test implementation
if __name__ == "__main__":
    pass
