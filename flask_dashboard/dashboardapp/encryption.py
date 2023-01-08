from Crypto.Cipher import AES
import secrets
from csv import reader, writer
import os
import pandas as pd
import numpy as np

# Class to encrypt the data using AES
def encrypt_data(filename, key_length=16):
    # Generate a random symmetric encryption key
    key = bytes.fromhex(secrets.token_hex(key_length))
    nonce = bytes.fromhex(secrets.token_hex(key_length))

    # create a cipher object using the random key
    cipher = AES.new(key, AES.MODE_GCM, nonce)

    # Open the file to encrypt
    enc_data=[]
    with open(filename, 'r') as f:
        filereader = reader(f)
        # skip the header
        for i, row in enumerate(filereader):
            print(row)
            if i == 0:
                enc_data.append(row)
            # Encrypt the data
            elif row==[]:
                print('empty row')
            else:
                enc_data.append([row[0]]+[cipher.encrypt(x.encode('utf-8')).hex() for x in row[1:]])

    # Create the encrypted file
    enc_filename = os.path.splitext(filename)[0] + '.csv'
    #print(enc_filename)
    
    # Write contents to a file
    with open(enc_filename, 'w',newline='') as f:
        writefile = writer(f)
        writefile.writerows(enc_data)
    # Return the encryption key and nonce used
    return key.hex(), nonce.hex()

def decrypt_data(filename, key, nonce):
    # create a cipher object using the random key
    cipher = AES.new(bytes.fromhex(key), AES.MODE_GCM, bytes.fromhex(nonce))

    # decrypt the data
    dec_data=[]
    with open(filename, 'r') as f:
        filereader = reader(f)
        # skip the header
        for i, row in enumerate(filereader):
            if i == 0:
                dec_data.append(row)
            # Encrypt the data
            else:
                dec_data.append([row[0]]+[cipher.decrypt(bytes.fromhex(x)).decode('ascii') for x in row[1:]])

    return dec_data