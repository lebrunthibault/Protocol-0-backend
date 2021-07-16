import subprocess

from config import PROJECT_ROOT


def execute_cli_command(command: str):
    subprocess.Popen(
        [
            "python",
            f"{PROJECT_ROOT}\\scripts\\cli.py",
            command,
        ],
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True,
    )
