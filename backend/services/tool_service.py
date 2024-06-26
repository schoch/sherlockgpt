import json
from backend.sherlockgpt.database import db
from backend.services.game_service import save_scenario
from backend.sherlockgpt.models import Scenario, Character

import os
import glob

def migrate():
    directory_path = 'backend/scenarios/'
    for filename in glob.glob(os.path.join(directory_path, '*.json')):
        print(filename)
        with open(filename, 'r') as f:
            scenario = json.load(f)
            save_scenario(scenario)