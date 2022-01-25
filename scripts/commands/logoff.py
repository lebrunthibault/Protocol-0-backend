from api.p0_system_api_client import system_client
from lib.ableton import kill_ableton
from scripts.commands.git_backup import push_git_repos


def logoff():
    """ on logoff / hibernation kill processes that would otherwise not work on unhibernate """
    push_git_repos()

    system_client.stop_midi_server()
    kill_ableton()


if __name__ == "__main__":
    logoff()
