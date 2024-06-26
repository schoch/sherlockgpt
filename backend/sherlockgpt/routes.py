from flask import request, jsonify, send_from_directory, render_template, session
from backend.services.openai_service import generate_scenario
from backend.services.game_service import get_all_scenarios,save_scenario,get_scenario
from backend.services.tool_service import migrate
from flask_session import Session

def initialize_routes(app):
    @app.route('/new_scenario', methods=['POST'])
    def new_scenario():
        data = request.get_json()
        keywords = data.get('keywords', '')
        scenario = generate_scenario(keywords)
        save_scenario(scenario)
        return jsonify({'scenario': scenario})
    
    @app.route('/new_scenario')
    def serve_new_scenario():
        return send_from_directory(app.static_folder, 'new_scenario.html')
    
    @app.route('/')
    def serve_frontend():
        #migrate()
        get_all_scenarios()
        return render_template('index.html', scenarios=get_all_scenarios())
    
    @app.route('/start_scenario/<int:id>')
    def start_scenario(id):
        scenario = get_scenario(id)
        if scenario:
            return render_template('scenario.html', scenario=scenario)
        return jsonify({"message": "Scenario not found"}), 404

    @app.route('/interrogate/<character_id>', methods=['GET'])
    def interrogate(character_id):
        # Hier können Sie die Logik für die Verhörseite hinzufügen
        return f"Interrogating character with ID {character_id}"
        
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory(app.static_folder, 'static/styles.css')