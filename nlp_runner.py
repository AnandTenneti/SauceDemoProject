from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.report_agent import ReportAgent

while True:
    request = input(
        "\nWhat tests should I run? (type 'quit' to exit): ").strip()

    if request.lower() == "quit":
        print("Test Execution completed")
        break

    try:
        plan = PlannerAgent.create_plan(request)
        commands = PlannerAgent.build_commands(plan)

        for command in commands:
            print(f"Executing: {command}")
            ExecutionAgent.execute(command)

        if plan["quit"]:
            print("Test execution completed")
            break

        if plan.get("allure"):
            ReportAgent.generate()
            ReportAgent.open()

    except Exception as e:
        print(f"Error: {e}")
