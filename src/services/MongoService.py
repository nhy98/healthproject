from pymongo import MongoClient
from config import Config

cfg = Config.get_config()

client = MongoClient(cfg['database']['url'])

db = client[cfg['database']['db_name']]

items = db.get_collection(cfg['database']['item_col'])
orders = db.get_collection(cfg['database']['order_col'])
