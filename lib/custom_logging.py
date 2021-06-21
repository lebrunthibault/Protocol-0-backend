import logging

from consts import LOGGING_DIRECTORY


def configure_logging(filename: str) -> None:
    logging.basicConfig(
        filename=f"{LOGGING_DIRECTORY}\\{filename}",
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger().addHandler(logging.StreamHandler())
