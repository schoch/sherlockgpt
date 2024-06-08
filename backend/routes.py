from flask import request, jsonify, send_from_directory
from .services.openai_service import generate_case

def initialize_routes(app):
    @app.route('/new_case', methods=['POST'])
    def new_case():
        data = request.get_json()
        keywords = data.get('keywords', '')
        case = generate_case(keywords)
        return jsonify({'case': case})
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')