class PlannerAgent:

    @staticmethod
    def create_plan(request):
        request = request.lower()

        plan = {
            "markers": [],
            "browser": None,
            "allure": False
        }

        # Test types
        for marker in ["smoke", "regression"]:
            if marker in request:
                plan["markers"].append(marker)

        # Browser
        for browser in ["chrome", "firefox", "edge"]:
            if browser in request:
                plan["browser"] = browser
                break
        if any(word in request for word in ["allure", "report", "reports"]):
            plan["allure"] = True

        return plan

    @staticmethod
    def build_command(plan):
        command = "pytest"

        if plan.get("markers"):
            command += f' -m "{" or ".join(plan["markers"])}"'

        if plan.get("browser"):
            command += f' --browser={plan["browser"]}'
        if plan.get("allure"):
            
            command += " --alluredir=allure-results"

        return command

## -------------------------------------------------------------#
# from utils.common_utils import CommonUtils


# class PlannerAgent:

#     EXECUTION_MAP = {
#         "smoke": "pytest -m smoke",
#         "regression": "pytest -m regression",
#         "all": "pytest"
#     }

#     @staticmethod
#     def get_commands(request):
#         request = request.lower()

#         commands = []

#         for test_type, command in PlannerAgent.EXECUTION_MAP.items():
#             if test_type in request:
#                 commands.append(command)

#         return commands
