"""
This is the entry point of the application that will resolve
the import dependencies. When running the app, point here
"""

from app import app, db

from models import *
from routes import *

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)