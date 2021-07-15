class AbstractRecognizerNotFoundError(Exception):
    LABEL = ""
    DESCRIPTION = ""

    def __str__(self):
        return self.LABEL
