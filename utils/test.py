from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from blockchain import Blockchain
from miner import Miner

blockchain = Blockchain()

print(blockchain.blockchains)

sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()

miner = Miner(blockchain, sign_key, public_key)

block = miner.mine(b'genesis block')

blockchain.add_block(block)

print(blockchain.blockchains)