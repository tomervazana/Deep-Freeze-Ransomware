from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

with open(f'{root_directory}\\Desktop\\Encrypted_Key.txt', 'rb') as readFile:
    enc_sym_key = readFile.read()

private_key = RSA.import_key(open('private.pem').read())  
private_cryptor = PKCS1_OAEP.new(private_key)
dec_fernet_key = private_crypter.decrypt(enc_fernet_key)
dec_fernet_key = private_cryptor.decrypt(enc_sym_key)
with open('DECRYPTED_SYM_KEY.txt', 'wb') as f:
    f.write(dec_fernet_key)