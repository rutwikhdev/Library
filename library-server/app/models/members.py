import sqlite3
from sqlite3 import Error

FILE = 'library.db'
TABLE = 'Members'

class Members:
    def __init__(self):
        """
        try to connect to file and create cursor
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        close the db connection
        """
        self.conn.close()

    def _create_table(self):
        """
        create new database table if one doesn't exist
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
        returns all members data
        """
        query = f"""SELECT * FROM {TABLE};"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res

    def add_member(self, some_id, name):
        """
        add a new member to database
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
        """
        query = f"""SELECT to_pay FROM {TABLE} WHERE id = '{memberID}';"""
        self.cursor.execute(query)
        res = self.cursor.fetchone()

        return res

    def add_outstanding(self, memberID):
        """
        adds to outstanding balance indicating that member has rented a book.
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
        """
        query = f"""UPDATE {TABLE} SET to_pay = to_pay - {amount} WHERE id = '{memberID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)
