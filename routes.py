# Flask
from flask import Flask, session, render_template, redirect, request, jsonify, Response

import json, time

import traceback

# Google API
from oauth2client.file import Storage

# Python standard library
import httplib2

from graph import Graph

from app import app

from fitness.fitness import Fitness
from fitness.week import Week
from fitness.ranking import Ranking
from fitness.category_mapper import CategoryMapper
from helpers import slug

from oauth2client.client import flow_from_clientsecrets

storage = Storage(app.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])

@app.route('/refactor')
def refactor():
	try:
		fitness = Fitness(app.config['GOOGLE_SHEETS_ID'])
		athletes = fitness.athletes()
		fitness.generate_all_stats()

		ranking = Ranking(athletes)
		print ranking.overall_ranking('oulqdya')

		return 'Done'

	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/')
def index():
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'])
		worksheets = mainSheet.weeks()

		return render_template('index.html', worksheets=worksheets.values())
	
	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/week/<worksheet_id>')
def show_week(worksheet_id):
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'])

		week = mainSheet.week(worksheet_id)

		if not week:
			return render_template('404.html', message='Could not find the specified worksheet')

		return render_template('worksheet.html',
			weeks=mainSheet.weeks().values(),
			week=week,
			categories=week.categories()
		)

	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/worksheet/<worksheet_id>/<category>')
def show_worksheet_category(worksheet_id, category):

	try:
		mainSheet = Week(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.week(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		return render_template('worksheet.html', worksheet=fitnessWorksheet)

	except Exception as e:
		return render_template('error.html', message=e.message)


@app.route('/week/<worksheet_id>.json', defaults = {'show': 'json'})
@app.route('/week/<worksheet_id>/graph', defaults = {'show': 'graph'})
def json_stats(worksheet_id, show):
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'])
		mainSheet.generate_all_stats()

		week = mainSheet.week(worksheet_id)
		week.set_fitness_ref(mainSheet)

		if not week:
			return Response(jsonify({'message': 'Could not find the specified worksheet'}), 404)

		if 'category' in request.args:
			category = request.args['category']
			mapper = CategoryMapper()
			sorter = mapper.sorter(category)
			category_stats = week.stats_for_category(category, sorter)
			stats = [{'athlete': category_stat[0].as_dict(), 'score': category_stat[1]} for category_stat in category_stats]

		else:
			ranking = Ranking(week.athletes())

			for name, athlete in week.athletes().iteritems():
				print name, athlete.categories

			overall_ranking = ranking.overall_ranking(worksheet_id)

			stats = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in overall_ranking]

		if show == 'json':
			return Response(json.dumps(stats), mimetype='application/json')
		elif show == 'graph':
			graph = Graph()
			return graph.get_line_graph('Overall Ranking', 'Overall Points', stats)

		# return jsonify(stats)

	except Exception as e:
		response = jsonify(message=e.message)
		response.status_code = 400
		return response

@app.route('/deauthorize')
def deauthorize():

	try:
		storage.delete()

		return redirect('/')

	except Exception as e:

		# Change error
		return render_template('404.html', message=e.message)


@app.route('/authorize')
def authorize():

	
	flow = flow_from_clientsecrets(app.config['BASE_DIR'] + '/client_secrets.json',
	                               scope='https://spreadsheets.google.com/feeds',
	                               redirect_uri=request.url_root + 'auth_return')

	auth_uri = flow.step1_get_authorize_url()
	return redirect(auth_uri)

@app.route('/auth_return')
def auth_return():

	flow = flow_from_clientsecrets(app.config['BASE_DIR'] + '/client_secrets.json',
	                               scope='https://spreadsheets.google.com/feeds',
	                               redirect_uri=request.url_root + 'auth_return')

	code = request.args['code']
	credentials = flow.step2_exchange(code)

	# Apply necessary credential headers to all request made by an httplib2.Http instance
	http = httplib2.Http()
	http = credentials.authorize(http)

	storage = Storage(app.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])
	storage.put(credentials)

	if 'redirect_url' in session and not session['redirect_url'].find('authorize'):
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