"""
Python3 script to send mail with multiple csvs attached (smtp) from outlook account
"""
import sys
import csv
import smtplib
import os
import glob
from datetime import datetime
#import automationassets

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


#to get the current filepath
#print(os.path.dirname(os.path.abspath(__file__)))
#print(os.listdir())

#glob - to catch all file in location of script located
csvlist = list()
for file in glob.glob("*.csv"):
    csvlist.append(file)
# print(csvlist)

#declare name and password credentials 
name = mail  
passw = password

sender = name
receiver = ['sxxx@outlook.com']
smtpsrv = "smtp.office365.com"

SUBJECT = 'Status'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
FILEPATH = os.path.dirname(os.path.abspath(__file__))

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = COMMASPACE.join(receiver)
msg['Subject'] = SUBJECT
body ="""schedule are processed successfully.
""" 
body = MIMEText(body)
msg.attach(body)

#attach multiple csvs to mail
for f in csvlist:
    file_path = os.path.join(FILEPATH, f)
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=f)  # or
    msg.attach(part)

#declare smtpserver
smtpserver = smtplib.SMTP(smtpsrv,587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(sender, passw)
smtpserver.sendmail(sender, receiver, msg.as_string())
print('Successfully sent mail')
smtpserver.close()
