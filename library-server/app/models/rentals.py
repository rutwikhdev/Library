import sqlite3
from sqlite3 import Error

FILE = 'library.db'
TABLE = 'Rentals'

class Rentals:
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
                    memberID VARCHAR(20),
                    bookID VARCHAR(20),
                    returned BOOLEAN DEFAULT FALSE,
                    date_time datetime NOT NULL
                );"""
        self.cursor.execute(query)
        self.conn.commit()

    def rent_book(self, memberID, bookID):
        """
        adds a rent record
        """
        query = f"""INSERT INTO {TABLE}(memberID, bookID, date_time) VALUES('{memberID}', '{bookID}', date());"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def return_book(self, memberID, bookID):
        """
        update the return status
        """
        query = f"""UPDATE {TABLE} set returned = TRUE WHERE bookID = '{bookID}' AND memberID = '{memberID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_rentals(self):
        """
        returns all rental records.
        """
        query = f"""SELECT * FROM {TABLE};"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res

    def check_existing(self, memberID, bookID):
        """
        checks if a user has already rented the book with bookID
        """
        query = f"""SELECT returned from {TABLE} WHERE memberID = '{memberID}' AND bookID ='{bookID}';"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res