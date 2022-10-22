from ast import Raise
import collections
from bson.objectid import ObjectId
from pymongo import MongoClient, database, ReturnDocument
from pymongo.errors import ConnectionFailure,ServerSelectionTimeoutError,NetworkTimeout,ExecutionTimeout,InvalidURI,OperationFailure
from logic import update_nested
import os

MONGO_ID_FIELD = "_id"

def get_first_data(api,name,version):
    results = get_all_collection_with_raw_objects_exists(api,name,version)
    if len(results) > 0:
        result = results[0]
        id = get_object_id(result)
        data = extract_data(result)
        overrides = result.get('overrides')
        re_override = result.get('re-override', False)
        if overrides != None:
            update_nested(data, overrides, re_override)
        return data, id
    return {}, None
    
def get_all_collection_objects(api):
    docs = get_all_collection_with_raw_objects_exists(api, None, None)
    return func_on_dict(docs, remove_object_id)

def get_all_collection_data(api):
    docs = get_all_collection_objects(api)
    return func_on_dict(docs, extract_data)

# This is added so that many files can reuse the function get_database()
def get_all_collection_raw_objects(api,name,version):  
    # Get the database
    collectionName = get_collection(api)
    try:
        results = collectionName.find(create_filter(name,version))
        resultsList = list(results)
        return resultsList
    except (ServerSelectionTimeoutError, ConnectionFailure, NetworkTimeout, ExecutionTimeout, InvalidURI):
        raise Exception('DB timeout, maybe it\'s offline',500)

def get_all_collection_with_raw_objects_exists(api,name,version):
    resultsList = get_all_collection_raw_objects(api,name,version)
    if (len(resultsList) == 0):
        raise Exception('The is not collection in {0} with the name {1} and version {2}'.format(api,name,version),404)
    return resultsList

def insert_data(api,name,version, data):
    collectionName = get_collection(api)
    dit:dict = {}
    dit['name'] = name
    dit['version'] = version
    dit['data'] = data

    resultsList = get_all_collection_raw_objects(api,name,version)
    if (len(resultsList) == 0):
        result = collectionName.insert_one(dit)
        id = result.inserted_id
    else:
        id = resultsList[0][MONGO_ID_FIELD]
        update_data(api, id, data, False, True)
    return str(id)

def update_data(api, id, data, re_override: bool = False, isUpsert : bool = False, isReturnDocument : ReturnDocument = ReturnDocument.AFTER):
    try:
        collection = get_collection(api)
        return collection.find_one_and_update({MONGO_ID_FIELD: ObjectId(id)}, {'$set': {'data': data, 're-override': re_override}}, upsert = isUpsert, return_document = isReturnDocument)
    except Exception as err:
        raise Exception('Failed to update the item ', err)

def get_collection(api) -> database.Collection:
    return db[api]

def get_database() -> database.Database :
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.getenv('MONGO_CONNECTION')
    if (CONNECTION_STRING == None):
        CONNECTION_STRING = "mongodb://localhost:27017"
        # mongodb://localhost:27017/

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING,  serverSelectionTimeoutMS=5000)

    # Create the database for our example (we will use the same database throughout the tutorial
    DB_NAME = os.getenv('MONGO_DB_NAME')
    if (DB_NAME == None):
        DB_NAME = 'Shimon'
    try:
        if DB_NAME not in client.list_database_names():
            raise Exception('DB {0} does not exist!'.format(DB_NAME))
    except (ServerSelectionTimeoutError, ConnectionFailure) as err:
        raise Exception('Failed to connet to the DB ', err)
    return client[DB_NAME]
   
def func_on_dict(docs:list, func):
    for doc in docs:
        func(doc)
    return docs


def extract_data(dic:dict):
    return dic['data']

def extract_overrides(dic:dict):
    if 'overrides' in dic:
        return dic['overrides']
    return None

def remove_object_id(doc:dict):
    doc.pop(MONGO_ID_FIELD)

def get_object_id(doc:dict):
    return doc[MONGO_ID_FIELD]

def create_filter(name:str,version:str):
    customFilter = {}
    if (name):
        customFilter['name'] = name
    if (version):
        customFilter['version'] = version

    return customFilter

try:
    db = get_database()
except Exception as err:
    print("Connection to the DB have failed! ", err)
    raise
