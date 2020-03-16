from flask import Flask, Response, render_template, request, redirect
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
    transactions = []
    amount = 1000
    comment = "comment"
    for i in range(4):
        sign_key_1 = SigningKey.generate()
        sender = sign_key_1.get_verifying_key()
        sign_key_2 = SigningKey.generate()
        receiver = sign_key_2.get_verifying_key()

        Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)
        transactions.append(Tx)

    block = miner.mine(transactions, b'genesis block')
    print(block)

    if (miner):
        return Response(status=202)  # already created
    else:
        return Response(status=201)


@app.route('/test')
def test():
    response = requests.post(
        miner_server+'/add',
        data={'miner': 'miner1'}
    )
    print(response)
    return "k"


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5011, debug=True)
