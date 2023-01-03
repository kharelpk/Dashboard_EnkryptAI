from Crypto.Cipher import AES
import secrets
from csv import reader, writer
import os

# Class to encrypt the data using AES
def encrypt_data(filename, key_length=16):
    # Generate a random symmetric encryption key
    key = secrets.token_hex(key_length)

    # create a cipher object using the random key
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)

    # Open the file to encrypt
    enc_data=[]
    with open(filename, 'r') as f:
        filereader = reader(f)
        # skip the header
        for i, row in enumerate(filereader):
            if i == 0:
                enc_data.append(row)
            # Encrypt the data
            else:
                enc_data.append([row[0]]+[cipher.encrypt(x.encode('utf-8')) for x in row[1:]])

    # Create the encrypted file
    enc_filename = os.path.splitext(filename)[0] + '.csv'
    #print(enc_filename)
    
    # Write contents to a file
    with open(enc_filename, 'w',newline='') as f:
        writefile = writer(f)
        writefile.writerows(enc_data)
    # Return the encryption key and nonce used
    return key, cipher.nonce