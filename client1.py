from flask import Flask, Response, render_template, request, redirect
from utils.spvclient import SPVClient
from utils.transaction import Transaction
from network_protocol import broadcast, get_public_key
import requests
import time

app = Flask(__name__)
miners = ['http://127.0.0.1:5011', 'http://127.0.0.1:5012']
clients = {
    'client2': 'http://127.0.0.1:5002'
    }

client = SPVClient.new('1')
print("Client Initialized")
print(f"Balance: {client.balance}\n")


@app.route('/')
def index():
    global client
    return render_template('client_index.html', client=client)


@app.route('/pub', methods=['GET'])
def get_pub_key():
    global client
    pub_key = client.public_key.to_string()
    response = Response(response=pub_key, status=200)

    return response


@app.route('/send', methods=['POST'])
def create_transaction():
    global clients, client

    receiver = request.form['receiver']
    amount = int(request.form['amount'])
    
    pub_key = get_public_key(clients[receiver])
    UTXO = client.send_transaction(pub_key, amount)
    broadcast(miners, UTXO.serialize(), '/recv_tx')

    time.sleep(5)
    return Response(status=200)


@app.route('/recv_proof', methods=['POST'])
def receive_proof():
    global client

    serialized_tx = request.form['transaction']
    tx = Transaction.deserialize(serialized_tx)
    serialized_proof = request.form['proof']
    # ([proof_idx, proof], root)
    proof, root = client.deserialize_proof(serialized_proof)

    if(client.validate_transaction(tx, proof, root)):
        print("Proof valid")
        client.balance += tx.amount
        return Response(status=200)
    else:
        print("Proof BAAAAAAAAAAAAAAD")
        return Response(status=406)


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5001, debug=True)
