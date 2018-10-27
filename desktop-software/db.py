import sqlite3
import flask
from werkzeug.security import generate_password_hash, check_password_hash

def find_user(username, password):
    conn = sqlite3.connect('../website/app.db')
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row
    print("Opened database successfully")
    find_user = (''' SELECT id, username, password_hash FROM user WHERE username = ?''')
    cursor.execute(find_user, [(username)])
    results = cursor.fetchone()
    # print(find_user('ankit'))
    conn.commit()
    conn.close()
    return results

# print(find_user('ankit', 'ankit'))