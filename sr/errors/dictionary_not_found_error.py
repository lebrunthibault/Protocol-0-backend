from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError


class DictionaryNotFoundError(AbstractRecognizerNotFoundError):
    LABEL = "Dictionary not found"
    DESCRIPTION = "<red>Word found doesn't belong to dictionary</>"
