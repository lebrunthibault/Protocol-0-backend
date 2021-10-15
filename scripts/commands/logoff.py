from lib.ableton import kill_ableton
from lib.terminal import kill_system_terminal_windows
from scripts.commands.git_backup import push_git_repos


def logoff():
    """ on logoff / hibernation kill processes that would otherwise not work on unhibernate """
    push_git_repos()

    kill_system_terminal_windows()
    kill_ableton()
    # toto


if __name__ == "__main__":
    logoff()
