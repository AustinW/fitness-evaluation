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
else:
	print '###########################'
	print '# Environment: Production #'
	print '###########################'

ATHLETE_DB_PATH = os.path.join(BASE_DIR, 'roster.json')

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

GOOGLE_SHEETS_ID = '15j9rlGdfKBJ3WsaNrwa_9Oho7PJnOKsPjD24uOAFr6M'

CACHE_TIME = 3600