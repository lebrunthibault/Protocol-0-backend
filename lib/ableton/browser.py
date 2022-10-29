from time import sleep

from lib.keys import send_keys, send_up, send_down


def search(search: str):
    send_keys("^f")
    sleep(0.1)
    send_keys(search)


def load_rev2_track():
    search('"Default.als"')
    sleep(0.2)

    for _ in range(12):
        send_down()

    send_up()
    send_up()

    send_keys("{ENTER}")


def load_minitaur_track():
    search('"Default.als"')
    sleep(0.2)

    for _ in range(12):
        send_down()

    send_up()

    send_keys("{ENTER}")
