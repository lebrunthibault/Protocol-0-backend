from abc import abstractmethod

from rx import Observable
from typing_extensions import Protocol


class AudioSourceInterface(Protocol):
    name: str
    sample_rate: int
    sample_width: int

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}: {self.sample_rate} Hz, {self.sample_width * 8} bits"

    @abstractmethod
    def make_observable(self) -> Observable:
        """creates an Observable[AudioSegment]"""
        raise NotImplementedError
