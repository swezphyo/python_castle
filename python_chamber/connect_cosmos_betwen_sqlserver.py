import pydocumentdb
import pydocumentdb.document_client as document_client

import pyodbc
import sys
import re
import datetime

DATE_TIME = datetime.datetime.now()

def _pair_nrc(raw_nrc):
    """
    use the raw_nrc from cosmos to find in MCIX Person table
    if nrc is already existed - insert into BorrowerExternalInfo
    if not = exit
    """ 
    fetch_nrc_list = list()
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=xxxxx;DATABASE=xxxxx;UID=xxxx;PWD=xxxxxx')
    cursor = conn.cursor()
    cursor.execute(" SELECT [PersonGUID] FROM [Person].[Person] where Full_NRC = '{0}';".format(raw_nrc))
    result_person = cursor.fetchall()    
    if not result_person:
        print("Not Matched\n")
    else:
        for res in result_person:
            #find the coming puid is already existed in table
            cursor.execute("SELECT top(5) [PersonGUID] From [dbo].[BorrowerExternalInfo] where PersonGUID=?",res.PersonGUID)
            fetch_puid = cursor.fetchall()
            #fetch_nrc_list is to record the puid coming from cursor 
            for _puid in fetch_puid:
                fetch_nrc_list.append(str(_puid))
            if fetch_puid is not None:
                #The coming PUID is new 
                _newpuid = "('" + res.PersonGUID + "', )"
                if _newpuid not in fetch_nrc_list:
                    print("Matched... Go to insert BorrowerExternalInfo\n")
                    cursor.execute('''
                                    INSERT INTO [dbo].[BorrowerExternalInfo](PersonGUID,CreatedDtm)
                                    VALUES(?,?)''',res.PersonGUID,DATE_TIME)
                    conn.commit()
    
def _connect_cosmos():
    """
    Fetch nrc data from Azure cosmos db and pass it to pair_nrc to check whether it is existed in MCIX Person table or not
    """
    #to test this "ded56dbb-0ad5-4555-54c0-cad94521bc16" and "56e0f9ac-0354-077b-e613-a23f5fb485e4" when connect with sql as it's nrc is in english
    config = {
        'ENDPOINT': 'xxxxxxxxx',
        'MASTERKEY': 'xxxxxxxxxxxxxx',
        'DOCUMENTDB_DATABASE': 'xxxxxx',
        'DOCUMENTDB_COLLECTION': 'xxxxx'
    };

    # Initialize the Python DocumentDB client
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    s_id = ['121ad45f-a278-3218-d2ba-63aaccd1fbab','2133173546727533-1957854191126003,2133173546727533',"2103324929678753-1957854191126003,2103324929678753","2152048201484081-1957854191126003,2152048201484081","5ee1dded-e677-4a45-6717-979fdc21dcde","56e0f9ac-0354-077b-e613-a23f5fb485e4","ded56dbb-0ad5-4555-54c0-cad94521bc16"]
    # use a SQL based query to get a bunch of documents
    for s in s_id:
        query = { 'query': 'SELECT * FROM server s where s.id = "{0}"'.format(s)}
        print(query)
        options = {}
        options['enableCrossPartitionQuery'] = True
        options['maxItemCount'] = 2 
        cosmosdata_iterable = client.QueryDocuments('dbs/pitepiteDB/colls/pitepiteCollection', query, options)
        raw_cosmos_data = list(cosmosdata_iterable);
        # print(raw_cosmos_data) #output will be json format of stored data based on query
        for i in raw_cosmos_data: 
            #need to check where the NRC is stored in json (has different keys)
            if 'data' in i:
                if 'la_ui_nrc_number' in i['data']:
                    raw_nrc = i['data'].get('la_ui_nrc_number')
                    #print("The NRC found is {0}".format(raw_nrc))
                    _pair_nrc(raw_nrc)
            elif 'La' in i:
                if 'la_ui_nrc_number' in i['La']:
                    raw_nrc = i['La'].get('la_ui_nrc_number')
                    #print("The NRC found is {0}".format(raw_nrc))
                    _pair_nrc(raw_nrc)
            elif 'conversation' in i:
                if 'la_ui_nrc_number' in i['conversation']:
                    raw_nrc = i['conversation'].get('la_ui_nrc_number') 
                    #print("The NRC found is {0}".format(raw_nrc))
                    _pair_nrc(raw_nrc)
            else:
                print('No NRC found')
                print('\n')

def main():
    _connect_cosmos()

if __name__ == '__main__':
    main()
