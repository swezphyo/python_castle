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
csvlist = list()
for file in glob.glob("*.csv"):
	csvlist.append(file)
# print(csvlist)
name = 'swezin.phyo@thitsaworks.com'    
passw = '499!ismylovE'

sender = name
#receiver = ['thynn.win@thitsaworks.com','waiphoo.ngon@thitsaworks.com','pye.aung@thitsaworks.com','aungmon.ko@thitsaworks.com','hnin.inzali@thitsaworks.com']
receiver = ['swezin.phyo@thitsaworks.com']
smtpsrv = "smtp.office365.com"

SUBJECT = 'MMCIX Daily Status ({0})'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
FILEPATH = os.path.dirname(os.path.abspath(__file__))
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = COMMASPACE.join(receiver)
msg['Subject'] = SUBJECT
body ="""    Daily Status job schedule are processed successfully.
""" 
body = MIMEText(body)
msg.attach(body)
part = MIMEBase('application', "octet-stream")
part.set_payload(open(FILEPATH, "rb").read())
encoders.encode_base64(part)
for f in csvlist:
    part.add_header('Content-Disposition', 'attachment', filename=f)  # or
    msg.attach(part)

smtpserver = smtplib.SMTP(smtpsrv,587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(sender, passw)
smtpserver.sendmail(sender, receiver, msg.as_string())
print('Successfully sent mail')
smtpserver.close()
