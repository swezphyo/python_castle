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

def send_mail_ses(expired,far_expired,no_ssl):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "swezinphyo@yoma.com.mm"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "swezinphyo@yoma.com.mm"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"

    # The subject line for the email.
    SUBJECT = "Domain SSL checker"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Check Domain's SSL \r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    expire_test = "The domain that expired within 30 days are:".format(expired)
    nonexpire_test = "The domain that still didn't expired are:".format(far_expired)
    nossl_test = "The domain that doesn't have ssl are: ".format(no_ssl)

    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Check Domain's SSL</h1>
      <p>{0}</p>
      <p>{1}</p>
      <p>{2}</p>
    </body>
    </html>
                """.format(expire_test,nonexpire_test,nossl_test)           

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# def send_mail(expired,far_expired,no_ssl):
#     """send mail about ssl expired dates and no-ssl website
#     """
#     #sender's mail credentials    
#     sender = 'swezinphyo@yoma.com.mm'
#     #decode the encoded password for security
#     passw = str(base64.b64decode('NDk5IWlzbXlsb3ZF'),"utf-8")
#     receiver = ['swezinphyo@yoma.com.mm']
#     smtpsrv = "smtp.office365.com"

#     SUBJECT = 'SSL checker notification'
#     msg = MIMEMultipart()
#     msg['From'] = sender
#     msg['To'] = COMMASPACE.join(receiver)
#     msg['Subject'] = SUBJECT
#     body =""" 
#     The domain that expired within 30 days are: {0}
#     The domain that still not expired: {1}
#     The domain that doesn't have ssl: {2}

#     """.format(expired,far_expired,no_ssl)
#     body = MIMEText(body)
#     msg.attach(body)

#     #smtpserver connection
#     smtpserver = smtplib.SMTP(smtpsrv,587)
#     smtpserver.ehlo()
#     smtpserver.starttls()
#     smtpserver.ehlo
#     smtpserver.login(sender, passw)
#     smtpserver.sendmail(sender, receiver, msg.as_string())
#     print('Successfully sent mail')
#     smtpserver.close()

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

"""Use this comment section when to implement in aws lambda"""
# def lambda_handler(event, context):
#     expired,far_expired,no_ssl = check_ssl_expiry()
#     print("The domain that expired within 30 days are: {0}".format(expired))
#     print("The domain that are long way to expire are: {0}".format(far_expired))
#     print("The domain that are ssl-disabled are: {0}".format(no_ssl))
    
#     #function send_mail to send the ssl information
#     send_mail(expired,far_expired,no_ssl)
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Successfully sent mail!')
#     }

def main():
    expired,far_expired,no_ssl = check_ssl_expiry()
    print("The domain that expired within 30 days are: {0}".format(expired))
    print("The domain that are long way to expire are: {0}".format(far_expired))
    print("The domain that are ssl-disabled are: {0}".format(no_ssl))
    #function send_mail to send the ssl information
    send_mail_ses(expired,far_expired,no_ssl)


if __name__ == '__main__':
    main()
    sys.exit(0) 
