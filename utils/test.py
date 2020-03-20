from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from blockchain import Blockchain
from miner import Miner
import time
from transaction import Transaction

blockchain = Blockchain()

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner1 = Miner(blockchain, public_key, sign_key)
print(len(blockchain.blockchains[0]))
print("mining")
block = miner1.mine()
print("done")

print(blockchain)


# sign_key = SigningKey.generate()
# public_key = sign_key.get_verifying_key()

# miner2 = Miner(blockchain, public_key, sign_key)


# miner1.send_transaction(miner2.public_key, 10)
# miner1.send_transaction(miner2.public_key, 30)
# miner1.send_transaction(miner2.public_key, 30)


# print("mining")
# reward = miner2.mine()
# print("done")

# print(miner2.get_transaction_proof(reward))
# print(miner2.deserialize_proof(miner2.get_transaction_proof(reward)))

# print(blockchain)

# print(blockchain.blockchains)
# print(blockchain.tx_pool)
# print(blockchain.tids)
# print(blockchain.balance)
