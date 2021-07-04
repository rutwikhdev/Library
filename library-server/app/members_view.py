from flask import Blueprint, request
from flask_cors import CORS
import uuid
import json

from .models.members import Members
from .models.rentals import Rentals

members_view = Blueprint('members_view', __name__)
CORS(members_view)


@members_view.route('/add_member', methods=['POST'])
def add_member():
    """
    CREATE a member in db
    return: status
    """
    data = json.loads(request.data)
    random_id = uuid.uuid4().hex[:6]

    members = Members()
    result = members.add_member(random_id, data['name'])
    members.close()

    return json.dumps({"text": "Successful"}), 201

@members_view.route('/remove_member', methods=['POST'])
def remove_member():
    """
    DELETE a member from db if,
    1. No outstanding balance
    2. Returned all rented books
    return: status
    """
    data = json.loads(request.data)
    status = True

    members = Members()
    debt = members.get_outstanding(data['id'])

    if debt[0] == 0:
        rentals = Rentals()
        all_rents = rentals.get_rented(data['id'])

        for r in all_rents:
            if r[0] == 0:
                status = False
                break
    else:
        status = False

    if status:
        members.remove_member(data['id'])
        response = json.dumps({"text": "Successful"}), 201
    else:
        response = json.dumps({"text": "Unsuccessful"}), 404

    members.close()
    rentals.close()

    return response

@members_view.route('/get_members', methods=['GET'])
def get_members():
    """
    returns: list containing all the members in db
    """
    members = Members()
    result = members.get_members()
    members.close()

    data = []
    for r in result:
        id, name, to_pay = r
        rec = {'id': id, 'name': name, 'debt': to_pay}
        data.append(rec)

    return json.dumps(data), 200
