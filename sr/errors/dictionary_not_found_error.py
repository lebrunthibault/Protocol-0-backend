from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError


class DictionaryNotFoundError(AbstractRecognizerNotFoundError):
    LABEL = "Dictionary not found"
