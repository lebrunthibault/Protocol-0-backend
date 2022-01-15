from gui.window.decorators.window_decorator import WindowDecorator
from gui.window.window_registry import WindowRegistry


class UniqueWindowDecorator(WindowDecorator):
    def display(self):
        WindowRegistry.close_current_window()
        self.window.display()
        WindowRegistry._CURRENT_INSTANCE = self.window
