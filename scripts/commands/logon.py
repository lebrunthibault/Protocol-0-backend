import subprocess
import sys

from lib.git import pull_git_repos


def logon():
    startup_script = "C:\\Users\\thiba\\dev\\scripts\\startup.ps1"
    subprocess.Popen(["powershell.exe",
                      "invoke-expression",
                      startup_script],
                     stdout=sys.stdout)
    pull_git_repos()
