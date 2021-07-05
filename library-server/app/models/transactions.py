import sqlite3
from sqlite3 import Error

from .init_db import Connection

FILE = 'library.db'
TABLE = 'Transactions'

class Transactions(Connection):
    def __init__(self):
        Connection.__init__(self, FILE)
        self._create_table()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE}(
                    member_Id INT,
                    memberName VARCHAR(50),
                    amount INT,
                    date datetime NOT NULL,
                    time datetime NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'Completed'
                );"""

        self.cursor.execute(query)
        self.conn.commit()

    def make_transaction(self, memberId, amount, memberName):
        """
        complete a transaction.
        return: None
        """
        query = f"""INSERT INTO {TABLE}(member_Id, memberName, amount, date, time) VALUES('{memberId}', '{memberName}', '{amount}', date(), time());"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_transactions(self):
        """
        return: all transaction details.
        """
        query = f"""SELECT * from {TABLE};"""

        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res
