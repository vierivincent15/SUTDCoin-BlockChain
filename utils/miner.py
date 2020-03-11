# implement miner class here
from merkletree import *
from transaction import *
from block import *
import time
import uuid


class Miner:
    def __init__(self, public_key):
        self.id = uuid.uuid4().hex
        self.ip = None
        self.public_key = public_key
        self.reward = 100
        
    #should check if prev_header in chain
    def mine(self, transactions, prev_header):
        global TARGET
        pow_val = TARGET
        
#         for transaction in transactions:
#             transaction.validate()

#         reward = Transaction.new(None, receiver = self.public_key, self.reward, "Reward")
#         transactions.insert(0,reward)
        
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
        
        Tx = Transaction.new(sender, receiver, amount, comment)
        Tx.sign(sign_key_1)
        transactions.append(Tx)

    TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    miner = Miner('aa')
    t1 = time.time()
    miner.mine(transactions, b'genesis block')
    print(time.time()-t1)
    pass