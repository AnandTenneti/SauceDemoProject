import subprocess


class ReportAgent:

    @staticmethod
    def generate():
        subprocess.run(
            "allure generate allure-results --clean -o allure-report",
            shell=True
        )

    @staticmethod
    def open():
        subprocess.run(
            "allure open allure-report",
            shell=True
        )
