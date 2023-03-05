from web3 import Web3
import os
from chain import fContract
from chain import handle_event


def register_on_contract(cost):
    
    # Get account
    web3 = Web3()
    web3.eth.account.enable_unaudited_hdwallet_features()
    mnemonic = ""
    with open('mnemonic.txt') as f:
        lines = f.readlines()
        mnemonic = lines[0]
    account = web3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
    
    # Send call to register on contract
    chain_id = web3.eth.chain_id
    tx = fContract.functions.registerResponder(cost, "").buildTransaction({
        "chainId": chain_id,
        'nonce': web3.eth.getTransactionCount(account.address),
        'from': account.address
    })
    print(tx)
    signed_tx = web3.eth.account.signTransaction(tx, private_key=account.key)

    sentTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    # Send call to fetch all past events from contract with 0x in responder field
    event_filter = fContract.events.RequestRecieved.createFilter(fromBlock='1401055', argument_filters={'responder':"0x0000000000000000000000000000000000000000"})
    
    # Select random 10 and send to model_runner
    count = 0
    for PairCreated in event_filter.get_all_entries():
        print("Sending to model_runner")
        handle_event(PairCreated)
        count += 1
        if count == 10:
            break