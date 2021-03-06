try:
    from merkletree import MerkleTree
    from transaction import Transaction
except:
    from utils.merkletree import MerkleTree
    from utils.transaction import Transaction
from ecdsa import SigningKey
import hashlib
import json
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
    def deserialize(cls, json_string, header_mode=False):
        data = json.loads(json_string)

        header = data['header']
        header = {
            'prev_header': bytes.fromhex(header['prev_header']),
            'tree_root': bytes.fromhex(header['tree_root']),
            'timestamp': header['timestamp'],
            'nonce': header['nonce']
        }

        if header_mode:
            return header

        transactions = [Transaction.deserialize(
            transaction) for transaction in data['transactions']]
        
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
    pass
