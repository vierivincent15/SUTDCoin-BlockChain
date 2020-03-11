from flask import Flask, render_template, request, redirect
from spvclient import SPVClient
import requests

app = Flask(__name__)
miners = []
miner_server = 'http://127.0.0.1:5000'
client = None


@app.route('/')
def index():
    global client

    return render_template('client_index.html', client=client)


@app.route('/create')
def create_client():
    global client
    if (client):
        return "Already created"
    else:
        client = SPVClient.new('1')
        return redirect('/')


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
    app.run(host=ip, port=5001, debug=True)
