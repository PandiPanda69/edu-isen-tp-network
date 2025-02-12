import requests
import json
import random

def check_project(cfg):
    random.seed()

    api_pub = "http://" + cfg["api_pub"]
    api_priv = "http://" + cfg["api_priv"]

    # Create account
    id1, balance = create_account(api_pub)

    # Make sure the balance is what has been set
    check_account_balance(api_pub, id1, balance)

    # Check the balance of an unknown account
    check_unknown_account(api_pub)

    # Check the operations - len should be 0 or 1
    check_account_operations(api_pub, id1, balance, 0, 1)

    # Make a transfer to myself
    amount = 50
    label = "VIREMENT A MOI-MEME"
    customer_transfer(api_pub, id1, id1, amount, 'EUR', label)

    def check_self_transfer(ops):
        found_in = False
        found_out = False

        for op in ops:
            if label in op["label"]:
                if op["amount"] == amount:
                    found_in = True
                if op["amount"] == -amount:
                    found_out = True

        if found_in == False:
            raise Exception("SelfTransfer - No ingress operation.")
        if found_out == False:
            raise Exception("SelfTransfer - No egress operation.")

    # Check the transfer
    check_account_operations(api_pub, id1, balance, 2, 3, checker=check_self_transfer)

    # Create another account
    id2, balance2 = create_account(api_pub)

    # Check the balance
    check_account_balance(api_pub, id2, balance2)

    # Make a transfer account to account
    amount = 44
    label = "LE VIREMENT"
    customer_transfer(api_pub, id1, id2, amount, 'EUR', label)

    balance = balance - amount
    balance2 = balance2 + amount

    # Check the transfer
    def check_the_transfer(ops):
        found_in = False
        found_out = False

        for op in ops:
            if label in op["label"]:
                if op["amount"] == amount:
                    found_in = True
                if op["amount"] == -amount:
                    found_out = True

        if found_in == True or found_out == True:
            pass
        else:
            raise Exception("Transfer - Missing operation.")

    check_account_operations(api_pub, id1, balance , 3, 4, checker=check_the_transfer)
    check_account_operations(api_pub, id2, balance2, 1, 2, checker=check_the_transfer) 

    # Accounts exist ?
    account_exists(api_priv, id1)
    account_exists(api_priv, id2)

    # Check invalid account
    account_exists(api_priv, 666)

    # Card payment
    amount = 15
    label = "PAIEMENT CARTE"
    card_payment(api_priv, id2, id1, 'EUR', amount, label)

    balance = balance + amount
    balance2 = balance2 - amount

    # Operations
    check_account_operations(api_pub, id1, balance,  4, 5, checker=check_the_transfer)
    check_account_operations(api_pub, id2, balance2, 2, 3, checker=check_the_transfer)

    # Denied card operation
    card_payment(api_priv, id2, id1, 'EUR', 175000, "ACHAT VOITURE")

    # Check balance
    check_account_balance(api_pub, id1, balance)    
    check_account_balance(api_pub, id2, balance2)

    # InstantTransfer
    amount = 6.99
    label = "VIRMT MICHEL"
    instant_transfer(api_priv, id1, id2, amount, 'EUR', label)

    balance = balance - amount
    balance2 = balance2 + amount

    # Operations
    check_account_operations(api_pub, id1, balance,  4, 5, checker=check_the_transfer)
    check_account_operations(api_pub, id2, balance2, 2, 3, checker=check_the_transfer)


def create_account(api):
    balance = 50 + random.randint(0, 50)

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


def check_account_operations(api, account_id, balance, min_len, max_len, checker=None):
    res = requests.post(api + "/account/" + account_id + "/details")
    if res.status_code != 200:
        raise Exception("AccountDetails - Error while querying the details.")

    data = res.json()

    if data["currency"] != "EUR":
        raise Exception("AccountDetails - The currency is not EUR.")
    if data["balance"] != balance:
        raise Exception("AccountDetails - The balance is incorrect")
    if data["account"] != account_id:
        raise Exception("AccountDetails - The account is invalid")
    if len(data["operations"]) < min_len or len(data["operations"]) > max_len:
        raise Exception("AccountDetails - Wrong amount of operations.")

    if checker is not None:
        checker(data["operations"])


def customer_transfer(api, account_id, recipient, amount, currency, label):
    res = requests.post(api + "/account/" + account_id + "/transfer", json=json.dumps({
        "amount": amount,
        "currency": currency,
        "label": label,
        "recipient": recipient,
    }))
    if res.status_code != 200:
        raise Exception("Transfer - Error while creating a new transfer.")


def account_exists(api, account_id):
    res = requests.get(api + "/account/" + account_id + "/exists")    
    if res.status_code != 200:
        raise Exception("AccountExists - Error while querying private API.")


def account_not_exists(api, account_id):
    res = requests.get(api + "/account/" + account_id + "/exists")    
    if res.status_code != 404:
        raise Exception("AccountExists - Error while querying private API.")


def card_payment(api, source, dest, currency, amount, merchant):
    res = requests.post(api + "/transaction/card", json=json.dumps({
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "merchant": merchant,
    }))
    if res.status_code != 200:
        raise Exception("CardPayment - Error while paying.")


def card_payment_denied(api, source, dest, currency, amount, merchant):
    res = requests.post(api + "/transaction/card", json=json.dumps({
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "merchant": merchant,
    }))
    if res.status_code != 401:
        raise Exception("CardPaymentDenied - Error while paying.")


def instant_transfer(api, source, dest, currency, amount, label):
    res = requests.post(api + "/transaction/transfer", json=json.dumps({
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "label": label,
    }))
    if res.status_code != 200:
        raise Exception("InstantTransfer - Error while paying.")
