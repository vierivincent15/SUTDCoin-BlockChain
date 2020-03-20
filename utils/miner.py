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

    def deserialize_proof(self, serialization):
        serialization = json.loads(serialization)
        proof_idx = serialization['proof_idx']
        proof = [bytes.fromhex(proof) for proof in serialization['proof']]
        root = bytes.fromhex(serialization['root'])
        return ([proof_idx, proof], root)

    def mine(self):
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

            if len(self.blockchain.tx_pool) < 1 and len(self.blockchain.blockchains[0]) > 0:
                if printhelper:
                    print("Waiting for more transactions...")
                    printhelper = False
                continue

            prev_header = self.blockchain.true_prev_header
            transactions = self.blockchain.tx_pool.copy()
            transactions.insert(0, reward)
            block = Block.new(transactions, prev_header)
            pow_val = block.hash_header()

    def mine_malicious(self, prev_header=None, bc_idx=-1, b_idx=-1, continuous=False):
        global TARGET
        pow_val = TARGET

        reward = Transaction.new(
            None, self.public_key, self.reward, "Reward", None)
        
        printhelper = True

        if prev_header is not None:
            if continuous:
                raise ValueError("continuous cannot be True if prev_header is used!")
            else:
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
            while True:
                # print(pow_val)
                if pow_val < TARGET:
                    try:
                        self.blockchain.add_block(block)
                        print(time.time()-t1)
                        return block
                    except ValueError:
                        raise
                
                if len(self.blockchain.tx_pool) < 1 and len(self.blockchain.blockchains[0]) > 0:
                    if printhelper:
                        print("Waiting for more transactions...")
                        printhelper = False
                    continue

                if bc_idx < len(self.blockchain.blockchains):
                    if b_idx < len(self.blockchain.blockchains[bc_idx]):
                        prev_header = self.blockchain.get_prev_header(
                            bc_idx, b_idx)
                    else:
                        raise IndexError
                else:
                    raise IndexError

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
