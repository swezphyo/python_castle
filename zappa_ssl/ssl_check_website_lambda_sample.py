import ssl, socket
import sys
import base64
import smtplib
import boto3
import json
from botocore.exceptions import ClientError

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

from datetime import datetime

def check_ssl_expiry():
    """
    check url is ssl enabled or not
    - if ssl enabled: check certificate and expired date comes within 30 days or not
    - if no ssl enabled : list them 
    """
    expired_list = list()
    far_expired = list()
    no_ssl_domain = list()

    #dummy_hostname
    hostname = ['yomaland.com','starcityyangon.com','balloonsoverbaganbookings.com','scratchpads.eu/explore/sites-list','weevil.info']
    for host in hostname: 
        #print(host) #print domain name for debugging 

        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=host)
        try:
            #use 443 to validate only https 
            s.connect((host, 443))
            cert = s.getpeercert()
            #print(cert)

            #expired_cert to get ssl expired date - notAfter
            expired_cert = cert.get('notAfter')

            #ssl.cert_time_to_seconds for get cert_time(GMT) in epoch
            timestamp = ssl.cert_time_to_seconds(expired_cert)
            #convert epoch time to utc format to validate
            time_utc = datetime.utcfromtimestamp(timestamp)
            #print(time_utc)
            
            datetime_now = datetime.now()
            expire = time_utc - datetime_now #expire is timedelta object

            #use (timedelta.days) to get only days from timedelta object
            expire_days = expire.days

            if expire_days <= 30:
                expired_list.append({host:expire_days})
            else:
                far_expired.append({host:expire_days})
        except:
            no_ssl_domain.append(host)
    return expired_list, far_expired, no_ssl_domain

#add this function to add in AWS lambda
def lambda_handler(event, context):
    expired,far_expired,no_ssl = check_ssl_expiry()
    print("The domain that expired within 30 days are: {0}".format(expired))
    print("The domain that are long way to expire are: {0}".format(far_expired))
    print("The domain that are ssl-disabled are: {0}".format(no_ssl))
    
    #function send_mail to send the ssl information
    send_mail_ses(expired,far_expired,no_ssl)
    return {
        'statusCode': 200,
        'body': json.dumps('Program end!')
    }
