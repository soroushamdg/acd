"""
this file will decode options and database file and will return data
"""
import json
from cryptography.fernet import Fernet

def encrypt(data,filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key.encode('utf-8'))
    encrypted_data = f.encrypt(json.dumps(data).encode('utf-8'))
    with open(filename, "wb") as file:
        file.write(encrypted_data)

    file.close()

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key.encode('utf-8'))
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    file.close()
    # decrypt data
    return json.loads(f.decrypt(encrypted_data))
