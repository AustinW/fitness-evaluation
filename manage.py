from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from models import *

import csv
from datetime import datetime

app.config.from_object('config')

ATHLETE_ROSTER = app.config['BASE_DIR'] + '/roster.csv'

FIRST_NAME = 0
LAST_NAME  = 1
GENDER     = 2
USAG_ID    = 3
BIRTHDAY   = 4
TRA_LVL    = 5
DMT_LVL    = 6
TUM_LVL    = 7
SYN_LVL    = 8

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def seed_athletes():
	"Add seed data to the database."
	
	with open(ATHLETE_ROSTER, 'rb') as roster:
		reader = csv.reader(roster)
		# Skip header
		next(reader, None)

		for row in reader:
			athlete = Athlete()

			athlete.usag_id = int(row[USAG_ID]) if row[USAG_ID] is not '' else None
			athlete.name = row[FIRST_NAME].strip() + ' ' + row[LAST_NAME].strip()
			athlete.gender = row[GENDER].strip()

			if row[BIRTHDAY] is not '':
				athlete.birthday = datetime.strptime(row[BIRTHDAY].strip(), '%d/%m/%Y')
			else:
				athlete.birthday = None

			db.session.add(athlete)
			print 'Adding %s' % athlete
			db.session.commit()

@manager.command
def seed_groups():
	"Add groups to the database"

	groups = [
		"Elite Trampoline",
		"Elite Double Mini & Tumbling",
		"Elite/Pre-Elite",
		"Optional Girls A",
		"Optional Girls B",
		"Compulsory A",
		"Compulsory B",
		"Compulsory C",
		"Compulsory D",
		"Optional Boys",
		"Boys Compulsory A",
		"Boys Compulsory B",
	]

	for group in groups:
		grp = Group()

		grp.name = group

		db.session.add(grp)
		print 'Adding %s' % grp
		db.session.commit()


@manager.command
def seed_athlete_groups():
	athlete_mappings = {
		'Logan Dooley': 1,
		'Neil Gulati': 1,
		'Charlotte Drury': 1,
		'Garret Chew': 1,
		'Maggie Gallagher': 1,
		'Tanner Robinson': 1,
		'Madelyne Barba': 1,

		'Austin White': 2,
		'Breanne Millard': 2,
		'Paige Howard': 2,
		'Kylee Roby': 2,
		'Carly Townsend': 2,
		'Kennedy Dierckman': 2,

		'Maya Yesharim': 3,
		'Lauren Broughton': 3,
		'Taylor Cook': 3,
		'Dana Nakano': 3,
		'Susan Gill': 3,
		'Anna Garmon': 3,
		'Emily Green': 3,
		'Danielle Ward': 3,
		'Nick Leavell': 3,

		'Molly Brascia': 4,
		'Ellie Clater': 4,
		'Allie Singer': 4,
		'Jocelyne McLaughlin': 4,
		'Makayla Vaughan': 4,

		'Sara Rose': 5,
		'Serena Meek': 5,
		'McKenna Andrew': 5,
		'Daisy Dick': 5,
		'Ellie Jameson': 5,
		'Bella Christman': 5,
		'Samantha Christman': 5,

		'Jenna ': 6,
		'Karen': 6,
		'Sophia': 6,
		'Kaitlyn': 6,
		'Sophie': 6,
		'Gianna': 6,
		'Sydney': 6,
		'Chavonne': 6,
		'Gracie': 6,

		'Lyndsey Caputo': 7,
		'Daylene': 7,
		'Sarah Reed': 7,
		'Natalie': 7,
		'Avery M': 7,

		'Julia M': 8,
		'Sophia S': 8,
		'Caroline ': 8,
		'Alyssa': 8,
		'Victoria': 8,
		'Dakota': 8,

		'Ashley': 9,
		'Kaela': 9,
		'Emily G': 9,
		'Emily S': 9,
		'Josie': 9,

		'Casey Block': 10,
		'Ryan Chew': 10,
		'Oliver Reed': 10,
		'Logan Broughton': 10,
		'Riley Wong': 10,
		'David Ilano': 10,

		'Marcus': 11,
		'Andrew Lamb': 11,
		'Johan Thrall': 11,
		'Garret': 11,
		'Luke': 11,

		'Ryder': 12,
		'Zander': 12,
		'Marco': 12,
		'Cooper': 12,
		'Jaden': 12,
		'Oliver': 12
	}

	# athletes = Athlete().query.all()

	# for athlete in athletes:

	# 	if athlete.name in athlete_mappings:

	# 		group = Group().query.filter_by(id=athlete_mappings[athlete.name]).first()

	# 		group.athlete_names.append(athlete)

	# 		print group.athlete_names

	# 		db.session.add(group)
	# 		db.session.commit()



if __name__ == '__main__':
	manager.run()

