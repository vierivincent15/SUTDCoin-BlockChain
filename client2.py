from flask import Flask, Response, render_template, request, redirect
from utils.spvclient import SPVClient
import requests

app = Flask(__name__)
miners = ['http://127.0.0.1:5011', 'http://127.0.0.1:5012']
client = SPVClient.new('2', 100)


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
    global client
    receiver = request.form['receiver']
    amount = request.form['amount']
    print(receiver)
    print(amount)
    #UTXO = client.send_transaction()
    return Response(status=200)


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
    app.run(host=ip, port=5002, debug=True)
