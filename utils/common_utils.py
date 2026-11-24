
import json
import re
import csv
import openpyxl

from pathlib import Path


class CommonUtils:

    @staticmethod
    def open_file(path):
        """Read JSON data."""
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def open_csv_file(path):
        """Read CSV login data."""
        with open(path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            return [
                (user["username"], user["password"])
                for user in reader
            ]

    @staticmethod
    def open_xlsx_file(path):
        """Read Excel login data."""
        login_data = []

        workbook = openpyxl.load_workbook(
            path,
            read_only=True,
            data_only=True
        )

        try:
            sheet = workbook.active

            for row in sheet.iter_rows(
                min_row=2,
                values_only=True
            ):
                if not row:
                    continue

                username = str(row[0] or "")
                password = str(row[1] or "")

                login_data.append((username, password))

        finally:
            workbook.close()

        return login_data

    @staticmethod
    def open_filetype(path):
        """Identify file type and call the appropriate reader."""

        filetype = Path(path).suffix.lower()

        match filetype:

            case ".json":
                return CommonUtils.open_file(path)

            case ".csv":
                return CommonUtils.open_csv_file(path)

            case ".xlsx":
                return CommonUtils.open_xlsx_file(path)

            case _:
                raise ValueError(
                    f"Unsupported file type: {filetype}"
                )

    @staticmethod
    def get_extension(filename):
        return Path(filename).suffix.lower()

    @staticmethod
    def extract_value(text):
        match = re.search(r"\d+(?:\.\d+)?", text)

        if not match:
            raise ValueError(
                f"No numeric value found in: {text}"
            )

        return float(match.group())

    @staticmethod
    def format_product_id(text):
        return text.replace(" ", "-").lower()
