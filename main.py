import requests
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np 
import pandas as pd 
import plotly.express as px

API_KEY = "RRA4HE9DZR6P77WFC7S3BMZVEQ7VP7B9IK" # etherscan API key
ETH_VALUE = 10 ** 18

Main_net = "https://api.etherscan.io/"
Goerli_testnet = "https://api-goerli.etherscan.io/"

#BASE_URL = "https://api.etherscan.io/api" #main net
BASE_URL = "https://api-goerli.etherscan.io/api" #test net


def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
        
    return url
    
    
def get_account_balance(address):
    # gets the account balance of the address
    
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = requests.get(balance_url)
    data = response.json()
    value = int(data['result']) / ETH_VALUE
    
    return value


def get_transactions(address):
    normal_tx_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response_normal = requests.get(normal_tx_url)
    data = response_normal.json()["result"]
    
    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response_internal = requests.get(internal_tx_url)
    data_internal = response_internal.json()["result"]
    
    data.extend(data_internal)
    data.sort(key=lambda x: int(x['timeStamp']))
    
    current_balance = 0
    balances = []
    balance_times = []
    
    for tx in data:
        to_addr = tx["to"]
        from_addr = tx["from"]
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        value = int(tx["value"]) / ETH_VALUE
        
        if "gasPrice" in tx:
            gas_cost = (int(tx["gasUsed"]) * int(tx["gasPrice"])) / ETH_VALUE
        else:
             gas_cost = int(tx["gasUsed"]) / ETH_VALUE
                
        money_in = to_addr.lower() == address.lower()
        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas_cost
            
        balances.append(current_balance)
        balance_times.append(time)
    
    fig = px.line(x=balance_times,y =balances,labels={'x':'time', 'y':'balance'})
    fig_plot = "line_plot.html"
    fig.write_html(fig_plot)
    print(current_balance)  
    
    
address = "0x3a53B398294B6378281D3Db712eB1d0E406296b4" #burner 
#address = "0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC" #example by etherscan

account_balance = get_account_balance(address)
print("account_balance :", account_balance)
get_transactions(address)
