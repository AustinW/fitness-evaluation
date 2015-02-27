from flask.ext.sqlalchemy import SQLAlchemy

from app import db

athlete_groups = db.Table('athlete_groups',
	db.Column('usag_id', db.Integer, db.ForeignKey('athletes.usag_id')),
	db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

class Athlete(db.Model):

	__tablename__ = 'athletes'

	usag_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	birthday = db.Column(db.DateTime, index=True)
	gender = db.Column(db.String(1))

	group = db.relationship("Group", secondary=athlete_groups)

	def __init__(self, name=None):
		self.name = name

	def __repr__(self):
		return '<Athlete %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def as_dict(self):
		return {
			'usag_id':  self.usag_id,
			'name':     self.name,
			'birthday': self.birthday.strftime('%m/%d/%Y'),
			'gender':   self.gender
		}

class Group(db.Model):

	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))

	athletes = db.relationship("Athlete", secondary=athlete_groups)

	def __repr__(self):
		return '<Group %r>' % (self.name)