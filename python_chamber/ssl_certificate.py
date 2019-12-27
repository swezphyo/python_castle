import ssl, socket

hostname = ['yomaland.com','starcityyangon.com','yomalife.com']
for host in hostname: 
	ctx = ssl.create_default_context()
	s = ctx.wrap_socket(socket.socket(), server_hostname=host)
	s.connect((host, 443))
	cert = s.getpeercert()
	print(cert)