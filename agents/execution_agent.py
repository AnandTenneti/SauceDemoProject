import subprocess


class ExecutionAgent:

    @staticmethod
    def execute(command):
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(
                f"⚠️  Tests failed or error occurred (exit code {result.returncode})")
