from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from network_protocol import broadcast, get_public_key, send_proof
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import requests
import time

app = Flask(__name__)
miners = ['http://127.0.0.1:5011']
clients = {
    'client1': 'http://127.0.0.1:5001',
    'client2': 'http://127.0.0.1:5002'
}

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
    global miners, miner

    while True:
        print("Mining")
        block = miner.mine()
        if (block):
            json_data = block.serialize()
            broadcast(miners, json_data, '/recv_block')
            for tx in block.transactions:
                if (tx.tid in pending_tx):
                    pending_tx[tx.tid] = miner.get_transaction_proof(tx)

    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miner, blockchain, pending_tx

    json_block = request.form['block']
    block = Block.deserialize(json_block)
    blockchain.add_block(block)
    for tx in block.transactions:
        if (tx.tid in pending_tx):
            pending_tx[tx.tid] = miner.get_transaction_proof(tx)

    return Response(status=200)


@app.route('/send', methods=['POST'])
def send_transaction():
    global miner, clients, pending_tx
    receiver = request.form['receiver']
    amount = request.form['amount']

    try:
        pub_key = get_public_key(clients[receiver])
        tx = miner.send_transaction(pub_key, amount)
        pending_tx[tx.tid] = None
        json_data = tx.serialize()
        broadcast(miners, json_data, '/recv_tx')
        print("Broadcasting Transaction")

        while (pending_tx[tx.tid] == None):
            time.sleep(1)
        print(f"Got proof: {pending_tx[tx.tid]}")
        send_proof(clients[receiver], pending_tx[tx.tid])

        del (pending_tx[tx.tid])
        return Response(status=200)
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


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5012, debug=True)
