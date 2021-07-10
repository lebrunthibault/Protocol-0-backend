class Event(object):
    def __init__(self, type: str):
        self.type = type


class Observable(object):
    def __init__(self):
        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def emit(self, type: str, **attrs):
        e = Event(type=type)
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)
