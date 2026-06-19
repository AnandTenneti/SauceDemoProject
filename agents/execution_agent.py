import subprocess


class ExecutionAgent:

    @staticmethod
    def execute(command):
        subprocess.run(command, shell=True)
