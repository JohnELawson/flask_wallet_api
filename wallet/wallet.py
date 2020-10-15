from typing import Mapping, Any
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import (
    Blueprint,
    request,
    jsonify,
    escape,
    current_app,
    abort,
)
from wallet.db import get_db


auth = HTTPBasicAuth()

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


def get_balance(username: str) -> float:
    """ return users balance """
    current_app.logger.info(f"get_balance - User: {username}")
    db = get_db()
    wallet = db.execute(
        "SELECT *"
        " FROM wallet w JOIN user u ON w.user_id = u.id"
        " WHERE u.username = ?",
        (username,)
    ).fetchone()

    bal = {
        "balance": wallet["value"],
        "currency": wallet["currency"]
    }
    current_app.logger.debug(f"get_balance - balance: {bal}")
    return bal


def get_transactions(username: str, limit: int = 10) -> Mapping[str, Any]:
    """ return users transactions """
    current_app.logger.info(f"get_transactions - User: {username}, Limit: {limit}")

    db = get_db()
    rows = db.execute(
        "SELECT u.username, t.receiver_id, t.created, t.value, t.currency"
        " FROM 'transaction' t JOIN user u ON t.sender_id = u.id"
        " WHERE u.username = ?"
        " ORDER BY t.created ASC"
        " LIMIT ?",
        (username, limit)
    ).fetchall()

    data = []
    for row in rows:
        # get receiver name - probably can merge this in above sql
        receiver = db.execute("SELECT username FROM user WHERE id = ?", (row["receiver_id"],)).fetchone()

        data.append({
            "sender": row["username"],
            "receiver": receiver["username"],
            "date": row["created"],
            "value": row["value"],
            "currency": row["currency"],
        })

    current_app.logger.debug(f"get_transactions - transactions: {data}")
    return data


def make_transfer(from_username: str, to_user: str, amount: float) -> Mapping[str, str]:
    """ pay a user """
    current_app.logger.info(f"make_transfer - From user: {from_username}, to_user: {to_user}, amount: {amount}")

    # todo need some sort of strong consistency / mutex around this to ensure the funds arent spent twice at the same time

    db = get_db()

    # get sender id
    sender = db.execute("SELECT * FROM user WHERE username = ?", (from_username,)).fetchone()

    # check receiver exists
    receiver = db.execute("SELECT * FROM user WHERE id = ?", (to_user,)).fetchone()

    if receiver is None:
        response = {
            "status": "error",
            "reason": "receiving user does not exist"
        }
        current_app.logger.info(f"make_transfer: {response}")
        return response

    # check sender has enough funds
    # assuming one currency
    from_balance = get_balance(from_username)["balance"]
    if from_balance < amount:
        response = {
            "status": "error",
            "reason": "sending user does not have enough funds"
        }
        current_app.logger.info(f"make_transfer: {response}")
        return response

    # update from wallet
    db.execute(
        "UPDATE wallet"
        " SET value = value - ?"
        " WHERE user_id = ?",
        (amount, sender["id"]),
    )
    # db.commit()
    # todo better rounding / storage of floats

    # update from wall
    db.execute(
        "UPDATE wallet"
        " SET value = value + ?"
        " WHERE user_id = ?",
        (amount, to_user),
    )
    db.commit()

    # update transactions
    db.execute(
        "INSERT INTO 'transaction'"
        " (sender_id, receiver_id, value, currency) "
        " VALUES (?,?,?,?)",
        (sender["id"], to_user, amount, 'SGD'),
    )
    db.commit()

    response = {
        "status": "success",
    }
    current_app.logger.debug(f"make_transfer - transactions: {response}")
    return response


@auth.verify_password
def verify_password(username, password):
    """ lookup auth to db """
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        current_app.logger.info(f"verify_password - incorrect username")
        abort(403)
        # todo handle errors
    elif not check_password_hash(user["password"], password):
        current_app.logger.info(f"verify_password - incorrect password")
        abort(403)

    return user["username"]


@bp.route('/', methods=['GET'])
@auth.login_required
def index_route():
    """ simple test """
    return f"Hello, {auth.current_user()}!"


@bp.route('/balance', methods=['GET'])
@auth.login_required
def balance_route():
    """ get balance """
    return get_balance(auth.current_user())


@bp.route('/transactions', methods=['GET'])
@auth.login_required
def transactions_route():
    """ list transactions """
    limit = request.args.get('limit', 10)
    # todo check input
    limit = int(limit)

    return jsonify(list(get_transactions(auth.current_user(), limit)))


@bp.route('/transfer', methods=['POST'])
@auth.login_required
def transfer_route():
    """ make a transfer """
    from_user = auth.current_user()
    content = request.get_json(silent=True)
    to_user = escape(content['to_user_id'])
    amount = content['amount']
    # todo input validation
    amount = float(amount)

    return make_transfer(from_user, to_user, amount)
