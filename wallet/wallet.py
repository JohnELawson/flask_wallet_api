from wallet.db import get_db
from typing import Mapping, Any
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import (
    Blueprint,
    request,
    jsonify,
    escape,
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

    # app.logger.debug(f"get_balance - balance: {balance}")
    return {
        "balance": wallet["value"],
        "currency": wallet["currency"]
    }


def get_transactions(username: str, limit: int = 10) -> Mapping[str, Any]:
    """ return users transactions """
    # app.logger.info(f"get_transactions - User: {username}, Limit: {limit}")

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
        # get receiver name
        receiver = db.execute("SELECT username FROM user WHERE id = ?", (row["receiver_id"],)).fetchone()

        data.append({
            "sender": row["username"],
            "receiver": receiver["username"],
            "date": row["created"],
            "value": row["value"],
            "currency": row["currency"],
        })

    # app.logger.debug(f"get_transactions - transactions: {trans}")
    return data


def make_transfer(from_username: str, to_user: str, amount: float) -> bool:
    """ pay a user """
    db = get_db()
    # from_user = db.execute(
    #     "SELECT *"
    #     " FROM wallet w JOIN user u ON w.user_id = u.id"
    #     " WHERE u.username = ?",
    #     (from_username,)
    # ).fetchone()
    # db.execute(
    #     "SELECT ",
    #     (title, body, g.user["id"]),
    # )
    # db.commit()

    # update from wallet
    # update to wallet
    # update transactions
    # todo roll back
    return True


@auth.verify_password
def verify_password(username, password):
    """ lookup auth to db """
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        error = "Incorrect username."
        # todo handle errors
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
    return get_balance(auth.current_user())


@bp.route('/transactions', methods=['GET'])
@auth.login_required
def transactions_route():
    limit = request.args.get('limit', 10)
    # todo check input
    limit = int(limit)

    return jsonify(list(get_transactions(auth.current_user(), limit)))


@bp.route('/transfer', methods=['POST'])
@auth.login_required
def transfer_route():
    from_user = auth.current_user()
    to_user = escape(request.form.get('to_user_id'))
    amount = request.form.get('amount')
    # todo input validation
    amount = float(amount)

    trans = make_transfer(from_user, to_user, amount)
    return f"{trans}"
