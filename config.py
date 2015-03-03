# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
if os.environ.get('DATABASE_URL') is None:
	print '######################'
	print '# Environment: Local #'
	print '######################'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
else:
	print '###########################'
	print '# Environment: Production #'
	print '###########################'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

GOOGLE_OAUTH_AUTHORIZED_CREDENTIALS = BASE_DIR + '/.credentials.json'

GOOGLE_SHEETS_ID = '19WBz6tcl5_6khFxGjlrmAngobsX4s5RVaw3oJmBmuJw'