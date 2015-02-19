from flask import Flask
from flask import redirect, request

import gspread
import httplib2

from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.client import flow_from_clientsecrets

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds']
flow = flow_from_clientsecrets('./client_secrets.json',
                               scope='https://spreadsheets.google.com/feeds',
                               redirect_uri='http://localhost:5000/auth_return')

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/authorize')
def authorize():
	auth_uri = flow.step1_get_authorize_url()
	return redirect(auth_uri)

@app.route('/auth_return')
def auth_return():
	code = request.args['code']
	credentials = flow.step2_exchange(code)

	http = httplib2.Http()
	http = credentials.authorize(http)

if __name__ == '__main__':
	app.run(debug=True)