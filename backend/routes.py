from flask import request, jsonify, send_from_directory
from .services.openai_service import generate_case,interrogate_chat


global_chat = []
global_scenario = {}

def initialize_routes(app):
    @app.route('/new_case', methods=['POST'])
    def new_case():
        data = request.get_json()
        keywords = data.get('keywords', '')
        case = generate_case(keywords)
        global_scenario = case
        return jsonify({'case': case})
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/interrogate')
    def serve_interrogate_chat():
        return send_from_directory(app.static_folder, 'interrogation.html')
    
    @app.route('/interrogate_chat', methods=['POST'])
    def serve_interrogate():
        data = request.get_json()
        message = data.get('message', '')
        chat = interrogate_chat(message, global_chat, global_scenario)
        return jsonify({'chat': chat})
        
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory(app.static_folder, 'static/styles.css')