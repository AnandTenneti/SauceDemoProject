# utils/test_registry.py

import configparser


def get_markers():

    markers = []

    with open("pytest.ini") as f:
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

    return markers
