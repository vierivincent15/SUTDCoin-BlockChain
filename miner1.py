from flask import Flask, Response, make_response, render_template, request, redirect
from utils.miner import Miner
from utils.block import Block
from utils.blockchain import Blockchain
from utils.transaction import Transaction
from network_protocol import broadcast
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from multiprocessing import Process, Queue
import requests

app = Flask(__name__)
miners = ['http://127.0.0.1:5012']

blockchain = Blockchain()
sign_key = SigningKey.generate()
public_key = sign_key.get_verifying_key()
miner = Miner(blockchain, public_key, sign_key)
job = None

# TODO: change to predefined private key
miner2_priv_key = SigningKey.generate()
miner2_public_key = sign_key.get_verifying_key()
public_keys = {
    'miner2': miner2_public_key
}


@app.route('/')
def index():
    global miner

    return render_template('client_index.html', miner=miner)


@app.route('/init', methods=['POST'])
def start_mine():
    global miners, miner

    while True:
        block = miner.mine()
        if (block):
            json_data = block.serialize()
            broadcast(miners, json_data, '/recv_block')

    # response = Response(response=json_data, status=201)
    return Response(status=200)


@app.route('/recv_block', methods=['POST'])
def receive_block():
    global miner

    json_block = request.form['block']
    block = Block.deserialize(json_block)
    blockchain.add_block(block)


@app.route('/send', methods=['POST'])
def send_transaction():
    global miner
    receiver = request.form['receiver']
    amount = request.form['amount']

    tx = miner.send_transaction(public_keys[receiver], amount)
    return Response(status=200)


def mine_wrapper(queue, miner):
    queue.put(miner.mine())


@app.route('/recv_tx', methods=['POST'])
def receive_transaction():
    global miner, job
    serialized_tx = request.form['block']
    tx = Transaction.deserialize(serialized_tx)
    if (miner.blockchain.validate()):
        miner.blockchain.add_transaction(tx)
        print("added tx\n")

        block = miner.mine()
        print(block)
        # multiprocessing
        # queue = Queue()
        # job = Process(target=mine_wrapper, args=(queue, miner))
        # job = Process(target=miner.mine)
        # job.start()
        # block = queue.get()
        # job.join()
        # print(block)
        # jobs = None

        return Response(status=200)
    else:
        return Response(status=500)


@app.route('/stall', methods=['POST'])
def stall():
    global job
    job = Process(target=t)
    job.start()
    job.join()

    return Response(status=200)


@app.route('/test', methods=['GET'])
def stop():
    global job
    job.terminate()
    return Response(status=200)


def t():
    while True:
        pass


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5011, debug=True)
