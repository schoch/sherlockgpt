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
    return prompt.replace('{keywords}', keywords)

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
    return  json.loads(response.choices[0].message.tool_calls[0].function.arguments)