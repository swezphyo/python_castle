import ssl, socket
from datetime import datetime

hostname = ['yomaland.com','starcityyangon.com','balloonsoverbaganbookings.com']
for host in hostname: 
	print(host) #print domain name for debugging 

	ctx = ssl.create_default_context()
	s = ctx.wrap_socket(socket.socket(), server_hostname=host)
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
	else:
		print('Need long time to expire')