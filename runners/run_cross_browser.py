import subprocess

for browser in ["chrome", "firefox"]:
    subprocess.run([
        "pytest",
        "tests",
        "-m", "smoke",
        "-v",
        f"--browser={browser}",
        f"--alluredir=allure-results-{browser}"
    ])
