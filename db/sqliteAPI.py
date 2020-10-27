import sqlite3
import pandas as pd
import os


class SqliteAPI:
    def __init__(self, db):
        dbpath = os.path.join('./', db)
        self.conn = sqlite3.connect(dbpath)

    def execute(self, query):
        return pd.read_sql(query, con=self.conn)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    api = SqliteAPI('tempDataMining.db')
    df = api.execute('select * from engineNormal')
    api.close()
    print(df)
