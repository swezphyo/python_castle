#A script to encode password and decode back
import base64
import sys

def main():
	#declare the real password 
	passw = 'tecHnol0gy'

	#encode the password 
	encoded_pass = base64.b64encode(passw.encode("utf-8"))
	encodedStr = str(encoded_pass,"utf-8")

	print("Encoded data is {}".format(encodedStr))

	#decode the encoded output back to original password
	decoded_str = base64.b64decode(encodedStr)
	decoded_pass = str(decoded_str, "utf-8")
	print("Decoded data is {}".format(decoded_pass))


if __name__ == '__main__':
	main()
	sys.exit(0)