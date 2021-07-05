import sqlite3
from sqlite3 import Error

class Connection:
    def __init__(self, FILE):
        """
        try to connect to a file and read from a local sqlite3 database
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()

    def close(self):
        """
        close the db connection
        return: None
        """
        self.conn.close()

