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
#import automationassets

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

def main():
    #cred = automationassets.get_automation_credential("chinsql")
    #username = cred["username"]     
   # password = cred["password"]
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=prd-chin.database.windows.net;DATABASE=Prd-MMCIX;UID=appforchin;PWD=FAn^u?9()!5s-}4n')    
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dev-shan.database.windows.net;DATABASE=Dev-MMCIX;UID=secondary;PWD=By$!S5FfrgmU8=TB')
    cursor = conn.cursor()
    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptStagClientFileStatus] active")
    results_activeclient = cursor.fetchall()
    file1 = datetime.now().strftime('activeclientfile-%Y-%m-%d-%H-%M.csv')
    with open(file1,'w',newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','Institution','Status','RecCount'])
        a.writerows(results_activeclient)

    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptStagClientFileStatus] writeoff")
    results_writeoff = cursor.fetchall()
    file2 = datetime.now().strftime('writeoff-%Y-%m-%d-%H-%M.csv')
    with open(file2,'w',newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','Institution','Status','RecCount'])
        a.writerows(results_writeoff)

    cursor.execute("SET NOCOUNT ON; EXEC [App].[RptMFILog]")
    results_mfilog = cursor.fetchall()
    file3 = datetime.now().strftime('mfilog-%Y-%m-%d-%H-%M.csv')
    with open(file3,'w',newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['CreateDate','MFILog'])
        a.writerows(results_mfilog)

    cursor.execute("SET NOCOUNT ON; EXEC [Client].[GetAccountStatistics]")
    results_percent = cursor.fetchall()
    file4 = datetime.now().strftime('80percent-%Y-%m-%d-%H-%M.csv')
    with open(file4,'w',encoding="utf-8",newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['MFIName','ClientCountAtSignUp','UploadCountLastMonth','UploadCount','80%','Status'])
        a.writerows(results_percent)
    # #cred1 = automationassets.get_automation_credential("outlook_credentials")
#     name = 'swezin.phyo@thitsaworks.com'    
#     passw = '499!ismylovE'
    
#     sender = name
#     #receiver = ['thynn.win@thitsaworks.com','waiphoo.ngon@thitsaworks.com','pye.aung@thitsaworks.com','aungmon.ko@thitsaworks.com','hnin.inzali@thitsaworks.com']
#     receiver = ['swezin.phyo@thitsaworks.com']
#     smtpsrv = "smtp.office365.com"

#     SUBJECT = 'MMCIX Subscription Notification Status ({0})'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
#     FILENAME = ['file1','file2','file3','file4']
#     FILEPATH = os.path.abspath("D:/szphyo/python_castle/python_chamber/generate_random_numbers")
#     msg = MIMEMultipart()
#     msg['From'] = sender
#     msg['To'] = COMMASPACE.join(receiver)
#     msg['Subject'] = SUBJECT
#     body ="""    Daily Status job schedule are processed successfully.
    
#     Regards,
#     MMCIX Team
#     """ 
#     body = MIMEText(body)
#     msg.attach(body)

#     part = MIMEBase('application', "octet-stream")
#     part.set_payload(open(r'D:\szphyo\python_castle\python_chamber\generate_random_numbers', "rb").read())
#     encoders.encode_base64(part)
#     for f in FILENAME:
#         part.add_header('Content-Disposition', 'attachment', filename=f)  # or
#         msg.attach(part)

#     smtpserver = smtplib.SMTP(smtpsrv,587)
#     smtpserver.ehlo()
#     smtpserver.starttls()
#     smtpserver.ehlo
#     smtpserver.login(sender, passw)
#     smtpserver.sendmail(sender, receiver, msg.as_string())
#     print('Successfully sent mail')
#     smtpserver.close()
    
if __name__ == '__main__':
    main()
    #sys.exit(0) 


