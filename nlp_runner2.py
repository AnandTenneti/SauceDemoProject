import argparse
import os
import sys

from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.report_agent import ReportAgent


def run_once(request, open_report=True):
    """Plan, execute, and (optionally) report for a single request.
    Returns the plan dict on success, or None if it raised."""
    try:
        plan = PlannerAgent.create_plan(request)
        commands = PlannerAgent.build_commands(plan)

        for command in commands:
            print(f"Executing: {command}")
            ExecutionAgent.execute(command)

        if plan.get("allure"):
            ReportAgent.generate()
            if open_report:
                ReportAgent.open()

        return plan

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="NLP test runner")
    parser.add_argument(
        "--command", "-c",
        help=(
            "Run a single command non-interactively and exit "
            "(for CI/cron use). Must explicitly name a browser, e.g. "
            "'run smoke tests on chrome with allure report' \u2014 "
            "there's no stdin to prompt for one. "
            "If omitted, starts the interactive prompt."
        ),
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help=(
            "Generate the Allure report but don't launch a browser. "
            "Use this in CI/cron \u2014 there's no display to open one on."
        ),
    )
    args = parser.parse_args()

    # GitHub Actions sets CI=true automatically, so cron runs are
    # safe-by-default even if --no-open is forgotten.
    open_report = not args.no_open and os.environ.get(
        "CI", "").lower() != "true"

    if args.command:
        plan = run_once(args.command, open_report=open_report)
        sys.exit(0 if plan is not None else 1)

    # Interactive mode (unchanged behavior)
    while True:
        request = input(
            "\nWhat tests should I run? (type 'quit' to exit): ").strip()

        if request.lower() == "quit":
            print("Test Execution completed")
            break

        plan = run_once(request, open_report=open_report)

        if plan and plan.get("quit"):
            print("Test execution completed")
            break


if __name__ == "__main__":
    main()
