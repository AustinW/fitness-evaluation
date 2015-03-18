"""
This is the entry point of the application that will resolve
the import dependencies. When running the app, point here
"""
import os
from routes import app

import argparse

import logging
from logging.handlers import RotatingFileHandler

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Development Server Help')
	parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
				  help="run in debug mode (for use with PyCharm)", default=False)
	parser.add_argument("-p", "--port", dest="port",
				  help="port of server (default:%(default)s)", type=int, default=5000)

	cmd_args = parser.parse_args()

	app_options = {
		"host": "0.0.0.0",
		"port": int(os.environ.get("PORT", cmd_args.port)),
		"debug": True, # if cmd_args.debug_mode else False
		"use_debugger": True if cmd_args.debug_mode else False,
		"use_reloader": True if cmd_args.debug_mode else False,
	}

	import logging
	logging.basicConfig(filename=app.config['BASE_DIR'] + 'error.log', level=logging.ERROR)

	# handler = RotatingFileHandler(app.config['BASE_DIR'] + 'error.log', maxBytes=1024 * 1024 * 50, backupCount=2)
	# handler.setLevel(logging.DEBUG)
	# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	# handler.setFormatter(formatter)
	# app.logger.addHandler(handler)

	app.run(**app_options)