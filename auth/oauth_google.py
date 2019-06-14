import functools
import os
import flask
import config_secrets
from flask import jsonify
import hashlib

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google.oauth2 import id_token
from google.auth.transport import requests
import json

app = flask.Blueprint('oauth_google', __name__)

def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials._refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes,
          'expiry': credentials.expiry
          }

def checkTokenExpiration(accessToken):
    with open('client_secret_380333357631-mubtpvnl87nlgva0uf6qgtk7o929u6k0.apps.googleusercontent.com.json', 'r') as JSON:
        gclientjson = json.load(JSON)['web']

    try:
        credentials = google.oauth2.credentials.Credentials(
                    accessToken,
                    refresh_token=None,
                    id_token=None,
                    client_id=gclientjson['client_id'],
                    client_secret=gclientjson['client_secret'],
                    token_uri=gclientjson['token_uri'])

        print('Checking the validity of credential: {0}'.format(credentials.valid))
        if credentials.expired:
            print('Requesting a new access Token from Google...')
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
    except BaseException as e:
        print('Error refreshing token with Google: {0}'.format(str(e)))
        return False
    else:
        return credentials_to_dict(credentials)

@app.route('/google')
@no_cache
def gAuth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret_380333357631-mubtpvnl87nlgva0uf6qgtk7o929u6k0.apps.googleusercontent.com.json', scopes=['email', 'profile', 'openid', 'https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/contacts.readonly'])

    flow.redirect_uri = flask.url_for('oauth_google.gAuthCallback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        state=hashlib.sha256(os.urandom(1024)).hexdigest(),
        include_granted_scopes='true')
    
    flask.session['gauth_state'] = state
    flask.session.permanent = True

    return flask.redirect(authorization_url)

@app.route('/google/callback')
@no_cache
def gAuthCallback():
    state = flask.session['gauth_state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret_380333357631-mubtpvnl87nlgva0uf6qgtk7o929u6k0.apps.googleusercontent.com.json',
        scopes=['email', 'profile', 'openid', 'https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/contacts.readonly'],
        state=state)
    flow.redirect_uri = flask.url_for('oauth_google.gAuthCallback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    #     Store user's access and refresh tokens in db
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    credentials_dict = credentials_to_dict(credentials)
    print(credentials.refresh_token)

    return jsonify(credentials_dict)


@app.route('/google/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared')