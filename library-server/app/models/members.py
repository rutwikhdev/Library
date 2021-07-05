import sqlite3
from sqlite3 import Error

from .init_db import Connection
FILE = 'library.db'
TABLE = 'Members'

class Members(Connection):
    def __init__(self):
        Connection.__init__(self, FILE)
        self._create_table()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE}(
                    id INT UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    to_pay INT DEFAULT 0,
                    PRIMARY KEY(id)
                );"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_members(self):
        """
        return: list containing all members data
        """
        query = f"""SELECT * FROM {TABLE};"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res

    def add_member(self, some_id, name):
        """
        add a new member to database
        return: None
        """
        query = f"""INSERT INTO {TABLE}(id, name) values(
                    '{some_id}',
                    '{name}'
                );"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def remove_member(self, memberID):
        """
        removes a member: only if he has paid all debts
        return: None
        """
        query = f"""DELETE FROM {TABLE} WHERE id = '{memberID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_outstanding(self, memberID):
        """
        returns the current outstanding balance for memberID
        return: total debt of member
        """
        query = f"""SELECT to_pay FROM {TABLE} WHERE id = '{memberID}';"""
        self.cursor.execute(query)
        res = self.cursor.fetchone()

        return res

    def add_outstanding(self, memberID):
        """
        adds to outstanding balance indicating that member has rented a book.
        return: None
        """
        query = f"""UPDATE {TABLE} SET to_pay = to_pay + 50 WHERE id = '{memberID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)


    def deduct_outstanding(self, memberID, amount):
        """
        adds to outstanding balance indicating that member has returned a book.
        return: None
        """
        query = f"""UPDATE {TABLE} SET to_pay = to_pay - {amount} WHERE id = '{memberID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)
