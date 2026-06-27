import subprocess


class ReportAgent:

    @staticmethod
    def generate():
        result = subprocess.run(
            "allure generate allure-results --clean -o allure-report",
            shell=True
        )
        if result.returncode != 0:
            print("⚠️  Allure report generation failed")

    @staticmethod
    def open():
        subprocess.run(
            "allure open allure-report",
            shell=True
        )
