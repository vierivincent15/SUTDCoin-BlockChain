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
        data={}
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
    return response.status_code


if __name__ == "__main__":
    for miner in miners.keys():
        job = Process(target=start_mine, args=(miner, ))
        job.start()

    time.sleep(10)
    print("Sending Transaction")
    for miner in miners.values():
        status = send_transaction(miner, 'client1', 50)
        if (status != 500):
            break

    # print(status)


# response = requests.post(
#     client1+'/create',
#     data={}
# )
# if(response.status_code == 201):
#     print("Client 1 created")
# else:
#     print("Client 1 already created")
