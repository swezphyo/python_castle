'''
Python script to get data from sql server's procedure and write to csv and send mail
'''
import pyodbc
import random
import sys
import csv
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


def main():
    get db connect and insert them in the table
    config = _load_config(CONFIG_FILE)
    if config is None:
        sys.exit(0)

    driver = '{ODBC Driver 17 for SQL Server}'
    host = config.get("sqldb", "host")
    db = config.get("sqldb", "auth_db")
    username = config.get("sqldb", "auth_user")
    pwd = config.get("sqldb", "auth_pwd")
    params = 1

    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server},SERVER=xxxx')
    cursor = conn.cursor()
    results = cursor.execute("SET NOCOUNT ON; EXEC [App].[RptExpiringSubscription] 1")
    results = cursor.fetchall()
    #print(results) #list_type
    with open('data.csv','w',newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['Name','Start Date','End Date'])
        a.writerows(results)
        
if __name__ == '__main__':
    main()
    sys.exit(0) 
