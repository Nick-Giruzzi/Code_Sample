#!/usr/bin/python3

import sys, sqlite3, datetime, time, json
from werkzeug.security import generate_password_hash, check_password_hash

def insert_users():
    users = {
        "1": {
            "fn":"Tyrion",
            "ln":"Lannister",
            "un":"the_hand",
            "pwd":"noDebts",
            "email":None,
            "created": datetime.datetime.now(),
            "mfa":False
        },
        "2": {
            "fn":"admin ",
            "ln":"admin",
            "un":"admin",
            "pwd":"admin",
            "email":"admin@skills.hub",
            "created": datetime.datetime.now(),
            "mfa":False
        }
    }
    # Connect to SQLite database
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    for k,v in users.items():
        try:
            cursor.execute("INSERT INTO User(first_name,last_name,username,password,email,created,mfa) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (v['fn'], v['ln'], v['un'], generate_password_hash(v['pwd']), v['email'],v['created'],v['mfa']))

        # Committing the changes and closing the connection
            conn.commit()
        except Exception as e:
            print(f"ERROR:\t{str(e)}")
        else:
            print("User inserted successfully.")
            #time.sleep(3)
    conn.close()


def insert_acc():
    accs = {
        "1": {
            "user_id":"1",
            "acc_type":"Checking",
            "number": "123456789",
            "balance": 1003.44
        },
        "2": {
            "user_id":"1",
            "acc_type":"Saving",
            "number": "987654321",
            "balance": 50002.05
        },
        "3": {
            "user_id":"1",
            "acc_type":"Credit",
            "number": "867530900",
            "balance": 488.12
        }
    }
    # Connect to SQLite database
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    for k,v in accs.items():
        try:
            cursor.execute("INSERT INTO Accounts(user_id,acc_type,number,balance) VALUES (?, ?, ?, ?)",
            (v['user_id'],v['acc_type'],v['number'],v['balance']))

        # Committing the changes and closing the connection
        
            conn.commit()
        except Exception as e:
            print(f"ERROR:\t{str(e)}")
        else:
            print("Acc inserted successfully.")
    conn.close()


def insert_transactions():
    transactions = {
        "1": {
            "acc_id": 1,
            "trans_type": "deposit",
            "amount": 250.00,
            "date":datetime.datetime.now()
        },
        "2": {
            "acc_id": 1,
            "trans_type": "withdrawl",
            "amount": 39.71,
            "date":datetime.datetime.now()
        },
        "3": {
            "acc_id": 1,
            "trans_type": "withdrawl",
            "amount": 72.40,
            "date":datetime.datetime.now()
        },
        "4": {
            "acc_id": 2,
            "trans_type": "deposit",
            "amount": 159.33,
            "date":datetime.datetime.now()
        },
        "5": {
            "acc_id": 2,
            "trans_type": "deposit",
            "amount": 222.10,
            "date":datetime.datetime.now()
        },
        "6": {
            "acc_id": 2,
            "trans_type": "deposit",
            "amount": 41.50,
            "date":datetime.datetime.now()
        },
        "7": {
            "acc_id": 3,
            "trans_type": "withdrawl",
            "amount": 49.22,
            "date":datetime.datetime.now()
        },
        "8": {
            "acc_id": 3,
            "trans_type": "withdrawl",
            "amount": 77.77,
            "date":datetime.datetime.now()
        },
        "9": {
            "acc_id": 3,
            "trans_type": "withdrawl",
            "amount": 19.99,
            "date":datetime.datetime.now()
        },
    }
    # Connect to SQLite database
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    for k,v in transactions.items():
        cursor.execute("INSERT INTO Transactions(acc_id,trans_type,amount,date) VALUES (?, ?, ?, ?)",
        (v['acc_id'], v['trans_type'], v['amount'], v['date']))

        # Committing the changes and closing the connection
        try:
            conn.commit()
        except Exception as e:
            print(f"ERROR:\t{str(e)}")
        else:
            print("transaction inserted successfully.")
            #time.sleep(3)
    conn.close()

if __name__ == "__main__":
    insert_users()
    insert_acc()
    insert_transactions()