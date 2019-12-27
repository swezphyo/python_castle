import urllib.request
import sys

def _validate_ssl():
	from urllib.request import Request, urlopen, ssl, socket
	from urllib.error import URLError, HTTPError
	import json
	#some site without http/https in the path
	base_url = 'CHANGE_ME_TO_YOUR_SITE'
	port = '443'

	hostname = base_url
	context = ssl.create_default_context()

	with socket.create_connection((hostname, port)) as sock:
	    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
	        print(ssock.version())
	        data = json.dumps(ssock.getpeercert())
	        # print(ssock.getpeercert())

	print (data)


def check_ssl(url_list):
	"""to check whether the url has SSl or not
	- return True when there is ssl 
	"""
	non_ssl = list()
	ssl = list()
	for _url in url_list:
		conn = urllib.request.urlopen(_url)
		if(conn.getcode() == 200):
			#call validate function to check ssl's expired date
			print('hello')
		else:
			non_ssl.append(_url)
	#print(non_ssl)
	

def main():
	#_url = 'http://punhlaingestate.com'
	url_list = ['http://punhlaingestate.com','https://www.yomaland.com','https://www.digitbin.com/make-not-secure-site-secure-chrome-fix']
	check_ssl(url_list)
	

if __name__ == '__main__':
	main()
	sys.exit(0)