# Run a test server
from app import app
from app import lib

app.run(host='0.0.0.0', port=5000, debug=True)
