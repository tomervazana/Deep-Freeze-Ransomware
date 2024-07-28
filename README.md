# Deep-Freeze-Ransomware
Offensive ransomware to encrypt the target personal files with AES-128 asymmetric key, leveraging RSA-2048 to encrypt the target key or to decrypt his key after bitcoin payment, resulting in unbreakable ransom.

# Implementation:
First of all I built a Client side only Ransomware, it uses the same public and private RSA keys for all its
clients, but as we learned about Asymmetric encryption: "calculating the private key (which decrypts) given
the public key (which encrypts) is hard". So its good enough, but i thought it will be more impressive to make
a server-client Based project for an ending course project. So then we transferred this project into Client-Server
based project.
just like the phishing web, we made a site on the local host, when a victim gets infected he request with "GET"
a new public key.
the Server has a users.db which contains user_name, publicIP, privateIP, private_RSA_key, public_RSA_key and the infection date.
(we extract this info from the victims machine and give it as an input to the server he creates new entry in the DB
for the victim and generate the RSA keys)
after that, the victim's machines chosen Directory tree gets encrypted (...\Desktop\ransomTesting) in this code, we change
he's desktop background to creepy clown that tells him to follow the notepad.
then we give introductions to the victim how to decrypt he's PC (server version):
--> send an email with the encrypted Fernet key to our email --> pay us 200$ in bitcoins and send us mail that contains
he's private ip, public ip and username (for better authentication) --> we (the attacker) check for the payment if he 
paid we send him back he's decrypted Fernet key which he supposed to put on his desktop (decrypted on the attackers machine) 
(we get the private key that fits our victim from users.db with a quarry)
--> a (while true) loop is running until it finds the correct key on desktop under the name DECRYPTED_SYM_KEY.txt 
(also SHA256 for key authentication in the fernet algorithm, so we wont accept a wrong key)
then we remove any memory of the malware (and change back the desk background image to the previous background image) 
from the victim's machine to stay nice and reliable hackers.

## client-only vs client-server:
client only malware is sent with a public RSA key and the client-server generates it from the server.
client only malware has only one public RSA key to all its clients and the client-server generates different key for each client.
client only doesn't use DB and the client-server based on queries and DB manipulation 
(SQL injection proof server db with (?,?,...,?)).
client doesn't need network connection to encrypt your system and the client-server must have internet to work properly 
(since I don't wanna encrypt he's machine if I don't have a proper key to decrypt later)

# Researching:
First of all I started from gathering the idea and researching what is the best 
symmetric and asymmetric encryption within python libraries.
cryptography library - 
After I done some research I found that RSA is the best asymmetric encryption and AES is the best
symmetric encryption, I also considered triple DES but passed since cryptodome doesn't recommend
this algorithm "legacy purposes only". So I decided to use RSA and AES.
pycryptodome library - 
Then when i tried to look for examples I found pycryptodome library which provides the Fernet Algorithm:
encryption method based on AES 128-bit
it does the following: 128-bit AES in CBC mode and PKCS7 padding, with HMAC using SHA256 for authentication.
Looks good and easy to use. So I decided to use RSA and Fernet.

## Main resources:
https://cryptography.io/en/latest/#                                         | RSA Library
https://pycryptodome.readthedocs.io/en/latest/src/introduction.html	    | Fernet Library
google search for research and examples.
