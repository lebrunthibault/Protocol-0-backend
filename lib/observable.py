from typing import Any, Callable


class Event(object):
    def __init__(self, data: Any):
        self.data = data


class Observable(object):
    def __init__(self):
        self.callbacks = []

    def subscribe(self, type, callback: Callable):
        self.callbacks.append((type, callback))

    def emit(self, data: Any, **attrs) -> None:
        e = Event(data=data)
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for (type, callback) in self.callbacks:
            if isinstance(data, type):
                callback(e.data)
