from helpers import slug, is_number, clean_name
from models import Athlete
from week import Week

# Google API
from gspread_mod import Client
from gspread.urls import construct_url
from gspread.httpsession import HTTPSession
from gspread.utils import finditem
from gspread.client import _url_key_re_v1, _url_key_re_v2
from gspread.ns import _ns
from gspread.models import Spreadsheet, Worksheet

from xml.etree import ElementTree

class Fitness:

	spreadsheet_id = None

	_weeks = None

	config = None

	_athletes = {}

	NAME = 0
	RESULT = 1

	FAILED_FLAG = "-1"

	def __init__(self, spreadsheet_id):
		self.spreadsheet_id = spreadsheet_id

		self.weeks()

	def weeks(self):

		"""
		Return list of Week objects which are wrappers for worksheets within
		the main spreadsheet
		
		:return: list List of Week objects
		"""
		if not self._weeks:

			self._weeks = {}

			# Get all worksheets
			all_worksheets = self.worksheets()

			for worksheet in all_worksheets:
				self._weeks[worksheet.id] = Week(worksheet)

		return self._weeks

	def worksheets(self):

		"""
		Biggest hack of my life...
		This allows me to grab a public feed. VERY prone to error

		:return: :raise Exception:
		"""
		client = Client(auth=None)

		spreadsheet = Fitness.spreadsheet_fake(client, self.spreadsheet_id)

		url = construct_url('worksheets', spreadsheet_id=self.spreadsheet_id, visibility='public', projection='full')
		session = HTTPSession()
		r = session.get(url)

		worksheet_tree = ElementTree.fromstring(r.read())

		worksheets = []

		for elem in worksheet_tree.findall(_ns('entry')):
			worksheets.append(Worksheet(spreadsheet, elem))

		return worksheets

	def week(self, id):
		"""

		:param id: worksheet id
		:rtype: Week
		"""
		if not self._weeks:
			self.weeks()

		return self._weeks[id] if id in self._weeks else None

	def athletes(self):

		"""


		:return:
		"""
		if self._athletes:
			return self._athletes

		# Get all athletes from the database as Athlete models
		db_athletes = Athlete().query.all()

		# Create an empty set to contain all athletes
		all_athletes_names = set()

		# Add athletes from every week without duplicates
		for week in self._weeks.values():

			for athlete in week.athlete_names():
				all_athletes_names.add(clean_name(athlete))

		# Using the list of names (participants), get their corresponding Athlete model
		for athlete in db_athletes:
			if athlete.name in all_athletes_names:
				self._athletes[athlete.name] = athlete

		return self._athletes

	def generate_all_stats(self):

		"""


		"""

		if not self._athletes:
			self.athletes()

		# Loop through every week
		for week_id, week in self._weeks.iteritems():

			# Loop through each week's athletes
			for name in week.athlete_names():
				try:
					self._athletes[name].categories[week_id] = week.stats_for_athlete(name)
				except Exception as e:
					raise Exception("Could not find " + name + " in the athlete database")

	def slug_to_category_name(self, the_slug):

		"""

		:param the_slug:
		:return:
		"""
		for week in self._weeks:

			categories = week.categories()

			for cat in categories:
				if slug(cat) == the_slug:
					return cat

		return None

	def get_title(self):
		return self.spreadsheet_id.title

	def get_id(self):
		return self.spreadsheet_id.id

	@staticmethod
	def spreadsheet_fake(client, spreadsheet_id):
		with open ("spreadsheet.xml", "r") as spreadsheet_makeshift:
			feed = ElementTree.fromstring(spreadsheet_makeshift.read())

			for elem in feed.findall(_ns('entry')):
				alter_link = finditem(lambda x: x.get('rel') == 'alternate',
									  elem.findall(_ns('link')))
				m = _url_key_re_v1.search(alter_link.get('href'))
				if m and m.group(1) == spreadsheet_id:
					return Spreadsheet(client, elem)

				m = _url_key_re_v2.search(alter_link.get('href'))

				if m and m.group(1) == spreadsheet_id:
					return Spreadsheet(client, elem)

			else:
				raise Exception("Could not open spreadsheet")

	@staticmethod
	def safe_convert(data, func):

		all_numbers = True

		for name, result in data:
			if not is_number(result):
				all_numbers = False
				break

		if all_numbers:
			for i in range(len(data)):
				data[i] = (data[i][Fitness.NAME], func(data[i][Fitness.RESULT]))

		return data