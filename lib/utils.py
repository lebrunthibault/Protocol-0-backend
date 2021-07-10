import time


def filename_datetime():
    return time.strftime("%Y%m%d-%H%M%S")


def flatten(list: list) -> list:
    return [item for sublist in list for item in sublist]
