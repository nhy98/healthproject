from pydantic import BaseModel
from typing import Optional
import uuid
from bson import ObjectId
from datetime import datetime

class ItemModel(BaseModel):
    """
    Item Model
    Created by: NHYEN
    Created at: 05/10/2021
    """
    name: str
    quantity: int
    created_date: Optional[int] = int(datetime.now().timestamp())
    modified_date: Optional[int] = int(datetime.now().timestamp())
    created_by: Optional[str]
    modified_by: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "apple",
                "quantity": 10
            }
        }
