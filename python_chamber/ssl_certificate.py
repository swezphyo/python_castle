import ssl, socket

hostname = 'punhlaingestate.com'
ctx = ssl.create_default_context()
s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
s.connect((hostname, 443))
cert = s.getpeercert()
print(cert)