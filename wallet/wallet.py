import os
import json
import logging
from flask import Flask, request
from typing import Mapping, Any
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.DEBUG))
log = logging.getLogger(__name__)
# todo add time to log

app = Flask(__name__)
auth = HTTPBasicAuth()
# todo improve auth


# todo change to db
users = {
    "john": generate_password_hash("pass1"),
    "susan": generate_password_hash("pass2")
}

wallets = [
    {
        "user": "john",
        "value": 100.0
    },
    {
        "user": "susan",
        "value": 0.0
    }
]

transactions = [
    {
        "from_user": "john",
        "to_user": "susan",
        "amount": 50,
        "timestamp": 1, # todo
    }
]


def get_balance(username: str) -> float:
    """ return users balance """
    global wallets
    log.info(f"get_balance - User: {username}")
    balance = [wal for wal in wallets if wal["user"] == username][0]['value']
    log.debug(f"get_balance - balance: {balance}")
    return balance


def get_transactions(username: str, limit: int = 10) -> Mapping[str, Any]:
    """ return users transactions """
    log.info(f"get_transactions - User: {username}, Limit: {limit}")

    count = 0
    trans = []
    for i in transactions:

        if count > limit:
            # exit if limit found
            break

        if i["from_user"] == username:
            # return transaction
            trans.append(i)
            count += 1

    log.debug(f"get_transactions - transactions: {trans}")
    return trans


def make_transfer(from_user: str, to_user: str, amount: float) -> bool:
    """ pay a user """
    global wallets

    from_user_wallet = [wal for wal in wallets if wal["user"] == from_user]
    to_user_wallet = [wal for wal in wallets if wal["user"] == to_user]

    # todo some mutex locking here

    if from_user_wallet['value'] < amount:
        log.error(f"make_transfer - Failed: not enough funds in sender wallet")
        # todo
        return False

    # update from wallet
    # update to wallet
    # update transactions
    # todo roll back
    return True




@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/', methods=['GET'])
@auth.login_required
def index_route():
    return f"Hello, {auth.current_user()}!"


@app.route('/balance', methods=['GET'])
@auth.login_required
def balance_route():
    return f"{get_balance(auth.current_user())}"


@app.route('/transactions', methods=['GET'])
@auth.login_required
def transactions_route():
    limit = request.args.get('limit', 10)
    # todo check input
    limit = int(limit)

    trans = get_transactions(auth.current_user(), limit)
    return f"{json.dumps(trans)}"


@app.route('/transfer', methods=['POST'])
@auth.login_required
def transfer_route():
    from_user = auth.current_user()
    to_user = request.form.get('to_user')
    amount = request.form.get('amount')
    # todo input validation
    amount = float(amount)

    trans = make_transfer(from_user, to_user, amount)
    return f"{trans}"


if __name__ == '__main__':
    app.run()
