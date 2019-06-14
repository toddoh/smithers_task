import os
import json
import datetime

from bson.objectid import ObjectId
import flask
from flask import current_app
from flask import request
from flask import jsonify
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_bcrypt import Bcrypt
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

app = flask.Blueprint('users', __name__)
master = current_app

@master.jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'result': False, 'message': 'Missing Authorization Header' }), 401


@app.route('/', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    if request.method == 'GET':
        query = request.args
        data = master.db.users.find_one(query)
        del data['password']
        return dumps(data), 200
    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = master.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            master.db.users.update_one(data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
