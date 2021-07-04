from flask import Blueprint, request
from flask_cors import CORS
import json

from .models.members import Members
from .models.transactions import Transactions

transact_view = Blueprint('transact_view', __name__)
CORS(transact_view)

@transact_view.route('/get_transactions', methods=['GET'])
def get_transactions():
    """
    return: all transaction details.
    """
    transact = Transactions()
    res = transact.get_transactions()
    transact.close()

    transArr = [{
        'memberID': r[0],
        'memberName': r[1],
        'amount': r[2],
        'date': r[3],
        'time': r[4],
        'status': r[5]} for r in res]

    return json.dumps(transArr), 200

@transact_view.route('/make_transaction', methods=['POST'])
def make_transaction():
    """
    1. handle user payment checking for negative transactions.
    2. handle total outstanding.
    return: status
    """
    data = json.loads(request.data)

    transact = Transactions()
    member = Members()

    outstanding = member.get_outstanding(data['memberID'])

    if outstanding[0] - int(data['amount']) >= 0:
        transact.make_transaction(data['memberID'], data['amount'], data['memberName'])
        member.deduct_outstanding(data['memberID'], data['amount'])

        response = json.dumps({'text': 'Successful'}), 200
    else:
        response = json.dumps({'text': 'Unsuccessful'}), 400

    transact.close()
    member.close()

    return response
