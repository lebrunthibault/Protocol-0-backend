import os
import subprocess

from loguru import logger

git_repositories = [
    "C:\\Users\\thiba\\Google Drive\\music\\ableton projects",
    "C:\\Users\\thiba\\Google Drive\\music\\dev\\scripts",
    "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts",
    "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts\\a_protocol_0",
    "C:\\Users\\thiba\\Google Drive\\music\\dev\\Protocol0 System",
    "C:\\Users\\thiba\\Google Drive\\music\\dev\\speech_recognition",
    "C:\\Users\\thiba\\Google Drive\\music\\software presets\\Ableton User Library\\Presets\\MIDI Effects\\Max MIDI Effect",
]


def _git_repo_backup(path: str):
    if not os.path.exists(path):
        logger.error(f"path {path} does not exist")
        return

    logger.info(f"Checking {path}")
    cwd = os.getcwd()
    os.chdir(path)
    subprocess.run(["git", "add", "."])
    try:
        subprocess.check_call(["git", "commit", "-a", "-m", "'backup'"], stdout=None)
    except subprocess.CalledProcessError:
        logger.info(f"{path} untouched")
        return

    subprocess.run(["git", "push"])
    logger.info(f"{path} backed up")
    os.chdir(cwd)


def backup_git_repos():
    for git_repository in git_repositories:
        _git_repo_backup(path=git_repository)
