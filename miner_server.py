from flask import Flask, render_template, request, redirect

app = Flask(__name__)
miners = []


@app.route('/')
def index():
    global miners
    return render_template('index.html', miners=miners)


@app.route('/add', methods=["POST"])
def add_miner():
    global miners

    miner = request.form['miner']

    if (miner not in miners):
        miners.append(miner)
        print(f"Miner: {miner}")

    return redirect('/')


if __name__ == "__main__":
    ip = ""
    if (ip == ""):
        ip = "localhost"
    app.run(host=ip, port=5000, debug=True)
