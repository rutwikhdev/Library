import sqlite3
from sqlite3 import Error

from .init_db import Connection

FILE = 'library.db'
TABLE = 'Books'

class Books(Connection):
    def __init__(self):
        Connection.__init__(self, FILE)
        self._create_table()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE}(
                    bookID VARCHAR(50) UNIQUE NOT NULL,
                    title VARCHAR(250),
                    authors VARCHAR(100),
                    avg_rating FLOAT,
                    ratings_count INT,
                    lang_code VARCHAR(5),
                    num_pages INT,
                    text_reviews INT,
                    pub_date VARCHAR(15),
                    publisher VARCHAR(50),
                    quantity INT DEFAULT 10,
                    polularity INT DEFAULT 0,
                    PRIMARY KEY(bookID)
                );"""

        self.cursor.execute(query)
        self.conn.commit()

    def add_book(self, data):
        """
        1. adds a record to local db if not present. i.e. for the first time
        2. if the record already exists then increase quantity
        return: None
        """
        exists = self.check_if_exists(data['isbn'])

        if exists:
            query = f"""UPDATE {TABLE} SET quantity = quantity + 10 WHERE bookID = '{data["isbn"]}'"""
        else:
            query = f"""INSERT INTO {TABLE}(bookID, title, authors, avg_rating, ratings_count,
                lang_code, num_pages, text_reviews, pub_date, publisher) values(
                    "{data['isbn']}",
                    "{data['title']}",
                    "{data['authors']}",
                    {float(data['average_rating'])},
                    {int(data['ratings_count'])},
                    "{data['language_code']}",
                    {int(data['  num_pages'])},
                    {int(data['text_reviews_count'])},
                    "{data['publication_date']}",
                    "{data['publisher']}"
                );"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def search_book(self, data):
        """
        searches for a book in db by author name or title.
        return: list of books that match the search query
        """
        query = f"""SELECT * from {TABLE} where "{data['type']}" LIKE "%{data['text']}%";"""

        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res

    def check_if_exists(self, bookID):
        """
        check if book already exists in local db.
        return: Boolean
        """
        query = f"""SELECT * from {TABLE} WHERE bookID = '{bookID}';"""
        res = self.cursor.execute(query)

        if self.cursor.fetchall():
            return True
        else:
            return False

    # try using this function where check_if_exists is used
    def is_in_stock(self, bookID):
        """
        checks if the book is in stock(queries quantity)
        return: Boolean
        """
        query = f"""SELECT quantity from {TABLE} where bookID = '{bookID}';"""
        self.cursor.execute(query)

        q = self.cursor.fetchone()

        if q[0] > 0:
            return True
        else:
            return False

    def rent_book(self, bookID):
        """
        manages quantity of book
        return: None
        """
        query = f"""UPDATE {TABLE} set quantity = quantity - 1 where bookID = '{bookID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def return_book(self, bookID):
        """
        manages quantity of book: can be merged with above function
        return: None
        """
        query = f"""UPDATE {TABLE} set quantity = quantity + 1 where bookID = '{bookID}';"""

        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_one_book(self, bookID):
        """
        return: data for a single book.
        """
        query = f"""SELECT * FROM {TABLE} WHERE bookID = '{bookID}';"""

        self.cursor.execute(query)
        res = self.cursor.fetchone()

        return res
