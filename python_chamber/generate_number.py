'''Python script to generate ID randomly
    - range() - the number of rows you want to generate
    - using random.randint() - the number between to insert 
- get db connect and insert them in the table
min - 001001001 in production'''
import pyodbc
import random
import sys
import datetime

#import automationassets
DATE_TIME = datetime.datetime.now()

# def _get_credential():
#     '''
#     use automationassets module to get credentials from azure (secure the password and username)
#     '''
#     cred = automationassets.get_automation_credential("dev-inle")
#     username = cred["username"]
#     password = cred["password"]
#     return username,password


def _generate_checksum(rand_num):
    """input - 9digits generated numbers
     output - 1digit checksum based on input digits
     """
    digit=0
    const_num = 234567189
    temp_num1=const_num+int(rand_num) #sum
    for d in str(temp_num1):
        digit=digit+int(d)
    
    #print('Sum is ',digit)
    temp_num1=int(digit*3)  #multiply with 3
        
    binary=bin(temp_num1) #change binary
    #print('Binary Number is',binary)
        
    temp_num1=int(bin(temp_num1>>1),2) #right shift and change to decimal
    #print('Right Shift Decimal is',temp_num1)

    shifted_num=temp_num1
    #print('Right Shift Digit is',(int(temp_num1/10)))

    checksum_num=shifted_num%10
    return checksum_num

def generate_random_numbers(conn, cursor):

    '''
    - range() - the number of rows you want to generate
    - using random.randint() - the number between to insert 
    - insert the numbers into the table
    '''

    for ran in range(0,10):
        raw_random = "%0.9d" % random.randint(1,999999999)
        print(raw_random)
        flag = 0
        try:
            if '000' not in raw_random:
                print('insert')
                #insert the raw_random if doesn't contain 3 consecutive zeros
                #create main_identifiers = checksum (_generate_checksum)+9digits from random
                main_identifiers = "{0}{1}".format(_generate_checksum(raw_random),raw_random)
                cursor.execute('''
                    INSERT INTO [Person].[RandomNumbers](value,MainIdentifier,is_taken,Createddtm) VALUES(?,?,?,?)''',raw_random,main_identifiers,flag,DATE_TIME)
                conn.commit()
        except pyodbc.IntegrityError:
            print('duplicate, not inserted')
    print("Insert done! ")

def main():
    #get db connect and insert them in the table
    # driver = '{ODBC Driver 17 for SQL Server}'

    #TO MAKE UNCMT THESE WHEN RUN IN AZURE AUTOMATION
    #username,password = _get_credential()
    #conn = pyodbc.connect("DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}".format(driver,host,db,username,pwd))
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=xxxxx;DATABASE=xxxx;UID=xxxx;PWD=xxxxxx')

    cursor = conn.cursor()
    # cursor.execute("select MAX(value) from person.RandomNumbers;")
    # raw_max = cursor.fetchone()

    # #start is the max value in random 
    # start = int(raw_max[0]) + 1
    # end = int(start) + int(10)

    #generate_random_numbers(conn,cursor,start,end)
    generate_random_numbers(conn,cursor)

if __name__ == '__main__':
    main()
    sys.exit(0) 

