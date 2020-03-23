from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from network_protocol import broadcast, broadcast_client, get_public_key, send_proof, start_malicious, broadcast_malicious
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process
import requests
import time

import logging


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

miners = ['http://127.0.0.1:5011', 'http://127.0.0.1:5012']
malicious = {
    'malicious1': 'http://127.0.0.1:5021',
    'malicious3': 'http://127.0.0.1:5023'
}

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)
pending_tx = {}
job = None


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/pub', methods=['GET'])
def get_pub_key():
    global public_key
    pub_key = public_key.to_string()
    response = Response(response=pub_key, status=200)

    return response


@app.route('/init', methods=['POST'])
def start_mine():
    global miners, miner, pending_tx, malicious

    while True:
        print("Mining")
        block = miner.mine_malicious(bc_idx=1, need_transaction=False)
        if (block):
            json_data = block.serialize()
            broadcast(miners, json_data, '/recv_block')
            broadcast_malicious(malicious, json_data, '/recv_block')
            for tid in pending_tx.keys():
                pending_tx[tid] = pending_tx[tid] - 1

    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miner, blockchain, pending_tx

    json_block = request.form['block']
    block = Block.deserialize(json_block)

    blockchain.add_block(block)
    for tid in pending_tx.keys():
        pending_tx[tid] = pending_tx[tid] - 1

    return Response(status=200)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5022, debug=True)
