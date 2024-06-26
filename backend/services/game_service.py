import json
from backend.sherlockgpt.database import db
from backend.sherlockgpt.models import Scenario, Character

# Save a given scenario to db
def save_scenario(scenario_data):
    scenario = Scenario(
        name=scenario_data["name"],
        setting=scenario_data["setting"],
        crime=scenario_data["crime"],
        intro=scenario_data["intro"],
        secret_truth=json.dumps(scenario_data["secret_truth"]),
        guilty_persons=json.dumps(scenario_data["guilty_persons"]),
        location_info=scenario_data["location_info"],
        plot_twists=json.dumps(scenario_data["plot_twists"]),
        crime_scene_description=scenario_data["crime_scene_description"]
    )
    db.session.add(scenario)
    db.session.commit()

    for character in scenario_data['characters']:
        character_data = Character(
            scenario_id=scenario.id,
            name=character['name'],
            appearance=character['appearance'],
            personality=character['personality'],
            relationships=json.dumps(character['relationships']),
            involvement=character['involvement'],
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

# Load a scenario by its id
def get_scenario(id):
    scenario = Scenario.query.filter_by(id=id).first()
    if scenario:
        scenario_data = {
            'name': scenario.name,
            'setting': scenario.setting,
            'crime': scenario.crime,
            'intro': scenario.intro,
            'secret_truth': json.loads(scenario.secret_truth),
            'guilty_persons': json.loads(scenario.guilty_persons),
            'location_info': scenario.location_info,
            'plot_twists': json.loads(scenario.plot_twists),
            'crime_scene_description': scenario.crime_scene_description
        }
        characters = Character.query.filter_by(scenario_id=scenario.id).all()
        scenario_data['characters'] = [
            {
                'name': character.name,
                'appearance': character.appearance,
                'personality': character.personality,
                'relationships': json.loads(character.relationships),
                'involvement': character.involvement,
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

    
# Get a list with id:title pairs of all scenarios    
def get_all_scenarios():
    scenarios = Scenario.query.all()
    scenarios_list = []

    for scenario in scenarios:
        scenario_data = { 'id': scenario.id, 'name': scenario.name }
        scenarios_list.append(scenario_data)

    return scenarios_list