import sqlite3
import pandas as pd


class SqliteAPI:
    def __init__(self):
        self.conn = sqlite3.connect('material.db')

    def execute(self, query):
        return pd.read_sql(query, con=self.conn)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    api = SqliteAPI()
    df = api.execute('select * from engine')
    print(df)
