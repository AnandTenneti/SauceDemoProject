from utils.test_registry import get_markers


class PlannerAgent:

    @staticmethod
    def create_plan(request):
        request = request.lower()

        plan = {
            "markers": [],
            "browsers": [],
            "allure": False,
            "html": False
        }
        available_markers = get_markers()

        # Test types
        for marker in available_markers:
            if marker in request:
                plan["markers"].append(marker)

        # Browser
        for browser in ["chrome", "firefox", "edge"]:
            if browser in request:
                plan["browsers"].append(browser)

        if any(word in request for word in ["allure", "report", "reports"]):
            plan["allure"] = True
        else:
            plan["html"] = True

        return plan

    @staticmethod
    def build_commands(plan):
        commands = []

        browsers = plan["browsers"] or [None]

        for browser in browsers:
            command = "pytest"

            if plan["markers"]:
                command += f' -m "{" or ".join(plan["markers"])}"'

            if browser:
                command += f" --browser={browser}"

            if plan["allure"]:
                command += " --alluredir=allure-results"

            elif plan["html"]:
                marker_name = "_".join(
                    plan["markers"]) if plan["markers"] else "all"
                command += f" --html=reports/{marker_name}_report.html"

            commands.append(command)

        return commands
