from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from utils.miner import Miner
from network_protocol import get_public_key
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process
import requests
import time
import json


miners = {
    'miner1': 'http://127.0.0.1:5011',
    'miner2': 'http://127.0.0.1:5012'
}

selfish_pool = {'selfish1': 'http://127.0.0.1:5021'}


def start_mine(miner):
    response = requests.post(
        miners[miner]+'/init',
        data={'wait': 'selfish'}
    )


def get_blockchain_balance():
    global miners

    print("\nGetting blockchain balance...")
    response = requests.get(miners['miner1']+'/get_balance')
    serialization = json.loads(response.content)
    for uuid, balance in serialization.items():
        print(f"{uuid}: {balance}")
    print()


if __name__ == "__main__":
    for miner in miners.keys():
        job = Process(target=start_mine, args=(miner, ))
        job.start()

