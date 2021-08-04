from typing import Any

from loguru import logger
from rx import operators as op


def rx_debug(name: str, enable=True):
    if enable:
        return op.do_action(lambda val: logger.info(f"{name}: {val}"))
    else:
        return op.do_action(rx_nop)


def rx_print(val: Any) -> None:
    logger.info(f"res ---> {val}")


def rx_nop(*_):
    pass
