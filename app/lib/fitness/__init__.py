import app

from app.lib.plot import Plot
from app.lib import slug
from app.lib import is_number

# Google API
import gspread
import pygal

from oauth2client.file import Storage

from operator import itemgetter

class FitnessWorksheet:

	worksheet = None

	categories = None

	config = None

	NAME = 0
	RESULT = 1

	FAILED_FLAG = "-1"

	def __init__(self, config):
		self.config = config

	def get_worksheet(self):

		if self.worksheet is not None:
			return self.worksheet

		storage = Storage(self.config['GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS'])

		if storage.get():

			# Initialize connection to google sheets
			gclient = gspread.authorize(storage.get())
			
			# Open the sheet
			sheet = gclient.open_by_key(self.config['GOOGLE_SHEETS_ID'])

			# Get the first worksheet
			self.worksheet = sheet.get_worksheet(0)

			return self.worksheet


	def get_categories(self):

		if self.categories:
			return self.categories

		columns = self.get_worksheet().row_values(1)
		
		# Delete the first two categories
		del columns[0]
		del columns[0]

		self.categories = columns

		return self.categories

	def slug_to_category_name(self, the_slug):

		categories = self.get_categories()

		for cat in categories:
			if slug(cat) == the_slug:
				return cat

		return None

	def get_athletes(self, sort=True):
		athletes = self.get_worksheet().col_values(2)
		del athletes[0]

		if sort:
			athletes.sort()

		return athletes

	def get_category_index_from_name(self, the_category):
		all_categories = self.get_categories()

		index = 3
		category_index = None

		for cat in all_categories:
			cat_slug = slug(cat)

			if the_category == cat_slug:
				category_index = index

			index += 1

		return category_index

	def get_category_stats(self, category):
		category_index = self.get_category_index_from_name(category)

		results = self.get_worksheet().col_values(category_index)
		del results[0]

		athletes = self.get_athletes(False)

		if len(athletes) == len(results):
			result_tuples = zip(athletes, results)

			results_as_floats = self.safe_convert(result_tuples, float)
			
			return self.get_sorted(results_as_floats)
		else:
			return results

	def get_plot(self, category_name):

		category_stats = self.get_category_stats(category_name)

		line_chart = pygal.Line()

		line_chart.title = category_name
		line_chart.x_labels = [i[0] for i in category_stats]
		line_chart.add('Result', [i[1] for i in category_stats])

		print line_chart.render()

	@staticmethod
	def get_sorted(stats_list):
		
		# Sort by value
		stats_list.sort(key=itemgetter(1))

		regular_results = []
		failed_results = []
		
		# Put -1's at the back
		for i in range(len(stats_list)):
			if stats_list[i][FitnessWorksheet.RESULT] == -1.0:
				failed_results.append(stats_list[i])
			else:
				regular_results.append(stats_list[i])
		
		return regular_results + failed_results

	@staticmethod
	def safe_convert(data, func):

		all_numbers = True

		for name, result in data:
			if not is_number(result):
				all_numbers = False
				break

		if all_numbers:
			for i in range(len(data)):
				data[i] = (data[i][FitnessWorksheet.NAME], func(data[i][FitnessWorksheet.RESULT]))

		return data