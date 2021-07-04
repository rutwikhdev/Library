from flask import Blueprint, request
from flask_cors import CORS
import uuid
import json

from .models.members import Members

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
    DELETE a member from db
    return: status
    """
    data = json.loads(request.data)

    members = Members()
    members.remove_member(data['id'])
    members.close()

    return json.dumps({"text": "Successful"}), 201

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
