# utils/common_utils.py

import json
import re


class CommonUtils:
    @staticmethod
    def open_file(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_extension(str):
        extension = str.split(".")[-1]
        return "." + extension

    @staticmethod
    def extract_value(str):
        return float(re.search(r"[\d.]+", str).group())
