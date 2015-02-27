from helpers import slug, clean_name
from category_ranking import CategoryRanking

from operator import itemgetter

class Ranking:

	worksheet = None

	def __init__(self, worksheet):
		self.worksheet = worksheet

	def overall_ranking(self):

		# Initialize empty array that will eventually contain sorted tuples of (name, score)
		overall_ranking = []

		# Get all results
		results = self.worksheet.get_athlete_stats()

		# Get all athletes
		athletes = self.worksheet.get_athletes()

		# Get all categories
		categories = self.worksheet.get_categories()

		# Loop through for each athlete
		for athlete in athletes:

			# Athlete's stats
			stats = self.get_stats_for_athlete(athlete.name, results)

			# Athlete's running total
			total_points = 0

			# Loop through each of the categories
			for category in categories:

				# Get stats for the category
				category_stats = self.worksheet.get_category_stats(slug(category))

				# Get category rankings object
				category_ranking = CategoryRanking(category, category_stats)

				# Get athlete's points based on their result
				category_points = category_ranking.points(stats)

				# print athlete.name + " (" + category + "): " + str(category_points)

				# Add the category points to their total points
				total_points += category_points

			# Assign the athlete's points to their Athlete object
			overall_ranking.append((athlete, total_points))

		# Sort the rankings
		overall_ranking.sort(key=itemgetter(1), reverse=True)

		return overall_ranking

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