import asyncio
from asyncio import AbstractEventLoop
from functools import partial
from typing import Any, AsyncIterable

from loguru import logger
from rx import operators as op, create
from rx.core.typing import Observer
from rx.disposable import Disposable


def rx_from_aiter(iter: AsyncIterable, loop: AbstractEventLoop):
    def on_subscribe(observer: Observer, _):
        async def _aio_sub():
            try:
                async for i in iter:
                    observer.on_next(i)
                loop.call_soon(
                    observer.on_completed)
            except Exception as e:
                loop.call_soon(partial(observer.on_error, e))

        task = asyncio.ensure_future(_aio_sub(), loop=loop)
        return Disposable(lambda: task.cancel())  # type: ignore

    return create(on_subscribe)


def rx_debug(name: str, enable=True):
    if enable:
        return op.do_action(lambda val: logger.info(f"{name}: {val}"))
    else:
        return op.do_action(rx_nop)


def rx_print(val: Any) -> None:
    logger.info(f"res ---> {val}")


def rx_nop(*_):
    pass
