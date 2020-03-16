from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

app = Flask(__name__)
miners = ['http://127.0.0.1:5012']

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)


def broadcast(json_block):
    global miners
    for miner in miners:
        response = requests.post(
            miner+'/init',
            data={'block': json_block}
        )


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/init', methods=['POST'])
def mine_genesis():
    global miner

    block = miner.mine(b'genesis block')
    json_data = block.serialize()
    miner.blockchain.add_block(block)
    print(miner.blockchain.blockchains)

    response = Response(response=json_data, status=201)
    broadcast(json_data)

    return response


@app.route('/test')
def test():
    response = requests.post(
        miner1+'/add',
        data={'miner': 'miner1'}
    )
    print(response)
    return "k"


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5011, debug=True)
