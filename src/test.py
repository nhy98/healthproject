from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

'''
ITEMS
'''
def test_read_error_item(id):
    response = client.get(f"/items/{id}")
    assert response.status_code == 404
    assert response.json() == {
            "data": "",
            "code": 404,
            "message": "Not Found Data"
        }


def test_create_item():
    response = client.post(
        "/items",
        json={
            "name": "onion",
            "quantity": 50
            })
    assert response.status_code == 201
    assert response.json() == {
        "data": {
            "name": "tomato",
            "quantity": 100,
            "created_date": 1633522232,
            "modified_date": 1633522232,
            "created_by": "shop owner",
            "modified_by": null,
            "id": "615dc47548fc69485cbf6705"
        },
        "code": 201,
        "message": "Created"
        }


def test_create_existing_item():
    response = client.post(
        "/items",
        json={
            "name": "tomato",
            "quantity": 100
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "data": "",
        "code": 1002,
        "message": "Duplicate Item. Can not insert again!"
        }

'''
ORDERS
'''
def test_create_order():
    response = client.post(
        "/orders",
        json={
        "user": "nhyen",
        "fruits": {
            "mango": 1,
            "apple": 1,
            "pineapple": 1
        }
    })
    assert response.status_code == 201
    assert response.json() == {
        "user": "nhyen",
        "fruits": {
            "mango": "1",
            "apple": "1",
            "pineapple": "1"
        },
        "created_date": 1633522232,
        "modified_date": 1633522232,
        "id": "615dc59548fc69485cbf6706"
        }


def test_create_order_not_enough_quantity():
    response = client.post(
        "/items",
        json={
        "user": "nhyen",
        "fruits": {
            "mango": 10,
            "pineapple": 1
        }
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "data": "",
        "code": 1001,
        "message": "There is not enough quantity for this item"
        }
