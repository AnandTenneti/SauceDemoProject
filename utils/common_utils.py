# utils/file_utils.py

import json


class CommonUtils:
    @staticmethod
    def open_file(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def get_extension(str):
        extension = str.split(".")[-1]
        return "." + extension
