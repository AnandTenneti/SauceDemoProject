# utils/test_registry.py

import os


def get_markers():

    ini_path = os.path.join(os.path.dirname(__file__), "..", "pytest.ini")
    markers = []
    try:
        with open(os.path.normpath(ini_path)) as f:
            inside = False

            for line in f:

                if line.strip() == "markers =":
                    inside = True
                    continue

                if inside:
                    if "=" in line:
                        break

                    marker = line.strip().split(":")[0]

                    if marker:
                        markers.append(marker)

    except FileNotFoundError:
        print("⚠️  pytest.ini not found — no markers loaded")

    return markers
