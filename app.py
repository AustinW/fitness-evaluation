from flask import Flask
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('ENVIRONMENT_CONFIG', silent=True)

app.cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'storage/cache'})