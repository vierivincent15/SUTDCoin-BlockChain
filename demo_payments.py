from utils.blockchain import Blockchain
from utils.transaction import Transaction
from utils.miner import Miner
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

miner_server = 'http://127.0.0.1:5000'
client1 = 'http://127.0.0.1:5001'
miner1 = 'http://127.0.0.1:5011'


blockchain = Blockchain()

response = requests.post(
    client1+'/create',
    data={}
)
if(response.status_code == 201):
    print("Client 1 created")
else:
    print("Client 1 already created")

response = requests.post(
    miner1+'/init',
    data={}
)
if(response.status_code == 201):
    block = response.content
    print(block)
else:
    print("Error")

print(blockchain.blockchains)
