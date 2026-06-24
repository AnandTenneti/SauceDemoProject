# utils/common_utils.py

import json
import re


class CommonUtils:
    @staticmethod
    def open_file(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_extension(filename):
        extension = filename.split(".")[-1]
        return "." + extension

    @staticmethod
    def extract_value(str):
        return float(re.search(r"[\d.]+", str).group())

    @staticmethod
    def format_product_id(text):
        """
        Convert a product name into the format used by SauceDemo
        add-to-cart button IDs.

        Example:
            'Sauce Labs Backpack' -> 'sauce-labs-backpack'

        Args:
            text (str): Product name.

        Returns:
            str: Formatted product identifier.
        """
        return text.replace(" ", "-").lower()
