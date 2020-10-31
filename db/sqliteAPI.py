import sqlite3
import os


class SqliteAPI:
    def __init__(self, db):
        dbpath = os.path.join('./', db)
        self.conn = sqlite3.connect(dbpath)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def update(self, query):
        c = self.conn.cursor()
        print("Open database successfully")
        c.execute(query)

    def select(self, query):
        c = self.conn.cursor()
        print("Open database successfully")
        return c.execute(query)

    def close(self):
        self.conn.close()
