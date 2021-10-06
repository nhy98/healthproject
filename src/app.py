from fastapi import FastAPI, status, Body, APIRouter
import uvicorn
from typing import List
from config import Config, Constants
from models import ItemModel, OrderModel, ResponseModel
from fastapi.encoders import jsonable_encoder
from services import ItemService, OrderService
from fastapi.responses import JSONResponse


cfg = Config.get_config()
temp = APIRouter()

app = FastAPI(
    title=cfg['app']['title'],
    description=cfg['app']['description'],
    version=cfg['app']['version'],
    docs_url=cfg['app']['docs'],
    redoc_url=cfg['app']['redoc']
)


@app.get("/")
@app.get("/healthz")
def get_healthz():
    return {
        "code": 200,
        "version": cfg['app']['version'],
        "maintainer": "nhyen",
        "description": cfg['app']['description']
    }

'''
ITEM
'''
@app.post("/items", response_description="Add new item")
async def create_item(data: ItemModel.ItemModel = Body(...)):
    items = ItemService.ItemService()
    return items.create_item(data)
    

@app.get(
    "/items", response_description="List all items", response_model=List[ItemModel.ItemModel]
)
async def list_all_items():
    items = ItemService.ItemService()
    return items.get_all_items()


@app.get(
    "/items/{id}", response_description="Get a single item"
)
async def get_item(id: str):
    items = ItemService.ItemService()
    return items.get_item(id)
    

@app.put("/items/{id}", response_description="Update an item")
async def update_item(id: str, data: ItemModel.ItemModel = Body(...)):
    req = {k: v for k, v in data.dict().items() if v is not None}
    items = ItemService.ItemService()
    return items.update_item(id, req)
    

@app.delete("/items/{id}", response_description="Delete an item")
async def delete_item(id: str):
    items = ItemService.ItemService()
    return items.delete_item(id)
    

'''
ORDER
'''
@app.post("/orders", response_description="Add new order")
async def create_order(data: OrderModel.OrderModel = Body(...)):
    orders = OrderService.OrderService()
    return orders.create_order(data)


@app.get(
    "/orders", response_description="List all orders"
)
async def list_all_orders():
    orders = OrderService.OrderService()
    return orders.get_all_order()


@app.get(
    "/orders/{id}", response_description="Get a single order"
)
async def get_order(id: str):
    orders = OrderService.OrderService()
    return orders.get_order(id)

@app.get(
    "/orders/history/{user}", response_description="Get order history"
)
async def get_order_history(user: str):
    orders = OrderService.OrderService()
    return orders.get_order_history(user)

app.include_router(temp, prefix='/health-service/api/v1')

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
