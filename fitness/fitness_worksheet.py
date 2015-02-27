from helpers import slug, is_number, clean_name
from models import Athlete

# Google API
import gspread
import pygal

from oauth2client.file import Storage

from operator import itemgetter

class FitnessWorksheet:

	worksheet = None

	all_results = None

	categories = None

	config = None

	athletes = []

	db_athletes = None

	NAME = 0
	RESULT = 1

	FAILED_FLAG = "-1"

	def __init__(self, worksheet):
		self.worksheet = worksheet

		self.all_results = self.worksheet.get_all_records()

		if len(self.all_results) == 0:
			raise Exception("Error retrieving results from sheet: " + self.worksheet.title)

	def get_categories(self):

		if self.categories:
			return self.categories

		self.categories = [item for item in self.all_results[0].keys() if item != 'Name' and item != 'Timestamp']

		return self.categories

	def slug_to_category_name(self, the_slug):

		categories = self.get_categories()

		for cat in categories:
			if slug(cat) == the_slug:
				return cat

		return None

	# TODO: The reason the app is going slow! Too many db queries
	def get_athletes(self, sort=True):

		if len(self.athletes) is not 0:
			return self.athletes

		if self.db_athletes is None:
			self.db_athletes = Athlete().query.all()

		# Look in all results
		for item in self.all_results:

			# Loop through all the athletes and match up the results
			for athlete in self.db_athletes:

				# Need to make sure the athlete is found
				found = False

				# Check if name matches
				if clean_name(item['Name']) == athlete.name:

					# Add the athlete
					self.athletes.append(athlete)

					# Set the found flag
					found = True

					# Stop the loop
					break

			if not found:
				raise Exception("Could not match athlete " + item['Name'] + " from Google to local database")

		if sort:
			self.athletes.sort()

		return self.athletes

	def get_category_stats(self, category):
		# category_index = self.get_category_index_from_name(category)

		category_name = self.slug_to_category_name(category)

		stats = [item[category_name] for item in self.all_results]

		athletes = self.get_athletes(False)

		if len(athletes) == len(stats):
			result_tuples = zip(athletes, stats)

			results_as_floats = self.safe_convert(result_tuples, float)
			
			return self.get_sorted(results_as_floats)
		else:
			return stats

	def get_athlete_stats(self):
		return self.worksheet.get_all_records()

	def get_plot(self, line_chart, category_name):

		category_stats = self.get_category_stats(category_name)

		line_chart.title = category_name
		line_chart.x_labels = [i[0] for i in category_stats]
		line_chart.add('Result', [i[1] for i in category_stats])

		return line_chart.render()

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

	def get_title(self):
		return self.worksheet.title

	def get_id(self):
		return self.worksheet.id