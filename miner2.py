from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

app = Flask(__name__)
miners = []

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/init', methods=['POST'])
def receive_genesis():
    global miner
    json_block = request.form['block']
    block = Block.deserialize(json_block)

    miner.blockchain.add_block(block)
    print(miner.blockchain.blockchains)

    return Response(status=201)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5012, debug=True)
