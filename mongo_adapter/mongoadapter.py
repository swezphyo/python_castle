#
# CRUD operations to mongodatabase through Pymongo module
# REQUIRES (TEST_DB)
#
import os
import sys
import logging


from configparser import ConfigParser

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import OperationFailure

from contextlib import contextmanager

CONFIG_FILE = "config.ini"

def _load_config(config_file):
    """Load configs from files
    """
    config = None
    try:
        config = ConfigParser()
        if len(config.read(config_file)) == 0:
            #logging.error("Config file [%s] is empty or not found" % config_file)
            print("Config file [%s] is empty or not found" % config_file)
            config = None
        #logging.info("Config file loaded") 
        print("Config file loaded")
    except:
        print("Cannot load config file[%s]" %config_file)
        #logging.error("Cannot load config file [%s]" % config_file)
    return config

@contextmanager
def _connect_mongodb(config):
    """Connect to testdb
    """
    db_host = config.get("testdb", "host")
    db_port = config.get("testdb", "port")
    db_auth = config.get("testdb", "auth_db")
    db_auth_user = config.get("testdb", "auth_user")
    db_auth_pwd = config.get("testdb", "auth_pwd")
    db_selection_timeout = config.get("testdb", "selection_timeout")
    db_socket_timeout = config.get("testdb", "socket_timeout")
    db_connect_timeout = config.get("testdb", "connect_timeout")
    dbclient = pymongo.MongoClient("mongodb://{0}:{1}/{2}?serverSelectionTimeoutMS={3}&socketTimeoutMS={4}&connectTimeoutMS={5}".format(
                                    db_host,db_port,db_auth,db_selection_timeout,db_socket_timeout,db_connect_timeout))
    #dbclient = pymongo.MongoClient("mongodb://{0}:{1}@{2}:{3}/{4}?serverSelectionTimeoutMS={5}&socketTimeoutMS={6}&connectTimeoutMS={7}".format(
                                    #db_auth_user, db_auth_pwd, db_host, db_port, db_auth, db_selection_timeout, db_socket_timeout, db_connect_timeout))
    try:
        dbclient.admin.command("ismaster")
        logging.info("Mongo: DB Connected")
    except ServerSelectionTimeoutError:
        #logging.error("Mongo: Database connection failed. ServerSelectionTimedOut")
        print("Mongo: Database connection failed. ServerSelectionTimedOut")
        dbclient = None
    except ConnectionFailure:
        print("Mongo: Database connection failed. Connection Failure")
        #logging.error("Mongo: Database connection failed. Connection Failure")
        dbclient = None
    except OperationFailure:
        print("Mongo: Database connection failed. Authentication Failed")
        #logging.error("Mongo: Database connection failed. Authentication Failed")
        dbclient = None
    except:
        print(traceback.format_exc())
        #logging.error(traceback.format_exc())
    yield dbclient
    _close_db(dbclient)
    print("Connection closed")
    #logging.info("MongoDB : DB connection closed")

def _close_db(db):
    if db is not None:
        try:
            db.close()
        except:
            pass
    return

def insert_documents(config):
    with _connect_mongodb(config) as mongodb_client:
        if not mongodb_client:
            return
        #connect mydatabase (db)
        testdb = mongodb_client.mydatabase
        #initialize the collection to use in db(mydatabase)
        mycol = testdb.customers
        mylist = [
          { "name": "Amy", "address": "Apple st 652"},
          { "name": "Hannah", "address": "Mountain 21"},
          { "name": "Michael", "address": "Valley 345"},
          { "name": "Sandy", "address": "Ocean blvd 2"}
        ]

        x = mycol.insert_many(mylist)
        #print list of the _id values of the inserted documents:
        print(x.inserted_ids) 

def main():
    config = _load_config(CONFIG_FILE)
    if config is None:
        sys.exit(0)

    insert_documents(config)
    # fileConfig('logging_config.ini')
    # logger = logging.getLogger()
    # logging.info("------LOGGING Started!! ----------")
    
if __name__ == '__main__':
    main()
    sys.exit(0)