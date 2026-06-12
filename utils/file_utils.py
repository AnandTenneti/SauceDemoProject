# utils/file_utils.py

import json


def open_file(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
