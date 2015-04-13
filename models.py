from fitness.ranking import Ranking

class Athlete:

	def __init__(self, first_name, last_name, gender, usag_id, dob, tra=None, dmt=None, tum=None, syn=None):
		self.name = first_name + ' ' + last_name
		self.gender = gender
		self.usag_id = usag_id
		self.dob = dob
		self.tra = tra
		self.dmt = dmt
		self.tum = tum
		self.syn = syn

		self.categories = {}
		self.ranking_points = {}
		self.week_rankings = []

	def add_category(self, worksheet_id, cat_name, cat_score):
		self.categories[worksheet_id][cat_name] = cat_score

	def rankings(self, mainSheet):
		for week_id, week in mainSheet.weeks().iteritems():
			week.set_fitness_ref(mainSheet)
			ranking = Ranking(week.athletes())

			overall_ranking = ranking.overall_ranking(week_id)

			i = 1
			for athlete, _ in overall_ranking:
				if athlete.usag_id == self.usag_id:
					self.week_rankings.append((week, i))

				i += 1

		return self.week_rankings

	def __repr__(self):
		return "<%s (%s: %s)" % (self.__class__.__name__, self.name, self.usag_id)

	def __unicode__(self):
		return self.name

	def as_dict(self):
		return {
			'usag_id':  self.usag_id,
			'name':     self.name,
			'birthday': self.dob,
			'gender':   self.gender,
			'categories': self.categories
		}