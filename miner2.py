from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from network_protocol import broadcast
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests

app = Flask(__name__)
miners = ['http://127.0.0.1:5011']

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/init', methods=['POST'])
def start_mine():
    global miners, miner

    while True:
        print("Mining")
        block = miner.mine()
        if (block):
            json_data = block.serialize()
            broadcast(miners, json_data, '/recv_block')

    return Response(status=201)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miner

    json_block = request.form['block']
    block = Block.deserialize(json_block)
    blockchain.add_block(block)


@app.route('/recv_tx', methods=['POST'])
def receive_transaction():
    global miner
    serialized_tx = request.form['block']
    tx = Transaction.deserialize(serialized_tx)
    if (miner.blockchain.validate()):
        miner.blockchain.add_transaction(tx)
        return Response(status=200)
    else:
        return Response(status=500)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5012, debug=True)
