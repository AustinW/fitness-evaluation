from operator import itemgetter

class Week:

	def __init__(self, worksheet):

		self._worksheet = worksheet
		self._records = self._worksheet.get_all_records()

		self._fitness_ref = None
		self._weeks = None
		self._categories = None
		self._athletes = None
		self._stats = None

	def categories(self):

		if self._categories:
			return self._categories

		if len(self._records):
			self._categories = [item for item in self._records[0].keys() if item != 'Name' and item != 'Timestamp']
		else:
			self._categories = []

		return self._categories

	def athlete_names(self):

		if self._athletes:
			return self._athletes

		self._athletes = [row['Name'] for row in self._records]

		return self._athletes

	def athletes(self):

		if not self._fitness_ref:
			raise Exception("Cannot get athletes because a reference to the Fitness object has not been made. Use Week::set_fitness_ref()")

		week_athletes = {}
		week_athlete_names = self.athlete_names()

		for athlete in self._fitness_ref.athletes().values():
			if athlete.name in week_athlete_names:
				week_athletes[athlete.name] = athlete

		return week_athletes

	def stats_for_category(self, category, sorter):

		athletes = [athlete for athlete in self.athletes().values() if athlete.categories.get(self.id()).get(category) != '']

		stats = map(lambda athlete: athlete.categories.get(self.id()).get(category), athletes)

		if len(athletes) == len(stats):
			result_tuples = zip(athletes, stats)

			preliminary_sort = self.get_sorted(result_tuples)
			real_sort = sorter(preliminary_sort)

			return real_sort
		else:
			raise Exception("Problem sorting athlete stats")

	def stats_for_athlete(self, athlete_name):

		if self._stats is None:
			self.generate_stats()

		return self._stats[athlete_name]

	def generate_stats(self):

		self._stats = {}

		# Go through every row in the worksheet
		for row in self._records:

			# Get the athlete name
			name = row['Name']

			# Create empty dictionary to store stats in
			athlete_stats = {}

			# Loop through each fitness category
			for category in self.categories():

				# Assign the category score to the athlete
				athlete_stats[category] = row[category]

			# Assign all of the athlete's stats to the main stats dictionary
			self._stats[name] = athlete_stats

	def set_fitness_ref(self, fitness):
		self._fitness_ref = fitness

	def id(self):
		return self._worksheet.id

	def title(self):
		return self._worksheet.title

	def as_dict(self):
		return {
			"id": self.id(),
			"title": self.title()
		}

	@staticmethod
	def get_sorted(stats_list):

		"""

		:param stats_list:
		:return:
		"""

		# Sort by value
		stats_list.sort(key=itemgetter(1))

		regular_results = []
		failed_results = []

		# Put -1's at the back
		for i in range(len(stats_list)):
			if stats_list[i][1] == -1.0:
				failed_results.append(stats_list[i])
			else:
				regular_results.append(stats_list[i])

		return regular_results + failed_results