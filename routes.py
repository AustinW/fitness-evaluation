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

@app.route('/')
def index():
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'], app.config['ATHLETE_DB_PATH'])
		worksheets = mainSheet.weeks()

		return render_template('index.html',
			worksheets=worksheets.values(),
			athletes=mainSheet.athletes().values()
		)
	
	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/week/<worksheet_id>')
def show_week(worksheet_id):
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'], app.config['ATHLETE_DB_PATH'])

		week = mainSheet.week(worksheet_id)

		if not week:
			return render_template('404.html', message='Could not find the specified worksheet')

		return render_template('worksheet.html',
			weeks=mainSheet.weeks().values(),
			week=week,
			athletes=mainSheet.athletes().values(),
			categories=week.categories()
		)

	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/api/week/<worksheet_id>', defaults = {'show': 'json'})
@app.route('/api/week/<worksheet_id>/graph', defaults = {'show': 'graph'})
def week_stats(worksheet_id, show):
	try:
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'], app.config['ATHLETE_DB_PATH'])
		mainSheet.generate_all_stats()

		week = mainSheet.week(worksheet_id)
		week.set_fitness_ref(mainSheet)

		if not week:
			return Response(jsonify({'message': 'Could not find the specified worksheet'}), 404)

		if 'category' in request.args and request.args['category'] != 'Overall Ranking':
			category = request.args['category']
			mapper = CategoryMapper()
			sorter = mapper.sorter(category)
			category_stats = week.stats_for_category(category, sorter)
			stats = [{'athlete': category_stat[0].as_dict(), 'score': category_stat[1]} for category_stat in category_stats]

		else:
			ranking = Ranking(week.athletes())

			overall_ranking = ranking.overall_ranking(worksheet_id)

			stats = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in overall_ranking]

		if show == 'json':
			return Response(json.dumps(stats), mimetype='application/json')
		elif show == 'graph':
			graph = Graph()
			return graph.get_line_graph(request.args.get('category', 'Overall Ranking'), 'Overall Points', stats)

	except Exception as e:
		response = jsonify(message=e.message)
		response.status_code = 400
		return response

@app.route('/athlete/<usag_id>/')
def show_athlete(usag_id):
	try:
		# Get main Google Sheet
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'], app.config['ATHLETE_DB_PATH'])
		mainSheet.generate_all_stats()

		# Get specific athlete object
		athlete = mainSheet.athlete(usag_id)

		if not athlete:
			return render_template('404.html', message='Could not find the specified athlete')

		return render_template('athlete.html',
			athlete=athlete,
			athletes=mainSheet.athletes().values(),
			weeks=mainSheet.weeks().values()
		)

	except Exception as e:
		return render_template('error.html', message=e.message)

@app.route('/api/athlete/<usag_id>', defaults={'show': 'json'})
@app.route('/api/athlete/<usag_id>/graph', defaults={'show': 'graph'})
def athlete_stats(usag_id, show):
	try:
		# Get main Google Sheet
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'], app.config['ATHLETE_DB_PATH'])
		mainSheet.generate_all_stats()

		# Get specific athlete object
		athlete = mainSheet.athlete(usag_id)

		# Check if we're looking for a specific category or overall stats
		if 'category' in request.args and request.args['category'] != 'Overall':

			# Init list to contain dicts of format {"week": ..., "result": ...}
			weekly_category_stats = []

			# Loop through each of the athlete's categories
			for week_id, stats in athlete.categories.iteritems():
				
				# Search for the specified category
				for category, score in stats.iteritems():
					if category == request.args['category']:

						# Map the result to the athlete's [category] score for each week
						weekly_category_stats.append({"week": mainSheet.week(week_id).title(), "result": score})

			# Sort the stats so later stats are to the right (convert week to a datetime object for sorting)
			weekly_category_stats.sort(key=lambda entry: time.strptime(entry['week'], '%m/%d/%Y'))

			# Show as json or a graph
			if show == 'json':
				return Response(json.dumps(weekly_category_stats), mimetype='application/json')
			elif show == 'graph':
				graph = Graph()
				return graph.get_line_graph_of_weeks(request.args['category'], 'Overall Points', weekly_category_stats)

		else:
			# Display overall ranking for the athlete over time
			ranking_data = [{"week": week.title(), "result": place} for week, place in athlete.rankings(mainSheet)]

			# Show as json or a graph
			if show == 'json':
				return Response(json.dumps(ranking_data), mimetype='application/json')
			elif show == 'graph':
				graph = Graph()
				return graph.get_line_graph_of_weeks('Overall Ranking Over Time', 'Ranking', ranking_data)

	except Exception as e:
		response = jsonify(message=e.message)
		response.status_code = 400
		return response

@app.route('/api/categories')
def categories():
	try:
		# Get main Google Sheet
		mainSheet = Fitness(app.config['GOOGLE_SHEETS_ID'])

		if 'week' in request.args:
			week = mainSheet.week(request.args['week'])

			if not week:
				raise Exception("The specified week could not be found.")

			categories = week.categories()
		else:
			categories = mainSheet.categories()

		return Response(json.dumps(categories), mimetype='application/json')

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

@app.errorhandler(500)
def internal_error(exception):
	app.logger.exception(exception)
	return render_template('error.html'), 500
@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.template_filter('slug')
def slug_filter(text, delim=u'-'):
	return slug(text, delim)