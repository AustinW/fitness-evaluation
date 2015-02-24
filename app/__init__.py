# Flask
from flask import Flask, session, render_template
from flask import redirect, request
from flask.ext.sqlalchemy import SQLAlchemy

# Google API
from gspread import GSpreadException
from gspread.httpsession import HTTPError
from oauth2client.file import Storage

# Python standard library
import httplib2

from app.lib.fitness.fitness_sheet import FitnessSheet
from app.lib.fitness.ranking import Ranking
from app.lib.fitness import FitnessWorksheet
from app.lib import slug

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import *

storage = Storage(app.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])

@app.route('/')
def index():
	if not storage.get():
		session['redirect_url'] = request.url
		return redirect('/authorize')

	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])
		worksheets = mainSheet.get_worksheets()

		return render_template('index.html', worksheets=worksheets)
	
	except GSpreadException as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

	except HTTPError as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

@app.route('/worksheet/<worksheet_id>')
def show_worksheet(worksheet_id):
	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.get_worksheet_by_id(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		ranking = Ranking(fitnessWorksheet)

		print ranking.overall_ranking()

		return render_template('worksheet.html', worksheets=mainSheet.get_worksheets(), worksheet=fitnessWorksheet)
	except GSpreadException as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

	except HTTPError as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')


@app.route('/categories/<category>')
def show_category(category):
	try:

		worksheet = FitnessWorksheet(app.config)
		
		athlete_stats = worksheet.get_category_stats(category)

		category_name = worksheet.slug_to_category_name(category).title()

		print worksheet.get_plot(category)

		return render_template('category.html', worksheet=worksheet, athlete_stats=athlete_stats, category=category_name)
	except HTTPError as e:
		session['redirect_url'] = request.url
		return redirect('/authorize')

@app.route('/worksheet/<worksheet_id>/<category>')
def show_worksheet_category(worksheet_id, category):

	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.get_worksheet_by_id(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		return render_template('worksheet.html', worksheet=fitnessWorksheet)

	except GSpreadException as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

	except HTTPError as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')


@app.route('/authorize')
def authorize():
	auth_uri = app.config['FLOW'].step1_get_authorize_url()
	return redirect(auth_uri)

@app.route('/auth_return')
def auth_return():
	code = request.args['code']
	credentials = app.config['FLOW'].step2_exchange(code)

	# Apply necessary credential headers to all request made by an httplib2.Http instance
	http = httplib2.Http()
	http = credentials.authorize(http)

	storage = Storage(app.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])
	storage.put(credentials)

	if 'redirect_url' in session:
		redirect_url = session['redirect_url']
		session.pop('redirect_url')
		return redirect(redirect_url)
	else:
		return redirect('/')

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.template_filter('slug')
def slug_filter(text, delim=u'-'):
	return slug(text, delim)