import app

# Google API
import gspread
import pygal

from operator import itemgetter

from app.lib.fitness import FitnessWorksheet

class FitnessSheet:

	worksheets = []

	storage = None

	sheets_id = None

	def __init__(self, storage, sheets_id):
		self.storage = storage
		self.sheets_id = sheets_id


	def get_worksheets(self):

		if len(self.worksheets) == 0:

			if self.storage.get():

				# Initialize connection to google sheets
				gclient = gspread.authorize(self.storage.get())
				
				# Open the sheet
				sheet = gclient.open_by_key(self.sheets_id)

				# Get the first worksheet
				self.worksheets = sheet.worksheets()

		
		return self.worksheets

	def get_worksheet_by_id(self, worksheet_id):

		for worksheet in self.get_worksheets():
			if worksheet.id == worksheet_id:
				return FitnessWorksheet(worksheet)

		return None