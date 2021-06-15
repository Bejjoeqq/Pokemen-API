import hashlib
def encrypt(message):
	result = hashlib.md5(message.encode())
	return result.hexdigest()
	
if __name__ == '__main__':
	print(encrypt("dandeats"))