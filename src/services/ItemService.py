from services.MongoService import items
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
import json
from bson.objectid import ObjectId
from bson import json_util
from models import ItemModel, ResponseModel
from config import Constants
import logging

class ItemService:
    def parse_json(self, data):
        data = json.loads(json_util.dumps(data))
        if '_id' in data:
            id = data['_id']['$oid']
            data['id'] = id
            del data['_id']
        return data

    def create_item(self, data):
        try:
            # search existed item
            existed_item = self.get_item_by_name(data.name)
            if existed_item:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.DuplicateItem, Constants.ErrorCode.DuplicateItem))
            data.created_by = "shop owner"
            item = jsonable_encoder(data)

            new_item = items.insert_one(item)
            created_item = items.find_one({"_id": new_item.inserted_id})

            return JSONResponse(status_code=status.HTTP_201_CREATED, content=ResponseModel.ResponseModel(self.parse_json(created_item), Constants.ErrorMessage.Created, Constants.ErrorCode.Created))
        except Exception as ex:
            logging.exception(f"ItemService create_item exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

    def update_item(self, id, data):
        try:
            item = items.find_one({"_id": ObjectId(id)})
            if not item:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND
                , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.NotFound, Constants.ErrorCode.NotFound))

            for k in data:
                item[k] = data[k]

            if not item['modified_by']:
                item['modified_by'] = "shop owner"
            
            update_result = items.update_one({"_id": ObjectId(id)}, {"$set": item})
            if not update_result:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

            return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.Success, Constants.ErrorCode.Success))
        except Exception as ex:
            logging.exception(f"ItemService update_item exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

    def get_item(self, id):
        try:  
            if (item := items.find_one({"_id": ObjectId(id)})) is not None:
                return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel(self.parse_json(item), Constants.ErrorMessage.Success, Constants.ErrorCode.Success))

            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND
                , content=ResponseModel.ResponseModel(item, Constants.ErrorMessage.NotFound, Constants.ErrorCode.NotFound))
        except Exception as ex:
            logging.exception(f"ItemService get_item exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))


    def get_item_by_name(self, name):
        if (item := items.find_one({"name": name})) is not None:
            return self.parse_json(item)

        return {}
        
    def get_all_items(self):
        try:
            all_items = [self.parse_json(x) for x in items.find()]
            return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel(all_items, Constants.ErrorMessage.Success, Constants.ErrorCode.Success))
        except Exception as ex:
            logging.exception(f"ItemService get_all_items exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

    def delete_item(self, id):
        try:
            item = items.find_one({"_id": ObjectId(id)})
            if item:
                items.delete_one({"_id": ObjectId(id)})
                return JSONResponse(status_code=status.HTTP_200_OK, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.Success, Constants.ErrorCode.Success))
    
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND
                , content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.NotFound, Constants.ErrorCode.NotFound))
        except Exception as ex:
            logging.exception(f"ItemService delete_item exception: {ex}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ResponseModel.ResponseModel({}, Constants.ErrorMessage.InternalServerError, Constants.ErrorCode.InternalServerError))

