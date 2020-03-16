# implement miner class here
from merkletree import MerkleTree
from transaction import Transaction
from block import Block
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from blockchain import Blockchain
import time
import uuid


class Miner:
    def __init__(self, blockchain, public_key, sign_key):
        self.id = uuid.uuid4().hex
        self.blockchain = blockchain
        self.ip = None
        self.public_key = public_key
        self.reward = 100
        self.sign_key = sign_key
    
    def transact(self, receiver, amount, comment="COOL!"):
        return Transaction.new(self.public_key, receiver, amount, comment, self.sign_key)

    #should check if prev_header in chain
    def mine(self, transactions, prev_header):
        global TARGET
        pow_val = TARGET
        
#         for transaction in transactions:
#             transaction.validate()

        reward = Transaction.new(None, self.public_key, self.reward, "Reward", None)
        transactions.insert(0,reward)
        
        while pow_val >= TARGET:
            block = Block.new(transactions, prev_header)
            pow_val = block.hash_header()
        return block


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
        
        Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)
        transactions.append(Tx)

    TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    blockchain = Blockchain()

    sign_key = SigningKey.generate()
    public_key = sign_key_1.get_verifying_key()

    print(type(blockchain))

    miner = Miner(blockchain, public_key, sign_key)
    t1 = time.time()
    miner.mine(transactions, b'genesis block')
    print(time.time()-t1)