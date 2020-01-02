import ssl, socket
import sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

from datetime import datetime

def send_mail(expired,far_expired,no_ssl):
    """send mail about ssl expired dates and no-ssl website
    """
    #sender's mail credentials    
    sender = 'xxxx@hello.com.mm'
    passw = 'xxxxxx'
    receiver = ['xxxx@hello.com.mm']
    smtpsrv = "smtp.office365.com"

    SUBJECT = 'SSL checker notification'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receiver)
    msg['Subject'] = SUBJECT
    body =""" 
    The domain that expired within 30 days are: {0}
    The domain that still not expired: {1}
    The domain that doesn't have ssl: {2}

    """.format(expired,far_expired,no_ssl)
    body = MIMEText(body)
    msg.attach(body)

    #smtpserver connection
    smtpserver = smtplib.SMTP(smtpsrv,587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(sender, passw)
    smtpserver.sendmail(sender, receiver, msg.as_string())
    print('Successfully sent mail')
    smtpserver.close()

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

def main():
    expired,far_expired,no_ssl = check_ssl_expiry()
    print("The domain that expired within 30 days are: {0}".format(expired))
    print("The domain that are long way to expire are: {0}".format(far_expired))
    print("The domain that are ssl-disabled are: {0}".format(no_ssl))
    #function send_mail to send the ssl information
    send_mail(expired,far_expired,no_ssl)


if __name__ == '__main__':
    main()
    sys.exit(0) 
