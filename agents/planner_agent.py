import re
from utils.test_registry import get_markers


class PlannerAgent:

    NEGATIVE_WORDS = [
        "but not",
        "without",
        "excluding",
        "exclude",
        "except",
        "not"
    ]

    @staticmethod
    def has_negative(text):
        return any(word in text for word in PlannerAgent.NEGATIVE_WORDS)

    @staticmethod
    def split_text(request_str):
        request_str = request_str.lower()

        for word in PlannerAgent.NEGATIVE_WORDS:
            pattern = rf"\b{re.escape(word)}\b"

            if re.search(pattern, request_str):
                include_text, exclude_text = re.split(
                    pattern,
                    request_str,
                    maxsplit=1
                )

                return include_text.strip(), exclude_text.strip()

        return request_str, ""

    @staticmethod
    def create_plan(request):
        request = request.lower()
        include_request, exclude_request = PlannerAgent.split_text(request)

        plan = {
            "markers": [],
            "exclude_markers": [],
            "browsers": [],
            "allure": False,
            "html": False,
            "parallel": False,
            "workers": 8,
            "quit": "quit" in request,
            "missing": []
        }

        available_markers = get_markers()

       # Detect markers
        for marker in available_markers:

            if re.search(rf"\b{re.escape(marker)}\b", include_request):
                if marker not in plan["markers"]:
                    plan["markers"].append(marker)

            if exclude_request and re.search(
                    rf"\b{re.escape(marker)}\b",
                    exclude_request):
                if marker not in plan["exclude_markers"]:
                    plan["exclude_markers"].append(marker)

        if not plan["markers"]:
            plan["missing"].append("markers")

        # Detect browsers
        available_browsers = ["chrome", "firefox", "edge"]

        for browser in available_browsers:
            if re.search(rf"\b{browser}\b", request):
                if browser not in plan["browsers"]:
                    plan["browsers"].append(browser)

        # Ask for browser if missing
        while not plan["browsers"]:
            browser = input(
                "Which browser do you want to execute? "
            ).strip().lower()

            if browser in available_browsers:
                plan["browsers"].append(browser)
            else:
                print("Please enter chrome, firefox or edge.")

        # Parallel execution
        if "parallel" in request:
            plan["parallel"] = True

            match = re.search(r"(\d+)\s+(workers?|threads?)", request)

            if match:
                plan["workers"] = int(match.group(1))
            else:
                while True:
                    workers = input(
                        "How many workers would you like to use? "
                    ).strip()

                    if workers.isdigit():
                        plan["workers"] = int(workers)
                        break

                    print("Please enter a valid number.")

        # Reports
        if "allure" in request:
            plan["allure"] = True

        if "html" in request:
            plan["html"] = True

        # Default report
        if not plan["allure"] and not plan["html"]:
            plan["html"] = True

        return plan

    @staticmethod
    def build_commands(plan):
        commands = []

        browsers = plan["browsers"] or ["chrome"]

        for browser in browsers:
            command = "pytest"

            marker_expression = ""

            if plan["markers"]:
                marker_expression = " or ".join(plan["markers"])

            if plan["exclude_markers"]:
                exclude_expression = " and ".join(
                    f"not {m}" for m in plan["exclude_markers"])

            if marker_expression:
                marker_expression = (
                    f"({marker_expression}) and {exclude_expression}")
            else:
                marker_expression = exclude_expression

        if marker_expression:
            command += f' -m "{marker_expression}"'

        command += f" --browser={browser}"

        if plan["parallel"]:
            command += f" -n {plan['workers']}"

        # Generate Allure report
        if plan["allure"]:
            command += " --alluredir=allure-results"

            # Generate HTML report
        if plan["html"]:
            marker_name = (
                "_".join(plan["markers"])
                if plan["markers"]
                else "all"
            )
            command += (
                f" --html=reports/{marker_name}_{browser}_report.html"
            )

        commands.append(command)

        return commands
