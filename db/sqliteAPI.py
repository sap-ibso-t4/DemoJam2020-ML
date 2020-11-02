import sqlite3
import os
import pandas as pd


class SqliteAPI:
    """
    API for sqlite3
    """

    def __init__(self, database_file):
        """
        constructor
        :param database_file: db file path
        """
        dbpath = os.path.join('./', database_file)
        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor()

    def commit(self):
        """
        DB commit
        :return:
        """
        self.conn.commit()

    def rollback(self):
        """
        database_file rollback
        :return:
        """
        self.conn.rollback()

    def dml(self, query):
        """
        CUD
        :param query: string
        :return:
        """
        self.c.execute(query)

    def dql(self, query):
        """
        select
        :param query: string
        :return: list, line with tuple
        """
        return self.c.execute(query)

    def dql_with_df(self, query):
        """
        select and return data frame
        :param query: string
        :return: data frame
        """
        return pd.read_sql(query, con=self.conn)

    def close(self):
        """
        close database_file connection
        :return:
        """
        self.conn.close()


if __name__ == "__main__":
    from db.dict_to_itab import data_frame_to_internal_table

    db = SqliteAPI('material.db')
    df = db.dql_with_df('select * from material')
    internal_table = data_frame_to_internal_table(df)
    print(internal_table)
