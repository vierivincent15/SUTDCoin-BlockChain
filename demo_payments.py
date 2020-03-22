from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from utils.miner import Miner
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process
import requests
import json
import time


clients = {
    'client1': 'http://127.0.0.1:5001',
    'client2': 'http://127.0.0.1:5002'
}
miners = {
    'miner1': 'http://127.0.0.1:5011',
    'miner2': 'http://127.0.0.1:5012'
}


def start_mine(miner):
    response = requests.post(
        miners[miner]+'/init',
        data={'wait': 'yes'}
    )


def get_balance(receiver, ip):
    response = requests.get(ip+'/get_balance')
    return int(response.content)


def get_blockchain_balance():
    global miners

    print("\nGetting blockchain balance...")
    response = requests.get(miners['miner1']+'/get_balance')
    serialization = json.loads(response.content)
    for uuid, balance in serialization.items():
        print(f"{uuid}: {balance}")
    print()


def send_transaction(sender, ip, receiver, ip2, amount, i):
    print(f"Attempting transaction {i} from {sender} to {receiver}")
    response = requests.post(
        ip+'/send',
        data={
            'receiver': receiver,
            'amount': amount
        }
    )

    if (response.status_code == 200):
        print(f"Transaction {i} from {sender} to {receiver} was successful.")
        print(f"{receiver} has {get_balance(receiver, ip2)} balance.")
    elif (response.status_code == 500):
        print(
            f"Transaction {i} from {sender} to {receiver} failed due to insufficient coins.")
    else:
        print(
            f"Transaction {i} from {sender} to {receiver} was unsuccessful :(((")


def resend_duplicate_transaction():
    print("\nAttempting to get duplicate transaction...")
    response = requests.get(miners['miner1']+'/get_random_tx')
    tx = response.content
    print("Attempting to resend the duplicate transaction...")
    response = requests.post(
        miners['miner1']+'/resend_duplicate',
        data={
            'tx': tx,
        }
    )
    if response.status_code == 500:
        print("Adding duplicate transaction failed")


if __name__ == "__main__":
    for miner in miners.keys():
        job = Process(target=start_mine, args=(miner, ))
        job.start()

    for i in range(1, 4):
        for miner, ip in miners.items():
            time.sleep(8)
            get_blockchain_balance()
            receiver = 'client1'
            ip2 = clients[receiver]
            job = Process(target=send_transaction,
                          args=(miner, ip, receiver, ip2, 30, i, ))
            job.start()

    for i in range(1, 4):
        time.sleep(8)
        get_blockchain_balance()
        job = Process(target=send_transaction,
                      args=('client1', clients['client1'], 'client2', clients['client2'], 20, i, ))
        job.start()

    time.sleep(10)
    get_blockchain_balance()

    time.sleep(10)
    resend_duplicate_transaction()
