import requests
import json

def check_project(cfg):
    api_url = "http://" + cfg["api"]
    print(api_url)

    # Create account
    id1, balance = create_account(api_url)

    # Make sure the balance is what has been set
    check_account_balance(api_url, id1, balance)

    # Check the balance of an unknown account
    check_unknown_account(api_url)

    # Check the operations that should be 0 or 1

    # Make a transfer to myself

    # Create another account

    # Check the balance

    # Make a transfer account to account


def create_account(api):
    balance = 50

    res = requests.post(api + "/account", json=json.dumps({"balance": balance}))
    if res.status_code != 200:
        raise Exception("AccountCreation - Error while creating account.")

    data = res.json()

    if data["currency"] != "EUR":
        raise Exception("AccountCreation - The currency is not EUR.")
    if data["balance"] != balance:
        raise Exception("AccountCreation - The balance is incorrect")
    if data["account"] < 100000 and data["account"] > 999999:
        raise Exception("AccountCreation - The account is invalid")
    
    return data["account"], balance


def check_account_balance(api, account_id, balance):
    res = requests.post(api + "/account/" + account_id + "/balance")
    if res.status_code != 200:
        raise Exception("AccountBalance - Error while querying the balance.")

    data = res.json()

    if data["currency"] != "EUR":
        raise Exception("AccountBalance - The currency is not EUR.")
    if data["balance"] != balance:
        raise Exception("AccountBalance - The balance is incorrect")
    if data["account"] != account_id:
        raise Exception("AccountBalance - The account is invalid")


def check_unknown_account(api):
    res = requests.post(api + "/account/666/balance")
    if res.status_code != 404:
        raise Exception("UnknownAccount - Unexpected HTTP code.")
