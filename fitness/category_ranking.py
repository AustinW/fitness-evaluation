from category_mapper import CategoryMapper
from helpers import clean_name

class CategoryRanking:

	category = None

	category_stats = None

	# Eventually map these out, but for now just ignore
	ignore_for_now = [
		'10 bounce',
		'Swing time',
		'3/4 back cody tuck',
		'3/4 front barani ballout tuck',

		'Barani tuck back tuck',
		'Barani straight back straight',

		'Round-off 6x whips',
		'Round-off 6x backhandsprings'
	]

	ATHLETE_OBJECT = 0
	SCORE = 1

	def __init__(self, category, category_stats):
		self.category = category
		self.category_stats = category_stats

	def points(self, athlete_stat):

		if self.category in self.ignore_for_now:
			return 0
		
		# Get instance of our category mapper
		mapper = CategoryMapper()

		# Use category mapper to properly sort the stats
		sorter = mapper.sort_stats(self.category)

		if sorter.__name__ == 'yes_no_sort':
			
			for stat in self.category_stats:

				# Find the athlete and break
				if stat[self.ATHLETE_OBJECT].name == clean_name(athlete_stat['Name']):

					return 1 if stat[1] == 'Yes' else 0

				return 0
		else:

			# Get the sorted results
			sorted_stats = sorter(self.category_stats)

			# Find where the athlete exists in the list
			index = 0

			for athleteObj, score in sorted_stats:

				# Find the athlete and break
				if athleteObj.name == clean_name(athlete_stat['Name']):
					break
				
				if score != -1.0:
					index += 1

			return len(sorted_stats) - index

