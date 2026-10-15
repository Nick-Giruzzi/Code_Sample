#!/usr/bin/python3

import sys, sqlite3, datetime, time, json
from werkzeug.security import generate_password_hash, check_password_hash

def steal_money():
    actions = {
        "update": {
            "1": {
                "user_id": 1,
                "acc_id": 1,
                "balance": 3.44,

            },
            "2": {
                "user_id":  1,
                "acc_id": 2,
                "balance":2.05,
            },
            "3": {
                "user_id":  1,
                "acc_id": 3,
                "balance":988.12,
            }
        },
        "trans": {
            "1": {
                "user_id": 1,
                "acc_id": 1,
                "trans_type": "transfer",
                "amount": 1000,

            },
            "2": {
                "user_id":  1,
                "acc_id": 2,
                "trans_type":"transfer",
                "amount":50000,
            },
            "3": {
                "user_id":  1,
                "acc_id": 3,
                "trans_type":"purchase",
                "amount":500,
            }
        }
    }
    
    # Connect to SQLite database
    conn = sqlite3.connect('/home/user/flask_app/server.db')
    cursor = conn.cursor()
    for k,v in actions['update'].items():
        cursor.execute(f"UPDATE Accounts SET balance={v['balance']} WHERE id={v['acc_id']}")

        try:
            conn.commit()
        except Exception as e:
            print(f"ERROR:\t{str(e)}")
        else:
            print("DB Updated.")
    
    for k,v in actions['trans'].items():
        cursor.execute("INSERT INTO Transactions(acc_id,trans_type,amount,date) VALUES (?, ?, ?, ?)",
        (v['acc_id'], v['trans_type'], v['amount'], datetime.datetime.now()))

        try:
            conn.commit()
        except Exception as e:
            print(f"ERROR:\t{str(e)}")
        else:
            print("DB Updated.")
      
    conn.close()

if __name__ == "__main__":
    steal_money()
