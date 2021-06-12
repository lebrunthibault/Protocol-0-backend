from a_protocol_0.enums.CommandEnum import CommandEnum
from django.urls import path

from .views import MainView

urlpatterns = [
    # path('', MainView.index, name='index'),
    path('test', MainView.test, name='test'),
    path('400', MainView.bad_request, name='400'),
    path('search/<str:search>', MainView.search, name='search'),
    path('action', MainView.action, name='action'),
]

simple_commands = {
    CommandEnum.SHOW_PLUGINS: MainView.show_plugins,
    CommandEnum.SHOW_HIDE_PLUGINS: MainView.show_hide_plugins,
    CommandEnum.HIDE_PLUGINS: MainView.hide_plugins,
    CommandEnum.PIXEL_HAS_COLOR: MainView.pixel_has_color,
    CommandEnum.ARROW_UP: MainView.arrow_up,
    CommandEnum.RELOAD_ABLETON: MainView.reload_ableton,
    CommandEnum.SHOW_WINDOWS: MainView.show_windows,
}

for command_enum, method in simple_commands.items():
    urlpatterns.append(
        path(command_enum.name.lower(), method, name=command_enum.name.lower()))
