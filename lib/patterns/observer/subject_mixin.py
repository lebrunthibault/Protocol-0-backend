import abc
from typing import Any, Set

from lib.patterns.observer.observer_mixin import ObserverMixin


class SubjectMixin(abc.ABC):
    observers_attr_name = "_observers"

    @property
    def observers(self) -> Set[ObserverMixin]:
        if not getattr(self, self.observers_attr_name, None):
            setattr(self, self.observers_attr_name, set())
        return getattr(self, self.observers_attr_name)

    def attach(self, observer: ObserverMixin):
        if observer not in self.observers:
            self.observers.add(observer)

    def detach(self, observer: ObserverMixin):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify(self, data: Any):
        for observer in self.observers:
            observer.update(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observers.clear()
