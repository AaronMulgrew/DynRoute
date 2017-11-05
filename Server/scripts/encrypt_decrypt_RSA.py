from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

message = 'To be encrypted'
key = RSA.importKey(open('public.pem').read())
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(message)
print ciphertext
key = RSA.importKey(open('private.pem').read(), passphrase='123456')
cipher = PKCS1_OAEP.new(key)
message = cipher.decrypt(ciphertext)
print message
