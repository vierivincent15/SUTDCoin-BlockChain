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


class Blockchain:

    # target = b"\x00\x00\x0f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

    def __init__(self):
        self.blockchains = [[]]
        self.true_blockchain = 0
        self.tx_pool = []
        self.tids = set()
        self.balance = [{}]
        self.true_prev_header = b'genesis block'

    def add_block(self, block, resolve=True):
        idxs = self.trace_prev_header(block.header["prev_header"])
        if self.validate_block(block, idxs):
            bc_idx, b_idx = 0, -1
            if idxs != -1:
                bc_idx, b_idx = idxs
            # print(idxs,len(self.blockchains[bc_idx]))
            if (b_idx == len(self.blockchains[bc_idx]) - 1) or b_idx == -1:
                self.blockchains[bc_idx].append(block)
            else:
                temp_blockchain = self.blockchains[bc_idx][:b_idx+1].copy()
                temp_blockchain.append(block)
                self.blockchains.append(temp_blockchain)
                print(1)

            self.remove_transaction(block)
            self.add_tids(block)
            if (b_idx == len(self.blockchains[bc_idx]) - 1) or b_idx == -1:
                self.balance[bc_idx] = self.update_balance(
                    self.balance[bc_idx], block)
            else:
                new_balance = self.aggregate_balance(bc_idx, b_idx)
                new_balance = self.update_balance(new_balance, block)
                self.balance.append(new_balance)

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
        # I need the blockchain index as well as the block index for this function
        # If block header is given, the index will be recomputed twice

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
        max_index = chain_length.index(max(chain_length))

        max_chain = self.blockchains[max_index]

        self.true_blockchain = max_index
        self.true_prev_header = max_chain[-1].hash_header()

    # def resolve_fork_old(self):
    #     if len(self.blockchains) > 1:
    #         max_length = max([len(blockchain)
    #                           for blockchain in self.blockchains])
    #         new = []
    #         new_balance = {}
    #         counter = 0
    #         for i in range(len(self.blockchains)):
    #             if len(self.blockchains[i]) == max_length:
    #                 new.append(self.blockchains[i])
    #                 new_balance[counter] = self.balance[i]
    #                 counter += 1

    #         self.blockchains = new
    #         self.balance = new_balance

    def trace_prev_header(self, prev_header):
        for i in range(len(self.blockchains)):
            for j in range(len(self.blockchains[i])):
                if self.blockchains[i][j].hash_header() == prev_header:
                    return (i, j)

        # meaning prev_header not found in chain
        return -1

    def get_prev_header(self, bc_idx, b_idx):
        return self.blockchains[bc_idx][b_idx].hash_header()

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
