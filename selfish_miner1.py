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

public_chain = Blockchain()
private_chain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(private_chain, public_key, sign_key)
private_branch_len = 0
last_unpublished_block = 0
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
    global miners, miner

    while True:
        print("Mining")
        block = miner.mine(need_transaction=False, selfish=True)
        if (block):
            recv_block_selfish(block, others=False)

    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miners, miner, public_chain, private_chain, private_branch_len, last_unpublished_block

    json_block = request.form['block']
    print("Received block from normal miner.")
    block = Block.deserialize(json_block)

    delta_prev = len(
        private_chain.blockchains[0]) - len(public_chain.blockchains[0])
    public_chain.add_block(block)

    if (delta_prev == 0):
        private_chain = public_chain
        private_branch_len = 0
    elif (delta_prev == 1):
        # public last block
        json_data = private_chain.blockchains[0][-1].serialize()
        broadcast(miners, json_data, '/recv_block')
        last_unpublished_block += 1
    elif (delta_prev == 2):
        # publish all chain
        for i in range(-2, 0):
            json_data = private_chain.blockchains[0][i].serialize()
            broadcast(miners, json_data, '/recv_block')
            last_unpublished_block += 1
        private_branch_len = 0
    else:
        # publish first unpublished block
        json_data = private_chain.blockchains[0][last_unpublished_block].serialize(
        )
        broadcast(miners, json_data, '/recv_block')
        last_unpublished_block += 1

    return Response(status=200)


@app.route('/recv_block_selfish', methods=['POST'])
def wrapper():
    json_block = request.form['block']
    block = Block.deserialize(json_block)

    return recv_block_selfish(block)


def recv_block_selfish(block, others=True):
    global miners, miner, public_chain, private_chain, private_branch_len, last_unpublished_block

    delta_prev = len(
        private_chain.blockchains[0]) - len(public_chain.blockchains[0])
    if (others):
        private_chain.add_block(block)
    private_branch_len += 1

    if (delta_prev == 0 and private_branch_len == 2):
        for i in range(-2, 0):
            json_data = private_chain.blockchains[0][i].serialize()
            broadcast(miners, json_data, '/recv_block')
            last_unpublished_block += 1
        private_branch_len = 0

    return Response(status=200)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5021, debug=True)
