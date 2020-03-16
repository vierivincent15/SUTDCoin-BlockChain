from flask import Flask, Response, render_template, request, redirect
from utils.spvclient import SPVClient
import requests

app = Flask(__name__)
miners = []
miner_server = 'http://127.0.0.1:5000'
client = SPVClient.new('1')


@app.route('/')
def index():
    global client

    return render_template('client_index.html', client=client)


@app.route('/send', methods=['POST'])
def create_client():
    global client
    if (client):
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
    app.run(host=ip, port=5001, debug=True)
