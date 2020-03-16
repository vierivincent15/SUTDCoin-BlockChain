from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from blockchain import Blockchain
from miner import Miner
import time
from transaction import Transaction

blockchain = Blockchain()

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner1 = Miner(blockchain, public_key, sign_key)

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner2 = Miner(blockchain, public_key, sign_key)

t1 = time.time()
block = miner1.mine(b'genesis block')
blockchain.add_block(block)

miner1.transact(miner2, 20)


# print(time.time()-t1)
# print(blockchain.blockchains[0][0].transactions)
# print(blockchain.balance)
# print(blockchain.tids)
# print(blockchain.tx_pool)