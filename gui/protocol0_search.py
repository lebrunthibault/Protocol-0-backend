import PySimpleGUI as sg
import requests

layout = [[sg.Input(key="input")]]

# window = sg.Window("", layout, return_keyboard_events=True, no_titlebar=True)
window = sg.Window("toto", layout, return_keyboard_events=True)


def send_search(search):
    requests.get('http://127.0.0.1:8000/search/%s' % search, auth=('user', 'pass'))


while True:
    event, values = window.read()
    if event.split(":")[0] == "Escape":
        break

    if len(event) == 1 and ord(event) == 13:
        # requests.get('http://127.0.0.1:8000/search/%s' % values["input"].strip(), auth=('user', 'pass'))
        break

    if len(event) == 1:
        search = values["input"]
        if len(search) >= 3:
            send_search(search)


window.close()