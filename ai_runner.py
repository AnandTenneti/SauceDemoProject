from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.report_agent import ReportAgent

request = input("What tests should I run? ")

plan = PlannerAgent.create_plan(request)
commands = PlannerAgent.build_commands(plan)
for command in commands:
    print(f"Executing: {command}")
    ExecutionAgent.execute(command)
    if plan["allure"]:
        ReportAgent.generate()
        ReportAgent.open()
