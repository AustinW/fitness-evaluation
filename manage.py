from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from app.models import *

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
	pass

@manager.command
def seed_athlete_groups():
	pass

if __name__ == '__main__':
	manager.run()

