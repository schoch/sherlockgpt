import openai
import os
import json
import urllib.request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
gpt_model = "gpt-4o"

def load_file(file_path, mode='r'):
    """ Utility function to load file content. """
    with open(file_path, mode) as file:
        return file.read() if mode == 'r' else json.load(file)

def load_prompt(template_name, keywords):
    return load_file(f'backend/prompts/{template_name}').replace('{template}', keywords)

def load_schema(schema_name):
    return load_file(f'backend/schemas/{schema_name}', 'r')

def call_openai_api(messages, schema, model=gpt_model, tool_choice="required"):
    """ Utility function to call OpenAI API. """
    response = openai.chat.completions.create(
        messages=messages,
        tools=[{"type": "function", "function": schema}],
        tool_choice=tool_choice,
        model=model,
    )
    return response.choices[0].message.tool_calls[0].function.arguments

def generate_scenario(keywords):
    # Generate part 1
    prompt = load_prompt('scenario.txt', keywords)
    schema = load_schema('scenario.json')
    arguments = call_openai_api([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ], schema)

    scenario = json.loads(arguments)

    # Generate part 2
    prompt_extra = load_prompt('scenario_extra.txt', arguments)
    schema_extra = load_schema('scenario_extra.json')
    arguments_extra = call_openai_api([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_extra}
    ], schema_extra)

    scenario_extra = json.loads(arguments_extra)
    scenario.update(scenario_extra)

    characters = generate_character_details(json.dumps(scenario))

    # Add character details to scenario
    for character in characters:
        for scenario_character in scenario['characters']:
            if character['name'] == scenario_character['name']:
                scenario_character.update(character)

    save_scenario(f"{scenario['name']}.json", scenario)
    return scenario

def generate_character_details(scenario):
    prompt_intro = load_prompt('character.txt', scenario)
    schema = load_schema('character.json')
    characters = []

    chat_messages = [{"role": "system", "content": "You are a helpful assistant."}]

    for scenario_character in json.loads(scenario)['characters']:
        chat_messages.append({"role": "user", "content": prompt_intro.replace("{character}", scenario_character["name"])})
        arguments = call_openai_api(chat_messages, schema)
        chat_messages.append({"role": "system", "content": arguments})
        characters.append(json.loads(arguments)["character"])

    return characters

def save_scenario(filename, scenario):
    with open(f'backend/scenarios/{filename}', 'w') as file:
        json.dump(scenario, file, indent=4)

def game_chat(message, chat, prompt):
    if not chat:
        chat.append({"role": "system", "content": prompt})

    chat.append({"role": "user", "content": message})
    response = openai.chat.completions.create(
        messages=chat,
        model=gpt_model,
    )

    answer = response.choices[0].message.content
    chat.append({"role": "system", "content": answer})
    return chat    

def interrogate_chat(message, chat, scenario, character, crime_scene=False, victim=False, resolution=False):
    prompt_name = 'investigate_crime_scene.txt' if crime_scene else \
                  'investigate_victim.txt' if victim else \
                  'resolution.txt' if resolution else \
                  'interrogate.txt'
    prompt = load_prompt(prompt_name, json.dumps(scenario)).replace("{characterName}", character['name'])
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

def save_image(url, path):
    urllib.request.urlretrieve(url, path)

def generate_scenario_cover_image(scenario):
    prompt = load_prompt('scenario_image.txt', json.dumps(scenario))
    image_prompt = simple_text_query(prompt)
    print(image_prompt)
    image_url = image_query(image_prompt)
    print(image_url)
    save_image(image_url, f"frontend/images/{scenario['id']}.png") 

def generate_character_image(character, scenario):
    prompt = load_prompt('character_image.txt', json.dumps(scenario)).replace("{characterName}", character['name'])
    image_prompt = simple_text_query(prompt)
    print(image_prompt)
    image_url = image_query(image_prompt)
    print(image_url)
    save_image(image_url, f"frontend/images/{scenario['id']}-{character['id']}.png") 

def generate_crime_scene_image(scenario):
    prompt = load_prompt('crime_scene_image.txt', json.dumps(scenario))
    image_prompt = simple_text_query(prompt)
    print(image_prompt)
    image_url = image_query(image_prompt)
    print(image_url)
    save_image(image_url, f"frontend/images/{scenario['id']}-crime-scene.png") 

def generate_all_character_images(scenario):
    for character in scenario['characters']:
        print(character['name'])
        generate_character_image(character, scenario)
