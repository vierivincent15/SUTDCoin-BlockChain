from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from utils.miner import Miner
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process
import requests
import time


miners = {
    'miner1': 'http://127.0.0.1:5011',
    'miner2': 'http://127.0.0.1:5012'
}


def start_mine(miner):
    response = requests.post(
        miners[miner]+'/init',
        data={'wait': 'no'}
    )


def send_transaction(sender, receiver, amount):
    response = requests.post(
        sender+'/send',
        data={
            'receiver': receiver,
            'amount': amount
        }
    )

    if (response.status_code == 200):
        print(f"Transaction to {receiver} was successful")
    elif (response.status_code == 500):
        print("Not enough coins")
    else:
        print(f"Transaction to {receiver} was unsuccessful :(((")


if __name__ == "__main__":
    for miner in miners.keys():
        job = Process(target=start_mine, args=(miner, ))
        job.start()
