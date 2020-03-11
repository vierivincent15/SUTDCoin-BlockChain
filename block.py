# implement block class here

from merkletree import *
from transaction import *
import time
import uuid

class Block:
    def __init__(self,transactions=None, prev_header=None, header=None):
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
    def new(cls,transactions, prev_header, header=None):
        block = cls(transactions, prev_header, header)
        return block
        
    def serialize(self,header_mode=False):
        data = {}
        if not header_mode:
            data['transactions'] = [transaction.serialize() for transaction in transactions]
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
        transactions = [Transaction.deserialize(transaction) for transaction in data['transactions']]
        header = data['header']
        header = {
            'prev_header': bytes.fromhex(header['prev_header']),
            'tree_root': bytes.fromhex(header['tree_root']),
            'timestamp': header['timestamp'],
            'nonce': header['nonce']
        }
        return cls(transactions, None, header)
    
    def validate(self):
        global TARGET
        boolean = True
        for transaction in self.transactions:
            boolean = transaction.validate()
            if not boolean:
                return boolean
        return self.header['tree_root'] == MerkleTree(transactions).get_root()

# to test implementation
if __name__ == "__main__":
    transactions = []
    amount = 1000
    comment = "COOL!"
    for i in range(4):
        sign_key_1 = SigningKey.generate()
        sender = sign_key_1.get_verifying_key()
        
        sign_key_2 = SigningKey.generate()
        receiver = sign_key_2.get_verifying_key()
        
        Tx = Transaction.new(sender, receiver, amount, comment)
        Tx.sign(sign_key_1)
        transactions.append(Tx)

    TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    block1 = Block.new(transactions,b'genesis block')
    print(block1.header)
    pass