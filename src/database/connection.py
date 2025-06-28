import sqlite3

def get_connection(db_url):
    return sqlite3.connect(db_url)
