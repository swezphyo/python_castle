import ssl, socket
from datetime import datetime
import sys

def send_mail():
    """send mail about ssl expired dates and no-ssl website
    """
        #sender's mail credentials    
    sender = 'swezinphyo@yoma.com.mm'
    receiver = ['swezinphyo@yoma.com.mm']
    smtpsrv = "smtp.office365.com"

    SUBJECT = 'SSL checker notification'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receiver)
    msg['Subject'] = SUBJECT
    body ="""    Status
    """ 
    body = MIMEText(body)
    msg.attach(body)

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
    hostname = ['yomaland.com','starcityyangon.com','balloonsoverbaganbookings.com','scratchpads.eu/explore/sites-list']

    for host in hostname: 
        print(host) #print domain name for debugging 

        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=host)
        try:
            #use 443 to validate only https 
            s.connect((host, 443))
            cert = s.getpeercert()
            #print(cert)

            #date_range to get ssl expired date - notAfter
            date_range = cert.get('notAfter')

            #ssl.cert_time_to_seconds for get cert_time in epoch
            timestamp = ssl.cert_time_to_seconds(date_range)
            #convert epoch time to utc format to validate
            time_utc = datetime.utcfromtimestamp(timestamp)
            print(time_utc)
            datetime_now = datetime.now()
            expire = time_utc - datetime_now #expire is timedelta object

            #use (timedelta.days) to get only days from timedelta object
            expire_days = expire.days

            if expire_days <= 30:
                print ('Expired within {0} days'.format(expire_days))
                expired_list.append(host)
            else:
                print('Need long time to expire')
                far_expired.append(host)
        except socket.gaierror:
            print('No ssl for this domain')
            no_ssl_domain.append(host)

    print(expired_list)
    print(far_expired)
    print(no_ssl_domain)
def main():
    check_ssl_expiry()


if __name__ == '__main__':
    main()
    #sys.exit(0) 
