from gui.celery import notification_window

if __name__ == "__main__":
    notification_window.delay("hello")
