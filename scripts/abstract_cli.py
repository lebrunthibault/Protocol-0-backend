import asyncclick as click
from loguru import logger

from lib.log import configure_logging
from lib.terminal import clear_terminal


@click.group()
async def cli() -> None:
    configure_logging()
    clear_terminal()
    logger.info("launching cli command")
