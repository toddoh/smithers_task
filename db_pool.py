from pymongo import MongoClient
import config_secrets

def init_db():
    client = MongoClient(config_secrets.FN_MONGODBURI)
    db = client['smithers']

    return db