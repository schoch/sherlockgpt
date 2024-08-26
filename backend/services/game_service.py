import json
from backend.sherlockgpt.database import db
from backend.sherlockgpt.models import Scenario, Character

# Save a given scenario to db
def save_scenario(scenario_data):
    scenario = Scenario(
        name=scenario_data["name"],
        style=scenario_data["style"],
        setting=scenario_data["setting"],
        crime=scenario_data["crime"],
        newspaper_headline=scenario_data["newspaper_headline"],
        newspaper_text=scenario_data["newspaper_text"],
        intro=scenario_data["intro"],
        secret_truth=json.dumps(scenario_data["secret_truth"]),
        victim=scenario_data["victim"],
        location_info=scenario_data["location_info"],
        plot_twists=json.dumps(scenario_data["plot_twists"]),
        crime_scene_description=scenario_data["crime_scene_description"]
    )
    db.session.add(scenario)
    db.session.flush()
    db.session.commit()

    # save the characters to db
    for character in scenario_data['characters']:
        character_data = Character(
            scenario_id=scenario.id,
            name=character['name'],
            appearance=character['appearance'],
            personality=character['personality'],
            relationships=json.dumps(character['relationships']),
            involvement=character['involvement'],
            is_dead=character['is_dead'],
            is_criminal=character['is_criminal'],
            is_victim=character['is_victim'],
            knowledge=character['knowledge'],
            feelings=character['feelings'],
            alibi=character['alibi'],
            activities=character['activities'],
            topics=character['topics'],
            motives=character['motives'],
            relevant_info=character['relevant_info']
        )
        db.session.add(character_data)

    db.session.commit()
    db.session.flush()
    return scenario.id

# Load a scenario by its id
def get_scenario(id):
    scenario = Scenario.query.filter_by(id=id).first()
    if scenario:
        scenario_data = {
            'id' : scenario.id,
            'name': scenario.name,
            'style': scenario.style,
            'setting': scenario.setting,
            'crime': scenario.crime,
            'newspaper_headline': scenario.newspaper_headline,
            'newspaper_text': scenario.newspaper_text,
            'intro': scenario.intro,
            'secret_truth': json.loads(scenario.secret_truth),
            'victim': scenario.victim,
            'location_info': scenario.location_info,
            'plot_twists': json.loads(scenario.plot_twists),
            'crime_scene_description': scenario.crime_scene_description
        }
        characters = Character.query.filter_by(scenario_id=scenario.id).all()
        scenario_data['characters'] = [
            {
                'id' : character.id,
                'name': character.name,
                'appearance': character.appearance,
                'personality': character.personality,
                'relationships': json.loads(character.relationships),
                'involvement': character.involvement,
                'is_dead': character.is_dead,
                'is_criminal': character.is_criminal,
                'is_victim': character.is_victim,
                'knowledge': character.knowledge,
                'feelings': character.feelings,
                'alibi': character.alibi,
                'activities': character.activities,
                'topics': character.topics,
                'motives': character.motives,
                'relevant_info': character.relevant_info
            } for character in characters
        ]
        return scenario_data
    
def get_character(id):
    character = Character.query.filter_by(id=id).first()
    if character:
        character_data = {
            'id' : character.id,
                'name': character.name,
                'appearance': character.appearance,
                'personality': character.personality,
                'relationships': json.loads(character.relationships),
                'involvement': character.involvement,
                'is_dead': character.is_dead,
                'knowledge': character.knowledge,
                'feelings': character.feelings,
                'alibi': character.alibi,
                'activities': character.activities,
                'topics': character.topics,
                'motives': character.motives,
                'relevant_info': character.relevant_info
        }
        return character_data

    
# Get a list with id:title pairs of all scenarios    
def get_all_scenarios():
    scenarios = Scenario.query.all()
    scenarios_list = []

    for scenario in scenarios:
        scenario_data = { 'id': scenario.id, 'name': scenario.name }
        scenarios_list.append(scenario_data)

    return scenarios_list