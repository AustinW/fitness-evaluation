from helpers import slug

from operator import itemgetter

class CategoryMapper:

	category_maps = None

	def __init__(self):
		self.category_maps = {
			'rope-climb': CategoryMapper.minimum_ignore_negative_sort,
			'rope-climb-steps': CategoryMapper.maximum_sort,
			'rope-climb-no-legs-small-rope': CategoryMapper.minimum_ignore_negative_sort,
			'suicide-run': CategoryMapper.minimum_ignore_negative_sort,
			'sprint': CategoryMapper.minimum_sort,
			'20s-chin-ups': CategoryMapper.maximum_sort,
			'20s-leg-lifts': CategoryMapper.maximum_sort,
			'20s-v-ups': CategoryMapper.maximum_sort,
			'20s-box-jumps': CategoryMapper.maximum_sort,
			'20s-step-ups': CategoryMapper.maximum_sort,
			'1-min-handstand': CategoryMapper.maximum_sort,
			'1-min-30s-handstand': CategoryMapper.maximum_sort,
			'2-min-handstand': CategoryMapper.maximum_sort,
			'10s-standing-back-tucks': CategoryMapper.maximum_sort,
			'10s-standing-back-pikes': CategoryMapper.maximum_sort,
			'standing-arabian': CategoryMapper.yes_no_sort,
			'bridge': CategoryMapper.maximum_sort,
			'left-splits': CategoryMapper.minimum_sort,
			'right-splits': CategoryMapper.minimum_sort,
			'middle-splits': CategoryMapper.minimum_sort,
			'pike-stretch': CategoryMapper.maximum_sort,
			'10-bounce': CategoryMapper.maximum_sort,
			'swing-time': CategoryMapper.maximum_sort,
			'3-4-back-cody-tuck': CategoryMapper.maximum_sort,
			'3-4-front-barani-ballout-tuck': CategoryMapper.maximum_sort,
			'2-straight-bounces': CategoryMapper.maximum_sort,
			'barani-tuck-back-tuck': CategoryMapper.maximum_sort,
			'barani-straight-back-straight': CategoryMapper.maximum_sort,
			'round-off-6x-backhandsprings': CategoryMapper.minimum_ignore_negative_sort,
			'round-off-6x-whips': CategoryMapper.minimum_ignore_negative_sort
		}
	
	@staticmethod
	def minimum_ignore_negative_sort(category_stats):
		
		# Sort by value
		category_stats.sort(key=itemgetter(1))

		regular_results = []
		failed_results = []
		
		# Put -1's at the back
		for i in range(len(category_stats)):
			if category_stats[i][1] == -1.0:
				failed_results.append(category_stats[i])
			else:
				regular_results.append(category_stats[i])
		
		return regular_results + failed_results

	@staticmethod
	def minimum_sort(category_stats):

		category_stats.sort(key=itemgetter(1))

		return category_stats

	@staticmethod
	def maximum_sort(category_stats):

		category_stats.sort(key=itemgetter(1), reverse=True)

		return category_stats

	@staticmethod
	def yes_no_sort(category_stats):

		# No sorting required

		return category_stats


	def sorter(self, category):

		return self.category_maps[slug(category)]
