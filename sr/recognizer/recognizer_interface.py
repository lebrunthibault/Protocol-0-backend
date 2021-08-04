from abc import abstractmethod

from lib.observable import Observable


class RecognizerInterface(Observable):
    @abstractmethod
    def handle_recording(self):
        raise NotImplementedError

    @abstractmethod
    def load_model(self, sample_rate: int):
        raise NotImplementedError
