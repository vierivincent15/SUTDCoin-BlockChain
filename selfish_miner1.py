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
selfish_pool = []

public_blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(public_blockchain, public_key, sign_key)
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
    global miners, miner, selfish_pool

    while True:
        print("Mining")
        block = miner.mine_selfish(need_transaction=False)
        if (block):
            json_data = block.serialize()
            broadcast(selfish_pool, json_data, '/recv_block_selfish')
            recv_block_selfish(block, others=False)

    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miners, miner, public_blockchain, private_branch_len, last_unpublished_block

    json_block = request.form['block']
    print("Received block from normal miner.")
    block = Block.deserialize(json_block)

    delta_prev = len(
        miner.private_chain) - len(public_blockchain.blockchains[public_blockchain.true_blockchain])

    public_blockchain.add_block(block)
    # temp_public_chain = public_blockchain.blockchains[public_blockchain.true_blockchain]

    # if len(temp_public_chain) != len(public_chain):
    #     public_chain = temp_public_chain.copy()
    #     print(len(public_chain))

    print("delta_prev: " + str(delta_prev))
    print("private_branch_len: " + str(private_branch_len))
    print()
    
    if (delta_prev == 0):
        # private_chain.add_block(block)
        print("Resetting private chain")
        miner.reset_private_chain()
        private_branch_len = 0
        # temp_private_chain = Blockchain()
        # for block in public_chain:
        #     temp_private_chain.add_block(block)
        # private_chain = copy(temp_private_chain, deep=True)

    elif (delta_prev == 1):
        print("COOL11!")
        # public last block
        # json_data = private_chain.blockchains[0][-1].serialize()
        block = miner.private_chain[-1]
        json_data = block.serialize()
        print("Broadcasting...")
        broadcast(miners, json_data, '/recv_block')
        print()
        public_blockchain.add_block(block)
        last_unpublished_block += 1

    elif (delta_prev == 2):
        # publish all chain
        for i in range(-2, 0):
            # json_data = private_chain.blockchains[0][i].serialize()
            block = miner.private_chain[i]
            json_data = block.serialize()
            print("Broadcasting...")
            broadcast(miners, json_data, '/recv_block')
            print()
            public_blockchain.add_block(block)
            last_unpublished_block += 1
            time.sleep(1)
        private_branch_len = 0

    else:
        # publish first unpublished block
        # json_data = private_chain.blockchains[0][last_unpublished_block].serialize()

        block = miner.private_chain[last_unpublished_block]
        json_data = block.serialize()
        print("Broadcasting...")
        broadcast(miners, json_data, '/recv_block')
        print()
        public_blockchain.add_block(block)
        last_unpublished_block += 1

    return Response(status=200)


@app.route('/recv_block_selfish', methods=['POST'])
def wrapper():
    json_block = request.form['block']
    block = Block.deserialize(json_block)

    return recv_block_selfish(block)


def recv_block_selfish(block, others=False):
    global miners, miner, public_blockchain, private_branch_len, last_unpublished_block

    # if others:
    # private_chain.add_block(block, print_idx=True)
    # miner.private_chain.append(block)

    delta_prev = len(miner.private_chain) - \
        len(public_blockchain.blockchains[public_blockchain.true_blockchain])

    miner.add_block_to_private(block)

    # public_blockchain.add_block(block)
    private_branch_len += 1

    print("delta_prev00: " + str(delta_prev))
    print("private_branch_len: " + str(private_branch_len))
    print()
    if (delta_prev == 0 and private_branch_len == 2):
        print("Sending block!")
        for i in range(-1, 0):
            block = miner.private_chain[i]
            # block = private_chain.blockchains[0][i]
            json_data = block.serialize()
            print("Broadcasting...")
            broadcast(miners, json_data, '/recv_block')
            print()
            public_blockchain.add_block(block)
            last_unpublished_block += 1
        private_branch_len = 0

    return Response(status=200)


@app.route('/get_balance', methods=['GET'])
def get_balance():
    global miner

    balance = miner.get_balance()
    response = Response(response=balance, status=200)

    return response


@app.route('/get_id', methods=['GET'])
def get_miner_id():
    global miner
    response = Response(response=miner.id, status=200)

    return response


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5021, debug=True)
