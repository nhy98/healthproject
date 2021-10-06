from services.MongoService import orders
from fastapi.encoders import jsonable_encoder
from fastapi import status
import json
from bson.objectid import ObjectId
from bson import json_util
from services.ItemService import ItemService
from datetime import datetime
from config import Constants
from fastapi.responses import JSONResponse
from models import OrderModel, ResponseModel
import logging

class OrderService:
    """
    Order Service
    Created by: NHYEN
    Created at: 05/10/2021
    """
    def parse_json(self, data):
        data = json.loads(json_util.dumps(data))
        if '_id' in data:
            id = data['_id']['$oid']
            data['id'] = id
            del data['_id']
        return data

    def create_order(self, data):
        try:
            update_item = []
            # check fruits stock
            items = ItemService()
            for fi in data.fruits:
                it = items.get_item_by_name(name=fi)
                if not it:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND
                        , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.NotFound, Constants.ErrorCode.NotFound))


                if it['quantity'] < int(data.fruits[fi]):
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                        , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.NotEnough, Constants.ErrorCode.NotEnough))


                it['modified_by'] = "customer"
                it['quantity'] -= int(data.fruits[fi])
                it['modified_date'] = int(datetime.now().timestamp())

                update_item.append(it)
            # update fruits stock
            for it in update_item:
                tmp_id = it['id']
                del it['id']
                res = items.update_item(tmp_id, it)
                if not res:
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                        , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

            order = jsonable_encoder(data)
            new_order = orders.insert_one(order)
            created_order = orders.find_one({"_id": new_order.inserted_id})
            
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=self.parse_json(created_order))
        except Exception as ex:
            logging.exception(f"OrderService create_order exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))


    def get_order(self, id):
        try:
            if (order := orders.find_one({"_id": ObjectId(id)})) is not None: 
                return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel(self.parse_json(order), Constants.ErrorMessage.Success, Constants.ErrorCode.Success))

            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND
                        , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.NotFound, Constants.ErrorCode.NotFound))
        except Exception as ex:
            logging.exception(f"OrderService get_order exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

    def get_all_order(self):
        try:
            all_orders = [self.parse_json(x) for x in orders.find()]
            return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel(all_orders, Constants.ErrorMessage.Success, Constants.ErrorCode.Success))
        except Exception as ex:
            logging.exception(f"OrderService get_all_order exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

    def get_order_history(self, user):
        try:
            list_order = orders.find({ "user": user})
            res = []
            for o in list_order:
                o = self.parse_json(o)
                res.append({
                    o['created_date']: o['fruits']
                })

            return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel(res, Constants.ErrorMessage.Success, Constants.ErrorCode.Success))

        except Exception as ex:
            logging.exception(f"OrderService get_order_history exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

