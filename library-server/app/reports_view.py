from flask import Blueprint
from flask_cors import CORS

from .models.rentals import Rentals
from .models.transactions import Transactions
from .models.books import Books
import json
import calendar

reports_view = Blueprint('reports', __name__)

@reports_view.route('/get_reports', methods=['GET'])
def get_reports():
    """
    returns a curated report json object.
    """
    rentals = Rentals()
    transacts = Transactions()
    books = Books()

    rental_data = rentals.get_rentals()
    transact_data = transacts.get_transactions()

    most_rented = {}
    most_paid = {}
    monthly_analysis = {}

    for r in rental_data:
        _, bookID, _, _ = r
        book = books.get_one_book(bookID)

        if bookID in most_rented:
            most_rented[bookID]['count'] += 1
        else:
            most_rented[bookID] = {
                'title': book[1],
                'authors': book[2],
                'count': 1
            }

    for r in transact_data:
        memberID, memberName, amount,  date, _, _ = r

        key = date[:7]
        year = '-' + date[:4]

        if key in monthly_analysis:
            monthly_analysis[key]['amount'] += amount
        else:
            month = calendar.month_name[int(date[5:7])] # pick month
            monthly_analysis[key] = {'month': month + year, 'amount': amount}

        if memberID in most_paid:
            most_paid[memberID]['amount'] += amount
        else:
            most_paid[memberID] = {
                'name': memberName,
                'amount': amount
            }

    rented = most_rented.values()
    paid = most_paid.values()
    rented = sorted(rented, key=lambda x: x['count'], reverse=True)
    paid = sorted(paid, key=lambda x: x['amount'], reverse=True)
    monthly = monthly_analysis.values()

    data = {'most_rented': rented, 'most_paid': paid, 'monthly': list(monthly)}

    return json.dumps(data), 200
