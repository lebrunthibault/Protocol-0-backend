from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError


class RecognizerNotFoundError(AbstractRecognizerNotFoundError):
    LABEL = "Kaldi not found"
