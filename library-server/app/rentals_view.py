from flask import Blueprint, request
from flask_cors import CORS
import json

from .models.books import Books
from .models.members import Members
from .models.rentals import Rentals

rentals_view = Blueprint('rentals_view', __name__)
CORS(rentals_view)


@rentals_view.route('/rent_book', methods=['POST'])
def rent_book():
    """
    1. Check if the book is in quantity.
    2. Check current outstanding.(if > cur+50>500, cancel request)
    3. Check if the member has already rented the book with bookID and not returned
    4. Add to rental record, manage quantity of books.
    """
    data = json.loads(request.data)

    member = Members()
    rental = Rentals()
    books = Books()

    response = json.dumps({"text": "Unsuccessful"}), 400

    if books.is_in_stock(data['bookID']):
        # do this stuff only if the book is in stock.
        res = member.get_outstanding(data['memberID'])
        ex_list = rental.check_existing(data['memberID'], data['bookID'])
        existing = False

        for r in ex_list:
            # _, _, i, _ = r
            i = r

            if i == 0:
                existing = True
            else:
                existing = False

        if res and not existing:
            if res[0] + 50 < 500: # transaction is valid
                member.add_outstanding(data['memberID'])

                # reduce quantity
                books.rent_book(data['bookID'])

                # add a rental record
                rental.rent_book(data['memberID'], data['bookID'])

                response = json.dumps({"text": "Successful"}), 200

    books.close()
    member.close()
    rental.close()

    return response

@rentals_view.route('/get_rentals', methods=['GET'])
def get_rentals():
    """
    returns the rental data
    """
    rentals = Rentals()
    res = rentals.get_rentals()
    rentals.close()

    rentalArr = []
    for r in res:
        memID, bookID, rental_status, date = r
        rentalArr.append({
            'memberID': memID,
            'bookID': bookID,
            'rental_status': True if rental_status == 1 else False,
            'date': date
        })

    return json.dumps(rentalArr), 200

@rentals_view.route('/return_book', methods=['POST'])
def return_book():
    """
    accepts book return back to library.
    """
    data = json.loads(request.data)

    rental = Rentals()
    book = Books()

    rental.return_book(data['memberID'], data['bookID'])
    book.return_book(data['bookID'])

    rental.close()
    book.close()

    return json.dumps({'text': 'Successful'}), 200
