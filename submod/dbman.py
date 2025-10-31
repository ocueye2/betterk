import sqlite3

class dbman:
    def __init__(self):
        self.conn = sqlite3.connect("data/main.db")

    def __enter__(self):
        return self.conn, self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()