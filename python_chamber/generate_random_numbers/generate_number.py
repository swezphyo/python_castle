'''Python script to generate ID randomly
- using range() to get all numbers between range
- using random.shuffle() to shuffle the numbers from the range function
- get db connect and insert them in the table'''
import pyodbc
import random
import sys
from configparser import ConfigParser

CONFIG_FILE = "config.ini"

def _load_config(config_file):
    """Load configs from files
    """
    config = None
    try: 
        config = ConfigParser()
        if len(config.read(config_file)) == 0:
            print("Config file [%s] is empty or not found" % config_file)
            config = None
        print("Config file loaded")
    except:
        print("Cannot load config file[%s]" %config_file)
    return config

def generate_random_numbers(conn, cursor):
    '''
    - using range() to get all numbers between range
    - using random.shuffle() to shuffle the numbers from the range function
    - insert the numbers into the table
    '''
    raw_list = list(range(0,50))
    #print ("Original list : ",  raw_list)
    random.shuffle(raw_list) #shuffle method
    print ("List after first shuffle  : ",  raw_list)
    for i in raw_list:
        insert_raw = "%0.7d" % i
        #print(insert_raw)
        cursor.execute('''
            INSERT INTO [dbo].[RandomNumbers](value) VALUES(?)''',insert_raw)
        conn.commit()
    print("Insert done! ")

def main():
    #get db connect and insert them in the table
    config = _load_config(CONFIG_FILE)
    if config is None:
        sys.exit(0)

    driver = '{ODBC Driver 17 for SQL Server}'
    host = config.get("sqldb", "host")
    db = config.get("sqldb", "auth_db")
    username = config.get("sqldb", "auth_user")
    pwd = config.get("sqldb", "auth_pwd")

    conn = pyodbc.connect("DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}".format(driver,host,db,username,pwd))
    cursor = conn.cursor()
    generate_random_numbers(conn,cursor)


if __name__ == '__main__':
    main()
    sys.exit(0) 

