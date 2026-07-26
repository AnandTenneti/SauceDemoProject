from unittest.mock import patch

from agents.execution_agent import ExecutionAgent


@patch("agents.execution_agent.subprocess.run")
def test_execute_command(mock_run):
    ExecutionAgent.execute("pytest")

    mock_run.assert_called_once()