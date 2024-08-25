from flask import request, jsonify, send_from_directory, render_template, session
from backend.services.openai_service import generate_scenario, interrogate_chat, generate_character_image, generate_scenario_cover_image, generate_all_character_images, generate_crime_scene_image
from backend.services.game_service import get_all_scenarios,save_scenario,get_scenario,get_character
from backend.services.admin_service import migrate
from flask_session import Session
from backend.services.tool_service import clean_chat
from enum import Enum
    
ChatType = Enum('Chat_Type', ['INTERROGATION', 'INVESTIGATION_CRIME_SCENE', 'INVESTIGATION_VICTIM', 'RESOLUTION'])


def initialize_routes(app):
    @app.route('/')
    def serve_frontend():
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
    
    @app.route('/resolution')
    def serve_resolution():
        session["chat_type"] = ChatType.RESOLUTION
        return send_from_directory(app.static_folder, 'resolution.html')
   
   # ---- Start a new game ----------------------

    @app.route('/start_scenario/<int:id>')
    def start_scenario(id):
        session["scenario_id"] = id
        scenario = get_scenario(id)
        if scenario:
            characters = get_scenario(session["scenario_id"])["characters"]

            return render_template('scenario.html', characters=characters, scenario=scenario)
        return jsonify({"message": "Scenario not found"}), 404

    # ---- Start Chat sessions to interrogate  ----------------------
    @app.route('/interrogate/<int:id>', methods=['GET'])
    def serve_interrogate(id):
        session["chat_type"] = ChatType.INTERROGATION
        session["character_id"] = id
        scenario = get_scenario(session["scenario_id"])
        characters = get_scenario(session["scenario_id"])["characters"]
        character = get_character(id)
        return render_template('interrogate.html', characters=characters, character = character, scenario=scenario)
    
    #perform a chat, either a investiation or an interrogation
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        message = data.get('message', '')
        chat_type = ChatType(session["chat_type"])
        crime_scene = False
        victim = False
        resolution = False
        if chat_type == ChatType.INVESTIGATION_CRIME_SCENE:
            crime_scene = True
        elif chat_type == ChatType.INVESTIGATION_VICTIM:
            victim = True
        elif chat_type == ChatType.RESOLUTION:
            resolution = True
        
        scenario = get_scenario(session["scenario_id"])
        character = get_character(session["character_id"])
        chat = session.get("character_chat_"+str(session["character_id"]),[])

        chat = interrogate_chat(message, chat, scenario, character, crime_scene, victim, resolution)

        if chat_type == ChatType.INVESTIGATION_CRIME_SCENE:
            session["crime_scene_chat"] = chat
        elif chat_type == ChatType.RESOLUTION:
            session["resolution_chat"] = chat
        else:
            session["character_chat_"+str(session["character_id"])] = chat
        answer = chat[len(chat)-1]["content"]

        return jsonify({"answer" : answer})
    
    # ---- Start Chat sessions to investigate victims and locations  ----------------------
    
    @app.route('/investigate/crime_scene', methods=['GET'])
    def serve_investigate_crime_scene():
        session["chat_type"] = ChatType.INVESTIGATION_CRIME_SCENE
        characters = get_scenario(session["scenario_id"])["characters"]
        scenario = get_scenario(session["scenario_id"])
        return render_template('interrogate.html', characters=characters, character =None, location = "Tatort", scenario=scenario)
    
    @app.route('/investigate/victim/<int:id>', methods=['GET'])
    def serve_investigate_victim(id):
        session["chat_type"] = ChatType.INVESTIGATION_VICTIM
        characters = get_scenario(session["scenario_id"])["characters"]
        character = get_character(id)
        scenario = get_scenario(session["scenario_id"])
        return render_template('interrogate.html', characters=characters, character = character, scenario=scenario)
    
    # ---- Other stuff  ----------------------
    
    @app.route('/get_chat_history', methods=['GET'])
    def chat_history():
        chat_type = ChatType(session["chat_type"])

        if chat_type == ChatType.INVESTIGATION_CRIME_SCENE:
            chat = session.get("crime_scene_chat",[])
        elif chat_type == ChatType.RESOLUTION:
            chat = session.get("resolution_chat",[])
        else:
            chat = session.get("character_chat_"+str(session["character_id"]),[])

        return jsonify({"chat" : clean_chat(chat)})
        
    @app.route('/admin/migrate')
    def admin_migrate():
        migrate()
        return "migation done"
    
    @app.route('/admin/character/image')
    def admin_character_image():
        scenario = get_scenario(session["scenario_id"])
        character = get_character(session["character_id"])
        generate_character_image(character, scenario)
        return "character image generated"
    
    @app.route('/admin/character/images')
    def admin_character_images():
        scenario = get_scenario(session["scenario_id"])
        
        generate_all_character_images(scenario)
        return "character images generated"
    
    @app.route('/admin/scenario/image')
    def admin_scenario_image():
        scenario = get_scenario(session["scenario_id"])
        generate_scenario_cover_image(scenario)
        return "cover image generated"
    
    @app.route('/admin/crime/image')
    def admin_crime_scene_image():
        scenario = get_scenario(session["scenario_id"])
        generate_crime_scene_image(scenario)
        return "crime scene image generated"