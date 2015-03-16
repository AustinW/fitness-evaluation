"""
This is the entry point of the application that will resolve
the import dependencies. When running the app, point here
"""
import os
from routes import app

import argparse

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
		"debug": True if cmd_args.debug_mode else False,
		"use_debugger": True if cmd_args.debug_mode else False,
		"use_reloader": True if cmd_args.debug_mode else False,
	}

	app.run(**app_options)