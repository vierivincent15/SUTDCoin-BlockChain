from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

app = Flask(__name__)
miners = []

TARGET = b'\x00\x00\xff\xff' + b'\xff'*28
blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/init', methods=['POST'])
def mine_genesis():
    global miner
    global TARGET

    #block = miner.mine(b'genesis block')
    # print(block)
    data = {
        "block": "test"
    }
    #response = Response(response=data, status=201)
    #response._content = data
    response = make_response(data, 201)

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
