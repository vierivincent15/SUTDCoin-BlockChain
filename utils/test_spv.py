from spvclient import SPVClient
from miner import Miner
from blockchain import Blockchain
from ecdsa import SigningKey, VerifyingKey, BadSignatureError


print("Testing SPVClient")
print("-" * 100)
client1 = SPVClient.new('1')
client2 = SPVClient.new('2')

blockchain = Blockchain()

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner1 = Miner(blockchain, public_key, sign_key)

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner2 = Miner(blockchain, public_key, sign_key)

print("-" * 100)
print("mining")
block, status = miner1.mine(b'genesis block')
print("done")

miner1.send_transaction(client1.public_key, 50)
miner1.send_transaction(client2.public_key, 20)

print(client2.public_key)
Tx = client1.send_transaction(client2.public_key, 40)
blockchain.add_transaction(Tx)

print("-" * 100)
print("mining")
miner2.mine()
print("done")

print("blockchain")
print(blockchain.blockchains)

print("txpool")
print(blockchain.tx_pool)

print("tids")
print(blockchain.tids)

print("balance")
print(blockchain.balance)