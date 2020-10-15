import pytest
import json
from base64 import b64encode


def test_hello(client):
    credentials = b64encode(b"john:pass1").decode('utf-8')
    response = client.get('/wallet/', headers={"Authorization": f"Basic {credentials}"})
    assert response.data == b'Hello, john!'
    assert response.status_code == 200


def test_balance(client):
    credentials = b64encode(b"john:pass1").decode('utf-8')
    response = client.get('/wallet/balance', headers={"Authorization": f"Basic {credentials}"})
    assert json.loads(response.data) == {
        "balance": 100.00,
        "currency": "SGD"
    }
    assert response.status_code == 200


def test_balance_diff_user(client):
    credentials = b64encode(b"sophie:pass2").decode('utf-8')
    response = client.get('/wallet/balance', headers={"Authorization": f"Basic {credentials}"})
    assert json.loads(response.data) == {
        "balance": 50.00,
        "currency": "SGD"
    }
    assert response.status_code == 200


def test_get_transactions_none(client):
    credentials = b64encode(b"sophie:pass2").decode('utf-8')
    response = client.get('/wallet/transactions', headers={"Authorization": f"Basic {credentials}"})
    assert json.loads(response.data) == []
    assert response.status_code == 200


def test_get_transactions(client):
    credentials = b64encode(b"john:pass1").decode('utf-8')
    response = client.get('/wallet/transactions', headers={"Authorization": f"Basic {credentials}"})
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["currency"] == "SGD"
    assert data[0]["receiver"] == "sophie"
    assert data[0]["sender"] == "john"
    assert data[0]["value"] == 50.0
    assert data[1]["currency"] == "SGD"
    assert data[1]["receiver"] == "sophie"
    assert data[1]["sender"] == "john"
    assert data[1]["value"] == 12.01
    assert response.status_code == 200


def test_get_transactions_with_limit(client):
    credentials = b64encode(b"john:pass1").decode('utf-8')
    response = client.get('/wallet/transactions?limit=1', headers={"Authorization": f"Basic {credentials}"})
    data = json.loads(response.data)
    assert len(data) == 1
    assert response.status_code == 200