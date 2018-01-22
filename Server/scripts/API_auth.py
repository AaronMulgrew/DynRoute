import jwt
import settings
import time
import json

def encode(username, password_hash):
    timestamp = time.time()
    encoded = jwt.encode({"timestamp":timestamp, "username":username, "password_hash":password_hash}, settings.SECRET_KEY, algorithm='HS256')
    return encoded

def decode(encoded_string):
    decoded_jwt = jwt.decode(encoded_string, settings.SECRET_KEY, algorithms=['HS256'])
    print(type(decoded_jwt))
    username = decoded_jwt['username']
    password_hash = decoded_jwt['password_hash']
    return decoded_jwt

#result = encode("aaron", "w23094823")
#print result
#decode_result = decode(result)