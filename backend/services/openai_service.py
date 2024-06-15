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
    characters = generate_character_details(response.choices[0].message.tool_calls[0].function.arguments)


    # Füge die Charakterdetails zum Szenario hinzu
    for character in characters['characters']:
        for scenario_character in scenario['characters']:
            if character['name'] == scenario_character['name']:
                scenario_character.update(character)


    # Ausgabe des gemergten Ergebnisses
    print(json.dumps(scenario, indent=2))


    return json.loads(scenario)

def generate_character_details(scenario):
    prompt = load_prompt('character.txt', scenario)
    schema = load_schema('character.json')

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
    return  json.loads(response.choices[0].message.tool_calls[0].function.arguments)