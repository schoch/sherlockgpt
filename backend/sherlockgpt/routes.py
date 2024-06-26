from flask import request, jsonify, send_from_directory, render_template, session
from backend.services.openai_service import generate_case
from backend.services.game_service import get_all_scenarios
from backend.services.tool_service import migrate
from flask_session import Session

# Example data for existing scenarios
scenarios = [
    {"id": 1, "name": "Scenario 1"},
    {"id": 2, "name": "Scenario 2"},
    {"id": 3, "name": "Scenario 3"}
]

def initialize_routes(app):
    @app.route('/new_case', methods=['POST'])
    def new_case():
        data = request.get_json()
        keywords = data.get('keywords', '')
        case = generate_case(keywords)
        global_scenario = case
        return jsonify({'case': case})
    
    @app.route('/new_scenario')
    def serve_new_scenario():
        return send_from_directory(app.static_folder, 'new_scenario.html')
    
    @app.route('/')
    def serve_frontend():
        get_all_scenarios()
        return render_template('index.html', scenarios=get_all_scenarios())
    
    @app.route('/start_scenario/<int:id>')
    def start_scenario(id):
        return f"Scenario {id} is starting..."
    
    @app.route('/interrogate')
    def serve_interrogate_chat():
        return send_from_directory(app.static_folder, 'interrogation.html')
    
    @app.route('/interrogate_chat', methods=['POST'])
    def serve_interrogate():
        data = request.get_json()
        message = data.get('message', '')
        #chat = interrogate_chat(message, global_chat, global_scenario)
        #return jsonify({'chat': chat})
        
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory(app.static_folder, 'static/styles.css')