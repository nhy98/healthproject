
## Install Instruction
Modify database connection string in /src/config/config.yaml file.
Restore database from filed placed in /healthprojectdb.

```
Install mongoclient

wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

Restore Database

mongorestore --uri="mongodb://[username]:[password]@[host]:[port]/?authSource=[authendb]" [filepath]
```
The demo app can be run as following:

```
cd ./src
pip -r install requirements.txt
uvicorn app:app --reload
```

The examples and demo app can also be built and run as a Docker image/container:

```
docker build -t healthproject:1.0.0 .
docker run -p 9090:80 --name heathproject healthproject:1.0.0
```


> NOTE: Access API swagger (http://localhost:9090/health-service/api/v1/docs)
                            (http://localhost:9090/health-service/api/v1/redoc)
# API Specification

1. Items
- /items [GET] : Get all items.
- /items/{id} [GET]: Get an item by id.
- /items [POST]: Create an item.
- /items/{id} [PUT]: Update an item by id.
- /items/{id} [DELETE]: Delete an item by id.
2. Orders
- /orders [GET]: Get all orders.
- /orders/{id} [GET]: Get an order by id.
- /orders [POST]: Create an order.
- /orders/history/{username} [GET]: Get all orders by username.

# Error Code
200 | Success
201 | Created
404 | Not Found
500 | Internal Server Error
1001| There is not enough quantity for this item
1002| Duplicate Item. Can not insert again!


