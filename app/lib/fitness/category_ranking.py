import app

import time

from app.lib.fitness.category_mapper import CategoryMapper

class CategoryRanking:

	category = None

	category_stats = None

	def __init__(self, category, category_stats):
		self.category = category
		self.category_stats = category_stats

	def points(self, athlete_stat):
		
		# Get instance of our category mapper
		mapper = CategoryMapper()

		# Use category mapper to properly sort the stats
		sorter = mapper.sort_stats(self.category)

		if sorter.__name__ == 'yes_no_sort':
			
			for stat in self.category_stats:

				# Find the athlete and break
				if stat[0] == athlete_stat['Name']:

					return 1 if stat[1] == 'Yes' else 0

				return 0
		else:

			# Get the sorted results
			sorted_stats = sorter(self.category_stats)

			# Find where the athlete exists in the list
			index = 0

			for stat in sorted_stats:

				# Find the athlete and break
				if stat[0] == athlete_stat['Name']:
					break
				
				if stat[1] != -1.0:
					index += 1

			return len(sorted_stats) - index

