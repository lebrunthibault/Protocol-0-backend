from typing import Any

from lib.patterns.observer.Observer import Observer


class Observable():
    def attach(self, observer: Observer):
        pass

    def detach(self, observer: Observer):
        pass

    def notify(self, data: Any):
        pass
