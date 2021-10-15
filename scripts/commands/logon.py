import subprocess
import sys

from scripts.commands.git_backup import pull_git_repos


def logon():
    startup_script = "C:\\Users\\thiba\\google_drive\\music\\dev\\scripts\\startup.ps1"
    p = subprocess.Popen(["powershell.exe",
                          "invoke-expression",
                          startup_script],
                         stdout=sys.stdout)
    pull_git_repos()


if __name__ == "__main__":
    logon()
