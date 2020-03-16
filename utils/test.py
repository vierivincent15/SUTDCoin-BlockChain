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

# t1 = time.time()
print("mining")
block = miner1.mine(b'genesis block')
print("done")
miner1.transact(miner2.public_key, 105)
miner1.transact(miner2.public_key, 30)

print(blockchain.tx_pool)

print("mining")
miner2.mine()
print("done")

print(blockchain.blockchains)
print(blockchain.tx_pool)
print(blockchain.tids)
print(blockchain.balance)

# print(time.time()-t1)
# print(blockchain.blockchains[0][0].transactions)
# print(blockchain.balance)
# print(blockchain.tids)
# print(blockchain.tx_pool)