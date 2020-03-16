from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from network_protocol import broadcast
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

app = Flask(__name__)
miners = ['http://127.0.0.1:5012']

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
    global miners
    global miner

    block, status = miner.mine(b'genesis block')
    json_data = block.serialize()
    print(block.header)
    print(miner.blockchain.blockchains)

    response = Response(response=json_data, status=201)
    broadcast(miners, json_data, '/init')

    return response


@app.route('/send', methods=['POST'])
def send_transaction():
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
