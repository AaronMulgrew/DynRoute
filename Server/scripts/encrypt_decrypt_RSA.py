from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def Encrypt(publicKey, message):
    #message = 'To be encrypted'
    key = RSA.importKey(open(publicKey).read())
    #key = RSA.importKey(open('public.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    print ciphertext
    return ciphertext

def Decrypt(privateKey, message):
    key = RSA.importKey(open(privateKey).read(), passphrase='123456')
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(ciphertext)
    print message
    return message

publicKey = 'scripts/public.pem'
message = 'To be Encrypted'
ciphertext = Encrypt(publicKey, message)
print Decrypt('scripts/private.pem', ciphertext)