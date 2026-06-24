import json
import os

config_path = os.path.join(
    os.path.dirname(__file__),
    "settings.json"
)

with open(config_path) as f:
    settings = json.load(f)
