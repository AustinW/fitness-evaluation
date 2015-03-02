# Flask
from flask import Flask, session, render_template, redirect, request, jsonify, Response

import json, time

import traceback

# Google API
from gspread import GSpreadException
from gspread.httpsession import HTTPError
from oauth2client.file import Storage

# Python standard library
import httplib2

from graph import Graph

from app import app
from models import Athlete, Group

from fitness.fitness_sheet import FitnessSheet
from fitness.ranking import Ranking
from helpers import slug

from oauth2client.client import flow_from_clientsecrets

storage = Storage(app.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])

@app.route('/')
def index():
	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])
		worksheets = mainSheet.get_worksheets()

		return render_template('index.html', worksheets=worksheets)
	
	except (GSpreadException, HTTPError) as e:
		return render_template('index.html')

@app.route('/worksheet/<worksheet_id>')
def show_worksheet(worksheet_id):
	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.get_worksheet_by_id(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		return render_template('worksheet.html',
			worksheets=mainSheet.get_worksheets(),
			worksheet=fitnessWorksheet,
			categories=fitnessWorksheet.get_categories()
		)

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


@app.route('/worksheet/<worksheet_id>.json')
def json_stats(worksheet_id):
	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.get_worksheet_by_id(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		if 'category' in request.args:
			category = request.args['category']
			category_stats = fitnessWorksheet.get_category_stats(category)
			stats = [{'athlete': category_stat[0].as_dict(), 'score': category_stat[1]} for category_stat in category_stats]

		elif 'group' in request.args:
			try:
				group = Group().query.filter_by(id=int(request.args['group'])).first()

				athletes = group.athletes

				ranking = Ranking(fitnessWorksheet)

				start = time.clock()

				partial_ranking = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in ranking.partial_ranking(athletes)]

				end = time.clock()

				print 'Elapsed time: ' + str((end - start)) + ' seconds'

				return Response(json.dumps(partial_ranking), mimetype='application/json')

			except Exception as e:
				print traceback.format_exc()
				return jsonify({'message': 'Could not identify group', 'error': e.message})

		else:

			ranking = Ranking(fitnessWorksheet)

			overall_ranking = ranking.overall_ranking()

			stats = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in overall_ranking]

		return Response(json.dumps(stats), mimetype='application/json')

		# return jsonify(stats)

	except GSpreadException as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

	except HTTPError as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

@app.route('/worksheet/<worksheet_id>/graph')
def graph_stats(worksheet_id):
	try:
		mainSheet = FitnessSheet(storage, app.config['GOOGLE_SHEETS_ID'])

		fitnessWorksheet = mainSheet.get_worksheet_by_id(worksheet_id)

		if not fitnessWorksheet:
			return render_template('404.html', message='Could not find the specified worksheet')

		graph = Graph()

		if 'category' in request.args:
			category = request.args['category']
			category_name = fitnessWorksheet.slug_to_category_name(category)
			category_stats = fitnessWorksheet.get_category_stats(category)
			
			stats = [{'athlete': category_stat[0].as_dict(), 'score': category_stat[1]} for category_stat in category_stats]

			return graph.get_line_graph(category_name, category_name, stats)

		if 'group' in request.args:
			try:
				group = Group().query.filter_by(id=int(request.args['group'])).first()

				athletes = group.athletes

				ranking = Ranking(fitnessWorksheet)

				start = time.clock()

				partial_ranking = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in ranking.partial_ranking(athletes)]

				end = time.clock()

				print 'Elapsed time: ' + str((end - start)) + ' seconds'

				return Response(json.dumps(partial_ranking), mimetype='application/json')

			except Exception as e:
				print traceback.format_exc()
				return jsonify({'message': 'Could not identify group', 'error': e.message})

		else:

			ranking = Ranking(fitnessWorksheet)

			overall_ranking = ranking.overall_ranking()

			stats = [{'athlete': athlete.as_dict(), 'score': score} for athlete, score in overall_ranking]

			return graph.get_line_graph('Overall Ranking', 'Overall Points', stats)



		return Response(json.dumps(stats), mimetype='application/json')

		# return jsonify(stats)

	except GSpreadException as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

	except HTTPError as e:
		# Refresh token
		session['redirect_url'] = request.url
		return redirect('/authorize')

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