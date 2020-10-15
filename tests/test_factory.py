from wallet import create_app
from base64 import b64encode


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


# def test_hello(client):
#     credentials = b64encode(b"john:pass1").decode('utf-8')
#     response = client.get('/wallet', headers={"Authorization": f"Basic {credentials}"})
#     assert response.data == b'Hello, john!'
