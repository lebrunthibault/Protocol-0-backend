from typing import Any


class Event(object):
    def __init__(self, data: Any):
        self.data = data


class Observable(object):
    def __init__(self):
        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def emit(self, data: Any, **attrs):
        e = Event(data=data)
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)
