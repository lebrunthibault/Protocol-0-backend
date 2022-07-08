from loguru import logger

from gui.window.message.message import Message
from gui.window.window_factory import WindowFactory
from lib.enum.NotificationEnum import NotificationEnum


class MessageFactory(WindowFactory):
    @classmethod
    def createWindow(
        cls,
        message: str,
        notification_enum: NotificationEnum = NotificationEnum.INFO,
        centered=True,
    ) -> Message:
        logger.info("creating message %s" % notification_enum)
        return Message(message=message, background_color=notification_enum.color, centered=centered)

    @classmethod
    def show_error(cls, message: str):
        cls.createWindow(message=message, notification_enum=NotificationEnum.ERROR).display()
