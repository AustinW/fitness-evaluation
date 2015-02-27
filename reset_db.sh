rm -rf migrations app.db
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py seed_athletes
python manage.py seed_groups
python manage.py seed_athlete_groups