# implement block class here
import hashlib
import json

from ecdsa import SigningKey
from utils.merkletree import MerkleTree
from utils.transaction import Transaction
import time
import uuid


class Block:
    def __init__(self, transactions=None, prev_header=None, header=None):
        self.transactions = transactions
        if header is None:
            self.header = {
                'prev_header': prev_header,
                'tree_root': MerkleTree(transactions).get_root(),
                'timestamp': int(time.time()),
                'nonce': uuid.uuid4().hex
            }
        else:
            self.header = header

    @classmethod
    def new(cls, transactions, prev_header, header=None):
        block = cls(transactions, prev_header, header)
        return block

    def serialize(self, header_mode=False):
        data = {}
        if not header_mode:
            data['transactions'] = [transaction.serialize()
                                    for transaction in self.transactions]
        data['header'] = {
            'prev_header': self.header['prev_header'].hex(),
            'tree_root': self.header['tree_root'].hex(),
            'timestamp': self.header['timestamp'],
            'nonce': self.header['nonce']
        }
        return json.dumps(data)

    def hash_header(self):
        return hashlib.sha256(self.serialize(True).encode()).digest()

    @classmethod
    def deserialize(cls, json_string):
        data = json.loads(json_string)
        transactions = [Transaction.deserialize(
            transaction) for transaction in data['transactions']]
        header = data['header']
        header = {
            'prev_header': bytes.fromhex(header['prev_header']),
            'tree_root': bytes.fromhex(header['tree_root']),
            'timestamp': header['timestamp'],
            'nonce': header['nonce']
        }
        return cls(transactions, None, header)

    def validate(self):
        boolean = True
        for i in range(1, len(self.transactions)):
            transaction = self.transactions[i]
            boolean = transaction.validate()
            if not boolean:
                return boolean
        return self.header['tree_root'] == MerkleTree(self.transactions).get_root()


# to test implementation
if __name__ == "__main__":

    sign_key = SigningKey.generate()
    public_key = sign_key.get_verifying_key()

    transactions = [Transaction.new(None, public_key, 100, "Reward", None)]

    Block.new(transactions, b'aaa')

    # transactions = []
    # amount = 1000
    # comment = "COOL!"
    # for i in range(4):
    #     sign_key_1 = SigningKey.generate()
    #     sender = sign_key_1.get_verifying_key()

    #     sign_key_2 = SigningKey.generate()
    #     receiver = sign_key_2.get_verifying_key()

    #     Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)
    #     transactions.append(Tx)

    # TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    # block1 = Block.new(transactions, b'genesis block')
    # print(block1.header)
