# Tech test
A wallet api

### How to run
Install requirements with `pip3 install -e .`
Set env vars `export FLASK_APP=wallet`
Init db with `flask init-db`
With with `flask run`

### Functionality
1) Query user name with `GET /wallet/`
Response: 
`Hello, john!`
2) Query users balance with `GET /wallet/balance` Response:
```
{
   "balance": 100.0,
   "currency": "SGD"
}
```
3) Query transactions with  `GET /wallet/transactions` or with a custom recent transaction limit `/transactions?limit=1` Response:
```
[
    {
        "currency": "SGD",
        "date": "Wed, 14 Oct 2020 19:38:30 GMT",
        "receiver": "sophie",
        "sender": "john",
        "value": 50.0
    }
]
```
4) Transfer funds to another user by `POST /wallet/transfer` with the following json content: 
```
{
    "amount": 23.12,
    "to_user_id": 2
}
```
Response:
```
{

}
```

All queries use HTTPBasicAuth. 