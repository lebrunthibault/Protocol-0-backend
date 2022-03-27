import os
import subprocess

from loguru import logger

blog_repo = "C:\\Users\\thiba\\dev\\blog"

git_repositories = [
    "C:\\Users\\thiba\\dev\\scripts",
    blog_repo,
    # "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts",
    "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts\\protocol0",
    "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts\\protocol0_midi",
    "C:\\Users\\thiba\\dev\\protocol0_backend",
    "C:\\Users\\thiba\\dev\\protocol0_stream_deck",
]

git_repositories_to_pull = [
    blog_repo
]


def _git_repo_push(path: str):
    if not os.path.exists(path):
        logger.error(f"path {path} does not exist")
        return

    logger.info(f"Checking {path}")
    cwd = os.getcwd()
    os.chdir(path)
    subprocess.run(["git", "add", "."])
    try:
        subprocess.check_call(["git", "commit", "-a", "-m", "'backup'"], shell=False,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logger.info("Untouched")
        return

    subprocess.run(["git", "push"])
    logger.info("Backed up")
    os.chdir(cwd)


def _git_repo_pull(path: str):
    if not os.path.exists(path):
        logger.error(f"path {path} does not exist")
        return

    logger.info(f"Checking {path}")
    cwd = os.getcwd()
    os.chdir(path)
    subprocess.run(["git", "pull"])
    logger.info("Repo pulled")
    os.chdir(cwd)


def push_git_repos():
    for git_repository in git_repositories:
        _git_repo_push(path=git_repository)


def pull_git_repos():
    for git_repository in git_repositories_to_pull:
        _git_repo_pull(path=git_repository)
