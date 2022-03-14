from gui.window.message.message import Message
from gui.window.window_factory import WindowFactory
from lib.enum.ColorEnum import ColorEnum
from lib.enum.NotificationEnum import NotificationEnum


class MessageFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO) -> Message:
        if notification_enum == NotificationEnum.INFO:
            return Message(message=message, background_color=ColorEnum.INFO)
        elif notification_enum == NotificationEnum.SUCCESS:
            return Message(message=message, background_color=ColorEnum.SUCCESS)
        elif notification_enum == NotificationEnum.WARNING:
            return Message(message=message, background_color=ColorEnum.WARNING)
        elif notification_enum == NotificationEnum.ERROR:
            return Message(message=message, background_color=ColorEnum.ERROR, title="P0 Error Message")
        else:
            raise NotImplementedError("cannot find Message class for enum %s" % notification_enum)

    @classmethod
    def show_error(cls, message: str):
        cls.createWindow(message=message, notification_enum=NotificationEnum.ERROR).display()
