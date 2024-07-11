from flask import request, jsonify, send_from_directory, render_template, session
from backend.services.openai_service import generate_scenario, interrogate_chat
from backend.services.game_service import get_all_scenarios,save_scenario,get_scenario,get_character
from backend.services.admin_service import migrate
from flask_session import Session
from backend.services.tool_service import clean_chat

def initialize_routes(app):
    @app.route('/')
    def serve_frontend():
        #migrate()
        get_all_scenarios()
        return render_template('index.html', scenarios=get_all_scenarios())
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory(app.static_folder, 'static/styles.css')
    
    # ---- Generate new scenarios ----------------------

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
   
   # ---- Start a new game ----------------------

    @app.route('/start_scenario/<int:id>')
    def start_scenario(id):
        session["scenario_id"] = id
        scenario = get_scenario(id)
        if scenario:
            return render_template('scenario.html', scenario=scenario)
        return jsonify({"message": "Scenario not found"}), 404

    # ---- Start Chat sessions to interrogate & investigate ----------------------
    @app.route('/interrogate/<int:id>', methods=['GET'])
    def serve_interrogate(id):
        session["character_id"] = id
        characters = get_scenario(session["scenario_id"])["characters"]
        character = get_character(id)
        return render_template('interrogate.html', characters=characters, character = character)
    
    @app.route('/investigate/crime_scene', methods=['GET'])
    def serve_investigate_crime_scene():
        #session["character_id"] = id
        characters = get_scenario(session["scenario_id"])["characters"]
        #character = get_character(id)
        return render_template('interrogate.html', characters=characters, character = character)
    
    @app.route('/investigate/location', methods=['GET'])
    def serve_investigate_location():
        #session["character_id"] = id
        characters = get_scenario(session["scenario_id"])["characters"]
        #character = get_character(id)
        return render_template('interrogate.html', characters=characters, character = character)
    
    @app.route('/interrogate', methods=['POST'])
    def interrogate():
        data = request.get_json()
        message = data.get('message', '')
        scenario = get_scenario(session["scenario_id"])
        character = get_character(session["character_id"])
        chat = session.get("character_chat_"+str(session["character_id"]),[])

        chat = interrogate_chat(message, chat, scenario, character)
        session["character_chat_"+str(session["character_id"])] = chat
        answer = chat[len(chat)-1]["content"]

        return jsonify({"answer" : answer})
    
    @app.route('/get_chat_history', methods=['GET'])
    def chat_history():
        chat = session.get("character_chat_"+str(session["character_id"]),[])

        return jsonify({"chat" : clean_chat(chat)})
        
    @app.route('/admin/migrate')
    def admin_migrate():
        migrate()
        return "migation done"
    
