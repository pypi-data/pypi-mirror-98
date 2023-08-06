'''
Created on 3 Nov 2020

@author: jacklok
'''
from cryptography.fernet import Fernet
from trexlib.conf import CRYPTO_SECRET_KEY
from six import string_types
import json

def encrypt(value):
    
    if value:
        f = Fernet(CRYPTO_SECRET_KEY)
        return f.encrypt(value.encode())
    
def encrypt_json(json_value):
    
    if json_value:
        f = Fernet(CRYPTO_SECRET_KEY)
        return f.encrypt(json.dumps(json_value).encode())    
    
def decrypt(value):
    if value:
        if isinstance(object, string_types):
            value = str.encode(value)
            
        f = Fernet(CRYPTO_SECRET_KEY)
        return f.decrypt(value).decode()
    
def decrypt_json(value):
    json_value_in_str = decrypt(value)
    if json_value_in_str:
        return json.loads(json_value_in_str)     
