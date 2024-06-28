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

def generate_scenario(keywords):
    
    # generate part 1 ----------
    
    prompt = load_prompt('scenario.txt', keywords)
    schema = load_schema('scenario.json')

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

    # generate part 2 ----------
    
    prompt_extra = load_prompt('scenario_extra.txt', response.choices[0].message.tool_calls[0].function.arguments)
    schema_extra = load_schema('scenario_extra.json')

    response = openai.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_extra}
        ],
    tools=[
        {
            "type": "function",
            "function": schema_extra,
        }
    ],
    tool_choice="required",
    model="gpt-4o",
    )

    scenario_extra = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    scenario.update(scenario_extra)

    characters = generate_character_details(json.dumps(scenario))


    # Füge die Charakterdetails zum Szenario hinzu
    for character in characters:
        for scenario_character in scenario['characters']:
            if character['name'] == scenario_character['name']:
                scenario_character.update(character)



    save_scenario(scenario["name"]+".json",scenario)
    return scenario

def generate_character_details(scenario):
    prompt_intro = load_prompt('character.txt', scenario)
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

def game_chat(message, chat, prompt):
    if(len(chat) == 0):
        chat.append({"role": "system", "content": prompt})

    chat.append({"role": "user", "content": message})
    response = openai.chat.completions.create(
    messages=chat,
    model="gpt-4o",
    )

    answer = response.choices[0].message.content
    chat.append({"role": "system", "content": answer})

    return chat    

def interrogate_chat(message, chat, scenario, character):
    prompt = load_prompt('interrogate.txt', json.dumps(scenario))
    prompt = prompt.replace("{characterName}", character['name'])
    return game_chat(message, chat, prompt)

def investigate_victim_chat(message, chat, scenario, character):
    prompt = load_prompt('investigate_victim.txt', json.dumps(scenario))
    prompt = prompt.replace("{characterName}", character['name'])
    return game_chat(message, chat, prompt)

def investigate_location_chat(message, chat, scenario, location):
    prompt = load_prompt('investigate_location.txt', json.dumps(scenario))
    prompt = prompt.replace("{location}", location)
    return game_chat(message, chat, prompt)

 

