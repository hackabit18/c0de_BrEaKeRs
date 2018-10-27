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

def write_stats_blinks(username, blinks):
    conn = sqlite3.connect('../website/app.db')
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row
    print("Opened database successfully")
    fetch_blinks = (''' SELECT blinks from user WHERE username = ?''')
    cursor.execute(fetch_blinks, [(username)])
    
    blink = cursor.fetchone()
    print(blink[0])
    print(blinks)
    blink = blink[0] + blinks

    update_blink = (''' UPDATE user SET blinks = ? WHERE username = ?''')
    cursor.execute(update_blink, [(blink), (username)])
    fetch_user = (''' SELECT blinks from user WHERE username = ?''')
    cursor.execute(fetch_user, [(username)])
    results = cursor.fetchone()
    # print(find_user('ankit'))
    conn.commit()
    conn.close()
    return results

# print(write_stats_blinks('test1', 3))
    