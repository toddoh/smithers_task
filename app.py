import functools
import json
import os
import flask
import config_secrets
import datetime
from flask import jsonify

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import db_pool

print('Smithers 0.2-05202019r1 -- Starting...')
app = flask.Flask(__name__)

with app.app_context():
    app.secret_key = config_secrets.FN_FLASK_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.flask_bcrypt = Bcrypt(app)
    app.jwt = JWTManager(app)
    app.db = db_pool.init_db()

    import auth.oauth_google
    import auth
    import users

    app.register_blueprint(auth.oauth_google.app, url_prefix='/api/v1/auth')
    app.register_blueprint(auth.app, url_prefix='/api/v1/auth')
    app.register_blueprint(users.app, url_prefix='/api/v1/users')


@app.route('/')
def index():
    return 'Smithers, release the hounds... API v1'


def checkValidToken(token):
    if token is None or token == '':
        return 'ERR_NEEDS_AUTH'

    tokenVerify = auth.oauth_google.checkTokenExpiration(token)
    if tokenVerify:
        return jsonify(tokenVerify)
    else:
        return 'ERR_INVALIDTOKEN'


@app.route('/api/v1/init')
def initApp():
    userTokenData = ''
    userTokenData = 'ya29.GlsMB2ceQ-aRuEOkfwL6Auk8NfSDuIpmxUNXWhto1K_7VvHimvLnsCd7SppNvnwC07HUt6bcc16-777zwkkw939p29pJZFj5v1owAikK9cyWZxdeznRGerAht1TY'
    return checkValidToken(userTokenData)




if __name__ == '__main__':
    #dev only
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

    app.run(debug=True)