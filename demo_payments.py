from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from utils.miner import Miner
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process
import requests
import time

miner_server = 'http://127.0.0.1:5000'
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

    # response = requests.post(
    #     miners['miner1']+'/send',
    #     data={
    #         'receiver': 'client1',
    #         'amount': 100
    #     }
    # )


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

    time.sleep(10)
    for i in range(1, 4):
        print(f"Sending transaction {i} from miner to client1")
        for miner in miners.values():
            job = Process(target=send_transaction,
                          args=(miner, 'client1', 30, ))
            job.start()
        time.sleep(15)

    for i in range(1, 4):
        print(f"Sending transaction {i} from client1 to client2")
        job = Process(target=send_transaction,
                      args=(clients['client1'], 'client2', 10, ))
        job.start()
        time.sleep(15)
