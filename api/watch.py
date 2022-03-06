from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileSystemMovedEvent
from watchdog.observers import Observer

from config import Config
from lib.decorators import throttle


class EventHandler(FileSystemEventHandler):
    EXCLUDED_DIRECTORIES = (".\\.git", ".\\.idea", ".\\api\\sdk_generation")

    def _is_watched(self, path: str) -> bool:
        if any([directory in path for directory in self.EXCLUDED_DIRECTORIES]):
            return False
        if path.endswith("~"):
            return False

        return True

    def on_moved(self, event: FileSystemMovedEvent):
        self._on_change(event)

    def on_created(self, event: FileSystemEvent):
        self._on_change(event)

    def on_deleted(self, event: FileSystemEvent):
        self._on_change(event)

    @throttle(2)
    def on_modified(self, event: FileSystemEvent):
        self._on_change(event)

    def _on_change(self, event: FileSystemEvent):
        if self._is_watched(event.src_path) and not event.is_directory:
            from api.midi_app import stop_midi_server
            stop_midi_server


def watch_filesystem() -> Observer:
    """
        See https://pythonhosted.org/watchdog/quickstart.html#a-simple-example
        Now using pm2 instead
    """
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, Config.PROJECT_ROOT, recursive=True)
    observer.start()
    return observer
