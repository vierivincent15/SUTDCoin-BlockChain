from ecdsa import VerifyingKey, NIST192p
import requests


def broadcast(miners, json_block, endpoint):
    for miner in miners:
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

if __name__ == "__main__":
    pass
