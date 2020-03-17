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


if __name__ == "__main__":
    pass
