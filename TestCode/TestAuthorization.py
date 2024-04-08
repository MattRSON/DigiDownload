from flask import Flask, request
from requests_oauthlib import OAuth2Session

# Configuration for OAuth2
CLIENT_ID = '7hfBMjX22DohVDr70pzbYcUAJwwURwjL'
CLIENT_SECRET = 'AVziXUJJToyuCd1D"'
AUTHORIZATION_URL = 'https://sandbox-api.digikey.com/v1/oauth2/authorize?'
TOKEN_URL = 'https://sandbox-api.digikey.com/v1/oauth2/token'
REDIRECT_URI = 'http://localhost:5000/callback'

# Flask setup
app = Flask(__name__)

# OAuth2 session setup
oauth2_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)


@app.route('/')
def index():
    # Redirect to authorization URL
    authorization_url, state = oauth2_session.authorization_url(AUTHORIZATION_URL)
    return f'<a href="{authorization_url}">Click here to authorize</a>'


@app.route('/callback')
def callback():
    # Fetch the authorization code from the callback URL
    authorization_response = request.url
    oauth2_session.fetch_token(TOKEN_URL, authorization_response=authorization_response,
                                client_secret=CLIENT_SECRET)
    
    # Extract access token
    access_token = oauth2_session.token['access_token']
    return f'Access Token: {access_token}'


if __name__ == '__main__':
    app.run(debug=True)
