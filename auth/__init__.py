import os
import json
import datetime

from bson.objectid import ObjectId
import flask
from flask import current_app
from flask import request
from flask import jsonify
from bson import json_util
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_bcrypt import Bcrypt
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

app = flask.Blueprint('account', __name__)
master = current_app

@master.jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'result': False, 'message': 'Missing Authorization Header' }), 401


def validate_user(data, schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return {'result': False, 'message': e}
    except SchemaError as e:
        return {'result': False, 'message': e}
    return {'result': True, 'data': data}

@app.route('/register', methods=['POST'])
def register():
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 6
            },
            "timezone": {
                "type": "string"
            }
        },
        "required": ["email", "password", "name", "timezone"],
        "additionalProperties": False
    }

    data = validate_user(request.get_json(), schema)
    if data['result']:
        data = data['data']
        data['password'] = master.flask_bcrypt.generate_password_hash(data['password'])
        userCollection = master.db.users
        dbResult = userCollection.insert_one(data)
        print('User added successfully to users collection: {0}'.format(dbResult.inserted_id))
        return json.dumps(dbResult, indent=4, default=json_util.default), 200
    else:
        return jsonify({'result': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/hello', methods=['POST'])
def auth_user():
    schema = {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 6
            }
        },
        "required": ["email", "password"],
        "additionalProperties": False
    }

    data = validate_user(request.get_json(), schema)
    if data['result']:
        data = data['data']
        user = master.db.users.find_one({'email': data['email']})
        if user and master.flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return json.dumps(user, indent=4, default=json_util.default), 200
        else:
            return jsonify({'result': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'result': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
            'access_token': create_access_token(identity=current_user),
            'refresh_token': create_refresh_token(identity=current_user)
    }
    return jsonify(ret), 200
