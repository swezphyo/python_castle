"""
Azure Automation documentation : https://aka.ms/azure-automation-python-documentation
Azure Python SDK documentation : https://aka.ms/azure-python-sdk

Python script to get data from sql server's procedure and write to csv and send mail
"""
import pyodbc
import random
import sys
import csv
import smtplib
import os
import glob
import codecs
from io import open
from datetime import datetime
import automationassets

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

def encode(y):
    """
    encode y with utf-8 to write in csv file (in case there are unicode in database execution)
    """
    if type(y) is str:
        en_y = y.encode('utf-8')
        return en_y
    else:
        return y

def strip_data(lst):
    """
    manual stipping data record for pretty output
    """
    res1 = str(lst).strip('(u')
    res2 = res1.strip('L)')
    return res2

def main():
    """mail loop to execute data and attach to mail and send the mail
    """
    #use automationassets to get credentials 
    cred = automationassets.get_automation_credential("xxxx")
    username = cred["username"]     
    password = cred["password"]
    driver = '{SQL Server}'
    
    #declare database connection
    conn = pyodbc.connect('DRIVER={0};SERVER=xxxxx;DATABASE=xxxxx;UID={1};PWD={2}'.format(driver,username,password))    
    cursor = conn.cursor()

    #execute [App].[RptStagClientFileStatus] procedure and write to csv file
    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptStagClientFileStatus] active")
    results_activeclient = cursor.fetchall()
    activecsv = datetime.now().strftime('activeclientfile-%Y-%m-%d-%H-%M.csv')
    with open(activecsv,'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','Institution','Status','RecCount'])
        a.writerows(results_activeclient)

    #execute [App].[RptStagClientFileStatus] procedure and write to csv file
    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptStagClientFileStatus] writeoff")
    results_writeoff = cursor.fetchall()
    writeoffcsv = datetime.now().strftime('writeoff-%Y-%m-%d-%H-%M.csv')
    with open(writeoffcsv,'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','Institution','Status','RecCount'])
        a.writerows(results_writeoff)

    #execute [App].[RptMFILog] procedure and write to csv file
    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptMFILog]")
    results_mfilog = cursor.fetchall()
    mficsv = datetime.now().strftime('mfilog-%Y-%m-%d-%H-%M.csv')
    with open(mficsv,'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','MFILog'])
        a.writerows(results_mfilog)

    #execute [Client].[GetAccountStatistics] procedure and write to csv file    
    cursor.execute("SET NOCOUNT ON; EXEC [Client].[GetAccountStatistics]")
    results_percent = cursor.fetchall()
    #create row_as_list for encoding process (changed pyodbc.Row to list data type)
    row_as_list = [x for x in results_percent]
    rawlist = list()
    #create rawlist to build manually list of pyodbc row for easily write to csv
    for x in row_as_list:
        lst2 = list()
        for y in x:
            res=encode(y)
            lst2.append(res)
        rawlist.append(lst2)

    percentcsv = datetime.now().strftime('80percent-%Y-%m-%d-%H-%M.csv')
    with codecs.open(percentcsv,'wb',encoding='utf-8') as fp:
        a = csv.writer(fp, delimiter=',')
        header = ['MFIName','ClientCountAtSignUp','UploadCountLastMonth','UploadCount','80%','Status']
        a.writerow(header)
        a.writerows(rawlist)
       
    #Execute [App].[RptDailyStatusSummary] and show in body of mail
    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptDailyStatusSummary]")
    summary = cursor.fetchall()
    #get summary data to show in mail's body
    sum1 = strip_data(summary[0])
    sum2 = strip_data(summary[1])
    sum3 = strip_data(summary[2])
    sum4 = strip_data(summary[3])
    sum5 = strip_data(summary[4])
    sum6 = strip_data(summary[5])
    sum7 = strip_data(summary[6])

    csvlist = list()
    for file in glob.glob("*.csv"):
        csvlist.append(file)

    #credentials of sender's address   
    cred1 = automationassets.get_automation_credential("RunBookEmailCred")     
    name = cred1["username"]   
    passw = cred1["password"]

    sender = name
    receiver = xxxxxxxx
    smtpsrv = "smtp.office365.com"

    SUBJECT = 'MMCIX Daily Status ({0})'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    #get the location of the script 
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    #build mail's body
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receiver)
    msg['Subject'] = SUBJECT
    b1 = 'Daily Status job schedule are processed successfully.'
    b2 = 'Daily Status Summary'
    btle = 'Title, Record'
    body ="""
    {0}

    {1}

    {2}
    {3}
    {4}
    {5}
    {6}
    {7}
    {8}
    {9}

    Regards,
    MMCIX Team

    """.format(b1,b2,btle,sum1,sum2,sum3,sum4,sum5,sum6,sum7)
    body = MIMEText(body)
    msg.attach(body)
    #attach multiple csv in csvlist
    for f in csvlist:
        #file_path = os.path.join(FILEPATH, f)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=f)  # or
        msg.attach(part)

    smtpserver = smtplib.SMTP(smtpsrv,587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(sender, passw)
    smtpserver.sendmail(sender, receiver, msg.as_string())
    print 'Successfully sent mail'
    smtpserver.close()

    
if __name__ == '__main__':
    main()
    #sys.exit(0) 
