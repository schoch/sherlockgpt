import openai
import os
import json

# Lade den API-Schlüssel aus der .env Datei
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def load_prompt(template_name, keywords):
    with open(f'backend/prompts/{template_name}', 'r') as file:
        prompt = file.read()
    return prompt.replace('{template}', keywords)

def load_schema(schema_name):
    with open(f'backend/schemas/{schema_name}', 'r') as file:
        return json.load(file)

def generate_case(keywords):
    prompt = load_prompt('scenario.txt', keywords)
    schema = load_schema('case.json')

    response = openai.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
        ],
    tools=[
        {
            "type": "function",
            "function": schema,
        }
    ],
    tool_choice="required",
    model="gpt-4o",
    )

    scenario = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    game_scenario = scenario

    characters = generate_character_details(response.choices[0].message.tool_calls[0].function.arguments)


    # Füge die Charakterdetails zum Szenario hinzu
    for character in characters:
        for scenario_character in scenario['characters']:
            if character['name'] == scenario_character['name']:
                scenario_character.update(character)



    save_scenario(scenario["scenario_name"]+".json",scenario)
    return scenario

def generate_character_details(scenario):
    prompt_intro = load_prompt('character_intro.txt', scenario)
    schema = load_schema('character.json')
    characters = []

    chat_messages=[
        {"role": "system", "content": "You are a helpful assistant."}
        ]
    
    for scenario_character in json.loads(scenario)['characters']:
        chat_messages.append({"role": "user", "content": prompt_intro.replace("{character}", scenario_character["name"])})
        response = openai.chat.completions.create(
        messages=chat_messages,
        tools=[
            {
                "type": "function",
                "function": schema,
            }
        ],
        tool_choice="required",
        model="gpt-4o",
        ) 
        chat_messages.append({"role": "system", "content": response.choices[0].message.tool_calls[0].function.arguments})
        characters.append(json.loads(response.choices[0].message.tool_calls[0].function.arguments)["character"])


    return  characters


def save_scenario(filename, scenario):
    with open('backend/scenarios/'+filename, 'w') as file:
        json.dump(scenario, file, indent=4)

def interrogate_chat(message, chat, scenario):
    if(len(chat) == 0):
        prompt = load_prompt('interrogate.txt', json.dumps(scenario))
        prompt.replace("{characterName}", scenario['characters'][0]['name'])
        chat.append({"role": "system", "content": prompt})

    chat.append({"role": "user", "content": message})
    response = openai.chat.completions.create(
    messages=chat,
    model="gpt-4o",
    )

    scenario = json.loads(response.choices[0].message.tool_calls[0].function.arguments)