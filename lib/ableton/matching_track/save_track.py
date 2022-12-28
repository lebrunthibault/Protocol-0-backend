from time import sleep

from api.client.p0_script_api_client import p0_script_client
from gui.celery import notification_window
from lib.ableton.interface.browser import preload_set_tracks, toggle_browser
from lib.ableton.interface.interface_color_enum import InterfaceColorEnum
from lib.ableton.interface.track import get_track_coords
from lib.ableton_set import AbletonSet
from lib.enum.notification_enum import NotificationEnum
from lib.keys import send_keys, send_left
from lib.mouse.mouse import drag_to, keep_mouse_position, move_to
from protocol0.application.command.DeleteSelectedTrackCommand import DeleteSelectedTrackCommand


@keep_mouse_position
def save_track_to_sub_tracks(set: AbletonSet):
    preload_set_tracks(set)

    move_to(*get_track_coords(InterfaceColorEnum.TRACK_FOCUSED))

    # drag track to tracks
    drag_to(278, 156)

    sleep(0.5)

    # checking the track was saved
    for i in range(0, 3):
        # save
        send_keys("{ENTER}")
        send_left()
        send_keys("{ENTER}")
        sleep(1)

        if set.is_track_saved:
            break

    assert set.is_track_saved, "Track was not saved"

    send_left()  # fold the set sub track
    toggle_browser()
    p0_script_client().dispatch(DeleteSelectedTrackCommand())
    notification_window.delay("Ok", NotificationEnum.SUCCESS.value)
