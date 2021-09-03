class AbstractRecognizerNotFoundError(Exception):
    LABEL = ""

    def __str__(self):
        return self.LABEL
