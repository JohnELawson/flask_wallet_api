import json
from wallet.db import get_db
from typing import Mapping, Any
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)


auth = HTTPBasicAuth()

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


def get_balance(username: str) -> float:
    """ return users balance """
    # app.logger.info(f"get_balance - User: {username}")
    db = get_db()
    wallet = db.execute(
        "SELECT *"
        " FROM wallet w JOIN user u ON w.user_id = u.id"
        " WHERE u.username = ?",
        (username,)
    ).fetchone()

    balance = wallet["value"]

    # app.logger.debug(f"get_balance - balance: {balance}")
    return balance


def get_transactions(username: str, limit: int = 10) -> Mapping[str, Any]:
    """ return users transactions """
    # app.logger.info(f"get_transactions - User: {username}, Limit: {limit}")

    db = get_db()
    trans = db.execute(
        "SELECT *"
        " FROM 'transaction' t JOIN user u ON t.sender_id = u.id"
        " WHERE u.username = ?",
        (username,)
    ).fetchall()

    # app.logger.debug(f"get_transactions - transactions: {trans}")
    return trans


# def make_transfer(from_user: str, to_user: str, amount: float) -> bool:
#     """ pay a user """
#     from_user_wallet = [wal for wal in wallets if wal["user"] == from_user]
#     to_user_wallet = [wal for wal in wallets if wal["user"] == to_user]
#
#     # todo some mutex locking here
#
#     if from_user_wallet['value'] < amount:
#         app.logger.error(f"make_transfer - Failed: not enough funds in sender wallet")
#         # todo
#         return False
#
#     # update from wallet
#     # update to wallet
#     # update transactions
#     # todo roll back
#     return True


@auth.verify_password
def verify_password(username, password):
    """ lookup auth to db """
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password."

    return user["username"]


@bp.route('/', methods=['GET'])
@auth.login_required
def index_route():
    """ simple test """
    return f"Hello, {auth.current_user()}!"


@bp.route('/balance', methods=['GET'])
@auth.login_required
def balance_route():
    return f"{get_balance(auth.current_user())}"


@bp.route('/transactions', methods=['GET'])
@auth.login_required
def transactions_route():
    limit = request.args.get('limit', 10)
    # todo check input
    limit = int(limit)

    trans = get_transactions(auth.current_user(), limit)
    return f"{json.dumps(trans)}"


# @app.route('/transfer', method='POST')
# @auth.login_required
# def transfer_route():
#     from_user = auth.current_user()
#     to_user = escape(request.form.get('to_user'))
#     amount = request.form.get('amount')
#     # todo input validation
#     amount = float(amount)
#
#     trans = make_transfer(from_user, to_user, amount)
#     return f"{trans}"
