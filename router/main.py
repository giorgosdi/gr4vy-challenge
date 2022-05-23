from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

app.secret_key = 'secret'

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'Gr4vy Platform Challenge'})


@app.route('/auth', methods=['POST', 'GET'])
def authorize():
    ui = os.getenv('UI', True)
    if ui == True:
        if request.method == 'GET':
            return render_template('auth.html')
        if request.method == 'POST':
            result = request.form
            for key, value in result.items():
                if key == 'Username':
                    username = value
                if key == 'Password':
                    password = value
    else:
        data = request.get_json()
        username: str = data.get('username')
        password: str = data.get('password')
    local = os.getenv("DOCKER", False)
    if local == False:
        response = requests.post('http://gr4vy-challenge_auth-api_1:5001/token', json={"username":username, "password":password})
    return response.content, response.status_code


@app.route('/transact', methods=["POST", "GET"])
def transact():
    ui = os.getenv('UI', True)
    if ui == True:
        if request.method == 'GET':
            return render_template('transact.html')
        if request.method == 'POST':
            result = request.form
            for key, value in result.items():
                if key == "Amount":
                    amount = value
                if key == "Currency":
                    currency = value
                if key == "Token":
                    token = value
    else:
        data = request.get_json()
        token: str = data.get('token')
        currency: str = data.get('currency')
        amount: str = data.get('amount')

    local = os.getenv('DOCKER', False)
    if local == False:
        response = requests.post('http://gr4vy-challenge_core-api_1:5002/transaction', json={"token":token, "amount":amount, "currency": currency})
    else:
        response = requests.post('http://0.0.0.0:5002/transaction', json={"token":token, "amount":amount, "currency": currency})
    return response.content, response.status_code

if __name__ == "__main__":
    http_port: int = int(os.getenv('HTTP_PORT', 5000))
    app.run(host='0.0.0.0', port=http_port, debug=True)
