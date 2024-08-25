from flask import request, jsonify, send_from_directory, render_template, session
from backend.services.openai_service import (
    generate_scenario, interrogate_chat, generate_character_image, 
    generate_scenario_cover_image, generate_all_character_images, 
    generate_crime_scene_image
)
from backend.services.game_service import (
    get_all_scenarios, save_scenario, get_scenario, get_character
)
from backend.services.admin_service import migrate
from backend.services.tool_service import clean_chat
from enum import Enum

ChatType = Enum('ChatType', [
    'INTERROGATION', 
    'INVESTIGATION_CRIME_SCENE', 
    'INVESTIGATION_VICTIM', 
    'RESOLUTION'
])

def initialize_routes(app):
    @app.route('/')
    def serve_frontend():
        scenarios = get_all_scenarios()
        return render_template('index.html', scenarios=scenarios)
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory(app.static_folder, 'static/styles.css')
    
    @app.route('/scripts.js')
    def serve_js():
        return send_from_directory(app.static_folder, 'static/scripts.js')
    
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
    
    @app.route('/resolution')
    def serve_resolution():
        session["chat_type"] = ChatType.RESOLUTION.name
        return send_from_directory(app.static_folder, 'resolution.html')

    @app.route('/start_scenario/<int:id>')
    def start_scenario(id):
        session["scenario_id"] = id
        scenario = get_scenario(id)
        if scenario:
            characters = scenario.get("characters", [])
            return render_template('scenario.html', characters=characters, scenario=scenario)
        return jsonify({"message": "Scenario not found"}), 404

    @app.route('/interrogate/<int:id>', methods=['GET'])
    def serve_interrogate(id):
        session["chat_type"] = ChatType.INTERROGATION.name
        session["character_id"] = id
        scenario = get_scenario(session["scenario_id"])
        characters = scenario.get("characters", [])
        character = get_character(id)
        return render_template('interrogate.html', characters=characters, character=character, scenario=scenario)
    
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        message = data.get('message', '')
        chat_type = ChatType[session.get("chat_type", 'INTERROGATION')]
        
        scenario = get_scenario(session["scenario_id"])
        character = get_character(session.get("character_id", 0))
        chat = session.get(f"character_chat_{character['id']}", [])

        crime_scene = chat_type == ChatType.INVESTIGATION_CRIME_SCENE
        victim = chat_type == ChatType.INVESTIGATION_VICTIM
        resolution = chat_type == ChatType.RESOLUTION

        chat = interrogate_chat(message, chat, scenario, character, crime_scene, victim, resolution)

        session_key = {
            ChatType.INVESTIGATION_CRIME_SCENE: "crime_scene_chat",
            ChatType.RESOLUTION: "resolution_chat"
        }.get(chat_type, f"character_chat_{character['id']}")
        
        session[session_key] = chat
        answer = chat[-1]["content"] if chat else ""

        return jsonify({"answer": answer})

    @app.route('/investigate/crime_scene', methods=['GET'])
    def serve_investigate_crime_scene():
        session["chat_type"] = ChatType.INVESTIGATION_CRIME_SCENE.name
        scenario = get_scenario(session["scenario_id"])
        return render_template('interrogate.html', characters=scenario.get("characters", []), character=None, location="Tatort", scenario=scenario)
    
    @app.route('/investigate/victim/<int:id>', methods=['GET'])
    def serve_investigate_victim(id):
        session["chat_type"] = ChatType.INVESTIGATION_VICTIM.name
        scenario = get_scenario(session["scenario_id"])
        character = get_character(id)
        return render_template('interrogate.html', characters=scenario.get("characters", []), character=character, scenario=scenario)
    
    @app.route('/get_chat_history', methods=['GET'])
    def chat_history():
        chat_type = ChatType[session.get("chat_type", 'INTERROGATION')]
        session_key = {
            ChatType.INVESTIGATION_CRIME_SCENE: "crime_scene_chat",
            ChatType.RESOLUTION: "resolution_chat"
        }.get(chat_type, f"character_chat_{session.get('character_id', 0)}")

        chat = session.get(session_key, [])
        return jsonify({"chat": clean_chat(chat)})
    
    @app.route('/admin/migrate')
    def admin_migrate():
        migrate()
        return "Migration done"
    
    @app.route('/admin/character/image')
    def admin_character_image():
        scenario = get_scenario(session["scenario_id"])
        character = get_character(session["character_id"])
        generate_character_image(character, scenario)
        return "Character image generated"
    
    @app.route('/admin/character/images')
    def admin_character_images():
        scenario = get_scenario(session["scenario_id"])
        generate_all_character_images(scenario)
        return "Character images generated"
    
    @app.route('/admin/scenario/image')
    def admin_scenario_image():
        scenario = get_scenario(session["scenario_id"])
        generate_scenario_cover_image(scenario)
        return "Cover image generated"
    
    @app.route('/admin/crime/image')
    def admin_crime_scene_image():
        scenario = get_scenario(session["scenario_id"])
        generate_crime_scene_image(scenario)
        return "Crime scene image generated"
