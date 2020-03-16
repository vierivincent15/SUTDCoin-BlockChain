try:
    from merkletree import MerkleTree
    from transaction import Transaction
    from block import Block
    from blockchain import Blockchain
    from config import TARGET
except:
    from utils.merkletree import MerkleTree
    from utils.transaction import Transaction
    from utils.block import Block
    from utils.blockchain import Blockchain
    from utils.config import TARGET
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
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
        Tx = Transaction.new(self.public_key, receiver,
                             amount, comment, self.sign_key)
        self.blockchain.add_transaction(Tx)
        return Tx

    # should check if prev_header in chain
    def mine(self, prev_header):
        global TARGET
        pow_val = TARGET

        transactions = self.blockchain.tx_pool.copy()
#         for transaction in transactions:
#             transaction.validate()
        reward = Transaction.new(
            None, self.public_key, self.reward, "Reward", None)
        transactions.insert(0, reward)

        while pow_val >= TARGET:
            block = Block.new(transactions, prev_header)
            pow_val = block.hash_header()

        try:
            self.blockchain.add_block(block)
            status = True
        except ValueError:
            status = False
        return block, status


# to test implementation
if __name__ == "__main__":
    TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    blockchain = Blockchain()

    print(blockchain.blockchains)

    sign_key = SigningKey.generate()
    public_key = sign_key.get_verifying_key()

    miner = Miner(blockchain, sign_key, public_key)
    t1 = time.time()
    block = miner.mine(b'genesis block')

    blockchain.add_block(block)
    print(time.time()-t1)
    print(blockchain.blockchains)

    # transactions = []
    # amount = 1000
    # comment = "COOL!"
    # blockchain = Blockchain()
    # for i in range(4):
    #     sign_key_1 = SigningKey.generate()
    #     sender = sign_key_1.get_verifying_key()

    #     sign_key_2 = SigningKey.generate()
    #     receiver = sign_key_2.get_verifying_key()

    #     Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)
    #     blockchain.add_transaction(Tx)

    # TARGET = b'\x00\x00\xff\xff' + b'\xff'*28

    # sign_key = SigningKey.generate()
    # public_key = sign_key_1.get_verifying_key()

    # print(type(blockchain))

    # print("Chain:")
    # print(blockchain.blockchains)

    # print("txpool")
    # print(blockchain.tx_pool)

    # print("tids")
    # print(blockchain.tids)

    # miner = Miner(blockchain, public_key, sign_key)
    # t1 = time.time()
    # blockchain.add_block(miner.mine(b'genesis block'))
    # print(time.time()-t1)

    # print("Chain:")
    # print(blockchain.blockchains)

    # print("txpool")
    # print(blockchain.tx_pool)

    # print("tids")
    # print(blockchain.tids)
