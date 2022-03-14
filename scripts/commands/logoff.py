from api.midi_server.p0_backend_api_client import backend_client
from lib.ableton.ableton import kill_ableton
from lib.git import push_git_repos


def logoff():
    """ on logoff / hibernation kill processes that would otherwise not work on unhibernate """
    push_git_repos()

    backend_client.stop_midi_server()
    kill_ableton()
