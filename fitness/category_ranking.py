from category_mapper import CategoryMapper
from helpers import clean_name, slug

class CategoryRanking:

	category = None

	category_stats = None

	# Eventually map these out, but for now just ignore
	IGNORE_FOR_NOW = [
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

		# Get instance of our category mapper
		self.mapper = CategoryMapper()

	def points(self, athlete):
		if self.category in CategoryRanking.IGNORE_FOR_NOW:
			return 0
		
		# Use category mapper to properly sort the stats
		sorter = self.mapper.sorter(self.category)

		if sorter.__name__ == 'yes_no_sort':

			for stat in self.category_stats:

				# Find the athlete and break
				if stat[self.ATHLETE_OBJECT].name == athlete.name:

					return 1 if stat[self.SCORE] == 'Yes' else 0

				return 0
		else:

			# Get the sorted results
			sorted_stats = sorter(self.category_stats)

			# Find where the athlete exists in the list
			index = 0

			remaining_points = len(sorted_stats)

			# Keep track of last rank in case of tie
			previous_points = remaining_points

			athlete_points = None

			for athlete_name, score in sorted_stats:

				if score == -1.0:
					athlete_points = 0

				# Detect if there was a tie
				if score == sorted_stats[index - 1][self.SCORE]:
					athlete_points = previous_points
					remaining_points -= 1
				else:
					athlete_points = remaining_points
					remaining_points -= 1

				previous_points = athlete_points

				# Find the athlete and break
				if athlete_name == athlete.name:

					return athlete_points

				index += 1



