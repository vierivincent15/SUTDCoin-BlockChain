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
import json


class Miner:
    def __init__(self, blockchain, public_key, sign_key):
        self.id = uuid.uuid4().hex
        self.blockchain = blockchain
        self.public_key = public_key
        self.reward = 100
        self.sign_key = sign_key

    def send_transaction(self, receiver, amount, comment="COOL!"):
        Tx = Transaction.new(self.public_key, receiver,
                             amount, comment, self.sign_key)
        self.blockchain.add_transaction(Tx)
        return Tx

    def add_transaction(self, transaction):
        self.blockchain.add_transaction(transaction)

    def get_transaction_proof(self, transaction):
        proof_with_root = self.blockchain.get_transaction_proof(transaction)
        return self.serialize_proof(proof_with_root)

    def serialize_proof(self, proof_with_root):
        serialization = {}
        serialization['proof_idx'] = proof_with_root[0][0]
        serialization['proof'] = [proof.hex()
                                  for proof in proof_with_root[0][1]]
        serialization['root'] = proof_with_root[1].hex()
        return json.dumps(serialization)

    def mine(self, need_transaction=True):
        global TARGET
        pow_val = TARGET
        reward = Transaction.new(
            None, self.public_key, self.reward, "Reward", None)
        t1 = time.time()
        printhelper = True

        while True:
            # print(pow_val)
            if pow_val < TARGET:
                try:
                    self.blockchain.add_block(block)
                    print(time.time()-t1)
                    return block
                except ValueError:
                    raise
            if need_transaction:
                if len(self.blockchain.tx_pool) < 1 and len(self.blockchain.blockchains[0]) > 0:
                    if printhelper:
                        print("Waiting for more transactions...")
                        printhelper = False
                    continue

            prev_header = self.blockchain.prev_header
            transactions = self.blockchain.tx_pool.copy()
            transactions.insert(0, reward)
            block = Block.new(transactions, prev_header)
            pow_val = block.hash_header()

    def mine_malicious(self, prev_header=None, bc_idx=-1, b_idx=-1, continuous=True, need_transaction=True):
        global TARGET
        pow_val = TARGET
        t1 = time.time()

        reward = Transaction.new(
            None, self.public_key, self.reward, "Reward", None)

        printhelper = True

        if not continuous:
            if prev_header is None:
                prev_header = self.blockchain.get_prev_header(bc_idx, b_idx)
            
            if need_transaction:
                while len(self.blockchain.tx_pool) < 1 and len(self.blockchain.blockchains[0]) > 0:
                    if printhelper:
                        print("Waiting for more transactions...")
                        printhelper = False
                    continue
            
            transactions = self.blockchain.tx_pool.copy()

            transactions.insert(0, reward)

            while pow_val >= TARGET:
                block = Block.new(transactions, prev_header)
                pow_val = block.hash_header()

            try:
                self.blockchain.add_block(block)
                return block
            except ValueError:
                raise

        else:
            if prev_header is not None:
                raise ValueError(
                    "continuous cannot be True if prev_header is used!")
            while True:
                # print(pow_val)
                if pow_val < TARGET:
                    try:
                        self.blockchain.add_block(block)
                        print(time.time()-t1)
                        return block
                    except ValueError:
                        raise

                if need_transaction:
                    if len(self.blockchain.tx_pool) < 1 and len(self.blockchain.blockchains[0]) > 0:
                        if printhelper:
                            print("Waiting for more transactions...")
                            printhelper = False
                        continue

                
                prev_header = self.blockchain.get_prev_header(bc_idx, b_idx)
                    
                transactions = self.blockchain.tx_pool.copy()
                transactions.insert(0, reward)
                block = Block.new(transactions, prev_header)
                pow_val = block.hash_header()


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
