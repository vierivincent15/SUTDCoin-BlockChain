from flask import Response
from ecdsa import VerifyingKey, NIST192p
import requests


def broadcast(miners, json_block, endpoint):
    response = Response(status=200)
    for miner in miners:
        response = requests.post(
            miner+endpoint,
            data={'block': json_block}
        )
    return response


def broadcast_client(clients, header, endpoint):
    for client in clients.values():
        response = requests.post(
            client+endpoint,
            data={'header': header}
        )


def broadcast_malicious(malicious, json_block, endpoint):
    for miner in malicious.values():
        response = requests.post(
            miner+endpoint,
            data={'block': json_block}
        )


def get_public_key(receiver):
    response = requests.get(receiver+'/pub')
    pub_key = VerifyingKey.from_string(response.content, curve=NIST192p)
    return pub_key


def send_proof(receiver, json_tx, serialized_proof):
    response = requests.post(
        receiver+'/recv_proof',
        data={
            'transaction': json_tx,
            'proof': serialized_proof
        }
    )
    return response.status_code


def request_proof(miner, json_tx):
    response = requests.post(
        miner+'/req_proof',
        data={
            'transaction': json_tx,
        }
    )
    return response.content


def start_malicious(miner):
    response = requests.post(
        miner+'/init',
        data={}
    )


if __name__ == "__main__":
    pass
