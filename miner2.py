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

miners = ['http://127.0.0.1:5011']
clients = {
    'client1': 'http://127.0.0.1:5001',
    'client2': 'http://127.0.0.1:5002'
}
malicious = {
    'malicious1': 'http://127.0.0.1:5021',
    'malicious2': 'http://127.0.0.1:5022',
    'malicious3': 'http://127.0.0.1:5023'
}
selfish_pool = {'selfish1': 'http://127.0.0.1:5021'}

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)
pending_tx = {}


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
    global miners, miner, pending_tx, clients, malicious, selfish_pool

    wait = request.form['wait']
    selfish = False
    if (wait == 'selfish'):
        selfish = True
        wait = 'no'
    if (wait == 'no'):
        wait = False
    else:
        wait = True
    while True:
        print("Mining")
        block = miner.mine(wait)
        if (block):
            json_data = block.serialize()
            broadcast(miners, json_data, '/recv_block')
            if(wait):
                broadcast_client(
                    clients, block.serialize(True), '/recv_header')
            else:
                if(selfish):
                    broadcast_malicious(selfish_pool, json_data, '/recv_block')
                    if(len(miner.blockchain.blockchains[0]) == 1):
                        job = Process(target=start_malicious,
                                    args=(malicious['malicious1'], ))
                        job.start()
                else:
                    broadcast_malicious(malicious, json_data, '/recv_block')
                    if(len(miner.blockchain.blockchains[0]) == 3):
                        job = Process(target=start_malicious,
                                    args=(malicious['malicious1'], ))
                        job.start()
            for tid in pending_tx.keys():
                pending_tx[tid] = pending_tx[tid] - 1

    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miner, blockchain, pending_tx

    json_block = request.form['block']
    block = Block.deserialize(json_block)
    blockchain.add_block(block)
    chain_len = [len(chain) for chain in blockchain.blockchains]
    print(chain_len)
    for tid in pending_tx.keys():
        pending_tx[tid] = pending_tx[tid] - 1

    return Response(status=200)


@app.route('/send', methods=['POST'])
def send_transaction():
    global miner, clients, pending_tx
    receiver = request.form['receiver']
    amount = request.form['amount']

    try:
        pub_key = get_public_key(clients[receiver])
        tx = miner.send_transaction(pub_key, amount)
        pending_tx[tx.tid] = 3
        serialized_tx = tx.serialize()
        broadcast(miners, serialized_tx, '/recv_tx')
        print("Broadcasting Transaction")

        while (pending_tx[tx.tid] != 0):
            time.sleep(1)
        print("Received enough transaction.")
        proof = miner.get_transaction_proof(tx)
        print("Sending proof...")
        status = send_proof(clients[receiver],
                            serialized_tx, proof)

        del (pending_tx[tx.tid])
        if(status == 200):
            print("Proof validated")
            return Response(status=200)
        else:
            print("Proof BAAAAAAAAAAAAAAD")
            return Response(status=406)

    except KeyError:
        print("Not enough coins")
        return Response(status=500)


@app.route('/recv_tx', methods=['POST'])
def receive_transaction():
    global miner
    serialized_tx = request.form['block']
    tx = Transaction.deserialize(serialized_tx)
    try:
        miner.add_transaction(tx)
        print("Added transaction\n")
        return Response(status=200)
    except ValueError:
        return Response(status=500)


@app.route('/get_balance', methods=['GET'])
def get_balance():
    global miner

    balance = miner.get_balance()
    response = Response(response=balance, status=200)

    return response


@app.route('/get_random_tx', methods=['GET'])
def get_random_tx():
    global miner

    random_tx = miner.blockchain.blockchains[-1][-1].transactions[-1].serialize(
        True)
    response = Response(response=random_tx, status=200)

    return response


@app.route('/resend_duplicate', methods=['POST'])
def resend_duplicate():
    global miner

    serialized_tx = request.form["tx"]
    res = broadcast(miners, serialized_tx, '/recv_tx')
    if res.status_code == 500:
        print("Can't add duplicate transaction as it exist in the blockchain")
        return Response(status=500)

    return Response(status=200)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5012, debug=True)
