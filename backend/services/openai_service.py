import openai
from openai import OpenAI
import os
import json
import urllib.request 

# Load the API-key from the .env file
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
gpt_model = "gpt-4o"

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
    model=gpt_model,
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
    model=gpt_model,
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
        model=gpt_model,
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
    model=gpt_model,
    )

    answer = response.choices[0].message.content
    chat.append({"role": "system", "content": answer})

    return chat    

def interrogate_chat(message, chat, scenario, character, crime_scene, victim, resolution):
    if crime_scene:
            prompt = load_prompt('investigate_crime_scene.txt', json.dumps(scenario))
    elif victim:
            prompt = load_prompt('investigate_victim.txt', json.dumps(scenario))
    elif resolution:
            prompt = load_prompt('resolution.txt', json.dumps(scenario))
    else:
        prompt = load_prompt('interrogate.txt', json.dumps(scenario))

    prompt = prompt.replace("{characterName}", character['name'])

    return game_chat(message, chat, prompt)

def simple_text_query(prompt):
    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
        model=gpt_model,
    )

    return response.choices[0].message.content

def image_query(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url

def generate_scenario_cover_image(scenario):
    prompt = load_prompt('scenario_image.txt', json.dumps(scenario))

    # 1st step: generate the required dalle-3 prompt
    image_prompt = simple_text_query(prompt)
    print(image_prompt)

    # 2nd step: generate image
    image_url = image_query(image_prompt)
    print(image_url)

    urllib.request.urlretrieve(image_url, "frontend/images/"+str(scenario['id'])+".png") 

def generate_character_image(character, scenario):
    prompt = load_prompt('character_image.txt', json.dumps(scenario))
    prompt = prompt.replace("{characterName}", character['name'])

    # 1st step: generate the required dalle-3 prompt
    image_prompt = simple_text_query(prompt)
    print(image_prompt)

    # 2nd step: generate image
    image_url = image_query(image_prompt)
    print(image_url)

    urllib.request.urlretrieve(image_url, "frontend/images/"+str(scenario['id'])+"-"+str(character['id'])+".png") 

def generate_crime_scene_image(scenario):
    prompt = load_prompt('crime_scene_image.txt', json.dumps(scenario))

    # 1st step: generate the required dalle-3 prompt
    image_prompt = simple_text_query(prompt)
    print(image_prompt)

    # 2nd step: generate image
    image_url = image_query(image_prompt)
    print(image_url)

    urllib.request.urlretrieve(image_url, "frontend/images/"+str(scenario['id'])+"-crime-scene.png") 

def generate_all_character_images(scenario):
    for character in scenario['characters']:
        print(character['name'])
        generate_character_image(character,scenario)