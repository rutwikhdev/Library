from flask import Blueprint, request
from flask_cors import CORS
import requests
import urllib
import json

from .models.books import Books

books_view = Blueprint('books_view', __name__)
CORS(books_view)

@books_view.route('/')
def home():
    return "<h1>Home Page</h1>"


@books_view.route('/search_api', methods=['POST'])
def search_api():
    """
    queries the api
    return: result from api
    """
    data = json.loads(request.data)

    enc = urllib.parse.urlencode({ data['type']: data['text']} )
    url = f"https://frappe.io/api/method/frappe-library?{enc}"
    res = requests.get(url)

    return json.dumps(json.loads(res.text)['message'])


@books_view.route('/search_local', methods=['POST'])
def search_local():
    """
    queries the local db
    return: result from local db as json
    """
    data = json.loads(request.data)

    books = Books()
    res = books.search_book(data)
    books.close()

    resArray = []

    if res:
        for i in range(len(res)):
            resArray.append({
                'bookID': res[i][0],
                'title': res[i][1],
                'authors': res[i][2],
                'average_rating': res[i][3],
                'language_code': res[i][5],
                'publisher': res[i][9],
                'quantity': res[i][10]
            })
        reponse = json.dumps(resArray), 200
    else:
        reponse = json.dumps(resArray), 404

    return reponse


@books_view.route('/add_library', methods=['POST'])
def add_library():
    """
    adds books to local db
    return: None
    """
    data = json.loads(request.data)

    books = Books()
    books.add_book(data)
    books.close()

    return json.dumps({"text":"Successful"}), 200
