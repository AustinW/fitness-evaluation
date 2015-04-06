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

	def add_category(self, worksheet_id, cat_name, cat_score):
		self.categories[worksheet_id][cat_name] = cat_score

	def __repr__(self):
		return '<Athlete %r>' % (self.name)

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