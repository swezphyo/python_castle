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
from datetime import datetime
import automationassets

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

def main():
    #cred = automationassets.get_automation_credential("chinsql")
    #username = cred["username"]     
   # password = cred["password"]
    
    #create database connection to connect mysql server with pyodbc
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=xxxx;DATABASE=xxx;UID=username;PWD=password')    
    cursor = conn.cursor()

    #query for procedure execution
    results = cursor.execute("SET NOCOUNT ON; EXEC [test]")
    results = cursor.fetchall()

    #declare csv file to write
    file = datetime.now().strftime('subscription_notification-%Y-%m-%d-%H-%M.csv')
    with open(file,'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['Name','Start Date','End Date'])
        a.writerows(results)

    #sender's mail credentials    
    sender = name
    receiver = ['xxxx@thitsaworks.com','wwww@thitsaworks.com']
    smtpsrv = "smtp.office365.com"

    SUBJECT = 'Notification Status ({0})'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    FILENAME = file
    FILEPATH = file
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receiver)
    msg['Subject'] = SUBJECT
    body ="""    Status
    """ 
    body = MIMEText(body)
    msg.attach(body)

    part = MIMEBase('application', "octet-stream")
    #attach single csv file to mail 
    part.set_payload(open(FILEPATH, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
    msg.attach(part)

    smtpserver = smtplib.SMTP(smtpsrv,587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(sender, passw)
    smtpserver.sendmail(sender, receiver, msg.as_string())
    print('Successfully sent mail')
    smtpserver.close()
    
if __name__ == '__main__':
    main()
    #sys.exit(0) 


