# import pytest
# from base64 import b64encode
#
#
# def test_hello(client):
#     credentials = b64encode(b"john:pass1").decode('utf-8')
#     response = client.get('/wallet', headers={"Authorization": f"Basic {credentials}"})
#     assert response.data == b'Hello, john!'
#
