from typing import Any, List

from lib.patterns.observer.Observer import Observer


class Observable():
    observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, data: Any):
        for observer in self.observers:
            observer.update(data)
