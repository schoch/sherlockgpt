from flask import Flask, send_from_directory
from .routes import initialize_routes

app = Flask(__name__, static_folder='../frontend', static_url_path='/frontend')
initialize_routes(app)

if __name__ == '__main__':
    app.run(debug=True)