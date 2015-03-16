from helpers import slug, clean_name
from category_ranking import CategoryRanking

from operator import itemgetter

class Ranking:

	RESULT = 1

	def __init__(self, athletes):
		self.athletes = athletes

	def overall_ranking(self, week_id):

		# Initialize empty array that will eventually contain sorted tuples of (name, score)
		overall_ranking = []

		# Loop through for each athlete
		for athlete in self.athletes.values():

			# Athlete's running total
			total_points = 0

			# Loop through each of the categories
			for category in athlete.categories[week_id]:

				# Get stats for the category
				category_stats = self.category_stats(week_id, category)

				# Get category rankings object
				category_ranking = CategoryRanking(category, category_stats)

				# Get athlete's points based on their result
				category_points = category_ranking.points(athlete)

				# Add the category points to their total points
				total_points += category_points

			# Assign the athlete's points to their Athlete object
			overall_ranking.append((athlete, total_points))

		# Sort the rankings
		overall_ranking.sort(key=itemgetter(1), reverse=True)

		return overall_ranking

	def category_stats(self, week_id, category):

		stats = []
		for name, athlete in self.athletes.iteritems():
			stats.append((name, athlete.categories[week_id][category]))

		return self.get_sorted(stats)

	@staticmethod
	def get_sorted(stats_list):

		# Sort by value
		stats_list.sort(key=itemgetter(1))

		regular_results = []
		failed_results = []

		# Put -1's at the back
		for i in range(len(stats_list)):
			if stats_list[i][Ranking.RESULT] == -1.0:
				failed_results.append(stats_list[i])
			else:
				regular_results.append(stats_list[i])

		return regular_results + failed_results

	def partial_ranking(self, athletes):

		overall_ranking = self.overall_ranking()

		partial_ranking = []

		for athlete in athletes:

			for rankedAthlete, score in overall_ranking:

				if clean_name(athlete.name) == clean_name(rankedAthlete.name):

					partial_ranking.append((rankedAthlete, score))
					

		return partial_ranking

	def get_stats_for_athlete(self, name, results):

		cleaned_name = clean_name(name)

		for result in results:
			if clean_name(result['Name']) == cleaned_name:
				return result

		return None