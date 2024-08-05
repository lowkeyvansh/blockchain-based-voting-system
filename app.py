from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Replace with your contract's deployed address and ABI
contract_address = '0xYourContractAddress'
with open('VotingABI.json') as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def home():
    candidates = [contract.functions.candidates(i).call() for i in range(1, contract.functions.candidatesCount().call() + 1)]
    return render_template('index.html', candidates=candidates)

@app.route('/vote', methods=['POST'])
def vote():
    candidate_id = int(request.form['candidate'])
    account = w3.eth.accounts[0]

    tx_hash = contract.functions.vote(candidate_id).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    flash('Vote cast successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
