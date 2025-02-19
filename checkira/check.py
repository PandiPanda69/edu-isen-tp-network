import requests
import random
import json

def check_project(cfg):
    random.seed()

    api_pub = "http://" + cfg["api_pub"]
    api_priv = "http://" + cfg["api_priv"]

    # Create account
    id1, balance = create_account(api_pub)
    print("Create account OK: ", id1, balance)

    # Make sure the balance is what has been set
    check_account_balance(api_pub, id1, balance)
    print("Check Account balance OK")

    # Check the balance of an unknown account
    check_unknown_account(api_pub)
    print("Check unknown account: OK")

    # Check the operations - len should be 0 or 1
    check_account_operations(api_pub, id1, balance, 0, 1)
    print("Check operations OK")

    # Make a transfer to myself
    amount = 50
    label = "VIREMENT A MOI-MEME"
    customer_transfer(api_pub, id1, id1, amount, 'EUR', label)
    print("Self transfer OK")

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
    print("Transfer operations OK")

    # Create another account
    id2, balance2 = create_account(api_pub)
    print("Create account 2 OK")

    # Check the balance
    check_account_balance(api_pub, id2, balance2)
    print("Check balance account 2 OK")

    # Make a transfer account to account
    amount = 44
    label = "LE VIREMENT"
    customer_transfer(api_pub, id1, id2, amount, 'EUR', label)
    print("Transfer account1 to account2 OK")

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
    account_not_exists(api_priv, 666666)

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
    card_payment(api_priv, id2, id1, 'EUR', 175000, "ACHAT VOITURE", 401)

    # Check balance
    check_account_balance(api_pub, id1, balance)
    check_account_balance(api_pub, id2, balance2)

    # InstantTransfer
    amount = 6.99
    label = "VIRMT MICHEL"
    instant_transfer(api_priv, id1, id2, 'EUR', amount, label)

    balance = balance - amount
    balance2 = balance2 + amount

    # Operations
    check_account_operations(api_pub, id1, balance,  4, 5, checker=check_the_transfer)
    check_account_operations(api_pub, id2, balance2, 2, 3, checker=check_the_transfer)


def create_account(api):
    balance = 50 + random.randint(0, 50)

    res = requests.post(api + "/account", json={"balance": balance})
    if res.status_code != 200:
        raise Exception("AccountCreation - Error while creating account: received status_code " + str(res.status_code))

    data = res.json()

    if data["currency"] != "EUR":
        raise Exception("AccountCreation - The currency is not EUR.")
    if data["balance"] != balance:
        raise Exception("AccountCreation - The balance is incorrect")
    if data["account"] < 100000 and data["account"] > 999999:
        raise Exception("AccountCreation - The account is invalid")

    return data["account"], balance


def check_account_balance(api, account_id, balance):
    res = requests.get(api + "/account/" + str(account_id) + "/balance")
    if res.status_code != 200:
        raise Exception("AccountBalance - Error while querying the balance: received status_code " + str(res.status_code))

    data = res.json()

    if data["currency"] != "EUR":
        raise Exception("AccountBalance - The currency is not EUR.")
    if data["balance"] != balance:
        raise Exception("AccountBalance - The balance is incorrect")
    if data["account"] != account_id:
        raise Exception("AccountBalance - The account is invalid")


def check_unknown_account(api):
    res = requests.get(api + "/account/999999/balance")
    if res.status_code != 404:
        raise Exception("UnknownAccount - Unexpected HTTP code: " + str(res.status_code))


def check_account_operations(api, account_id, balance, min_len, max_len, checker=None):
    res = requests.get(api + "/account/" + str(account_id) + "/details")
    if res.status_code != 200:
        raise Exception("AccountDetails - Error while querying the details: status code: " + str(res.status_code))

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
    d = {
        "amount": amount,
        "currency": currency,
        "label": label,
        "recipient": recipient,
    }

    print("Sending /account/%d/transfer with [%s]" % (account_id, json.dumps(d)))
    res = requests.post("%s/account/%d/transfer" % (api, account_id), json=d)
    if res.status_code != 200:
        raise Exception("Transfer - Error while creating a new transfer: status code: " + str(res.status_code))


def account_exists(api, account_id):
    res = requests.get("%s/account/%d/exists" % (api, account_id))
    if res.status_code != 200:
        raise Exception("AccountExists - Error while querying private API: status code: " + str(res.status_code))


def account_not_exists(api, account_id):
    res = requests.get("%s/account/%d/exists" % (api, account_id))
    if res.status_code != 404:
        raise Exception("AccountExists - Error while querying private API: status code: " + str(res.status_code))


def card_payment(api, source, dest, currency, amount, merchant, expected_status=200):
    d = {
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "merchant": merchant,
    }

    print("Sending /transaction/card with [%s]" % (json.dumps(d)))
    res = requests.post(api + "/transaction/card", json=d)
    if res.status_code != expected_status:
        raise Exception("CardPayment - Error while paying.")


def card_payment_denied(api, source, dest, currency, amount, merchant):
    d = {
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "merchant": merchant,
    }
    
    print("Sending /transaction/card with [%s]" % (json.dumps(d)))
    res = requests.post(api + "/transaction/card", json=d)
    if res.status_code != 401:
        raise Exception("CardPaymentDenied - Error while paying: status code: " + str(res.status_code))


def instant_transfer(api, source, dest, currency, amount, label):
    d = {
        "sourceAccount": source,
        "destAccount": dest,
        "currency": currency,
        "amount": amount,
        "label": label,
    }

    print("Sending /transation/transfer with [%s]" % (json.dumps(d)))
    res = requests.post(api + "/transaction/transfer", json=d)
    if res.status_code != 200:
        raise Exception("InstantTransfer - Error while paying: status code: " + str(res.status_code))
