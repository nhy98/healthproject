from pydantic import BaseModel
from typing import Optional, List, Set, Dict
import uuid
import datetime
from bson import ObjectId
from models import ItemModel
from datetime import datetime

class OrderModel(BaseModel):
    """
    Order Model
    Created by: NHYEN
    Created at: 05/10/2021
    """
    user: str
    fruits: Dict[str, str]
    created_date: Optional[int] = int(datetime.now().timestamp())
    modified_date: Optional[int] = int(datetime.now().timestamp())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user": "nhyen",
                "fruits": {
                    "mango": 1,
                    "apple": 1,
                    "pineapple": 1
                }
            }
        }
