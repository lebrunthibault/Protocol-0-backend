import PySimpleGUI as sg
import requests


with open("log.txt", "w") as f:
    f.write("I'm here")

layout = [[sg.Input()],
          [sg.Button('Ok', bind_return_key=True, visible=False)]]

window = sg.Window('Search set', layout)

event, values = window.read()  # Event loop or Window.read call


requests.get('http://127.0.0.1:8000/search/%s' % values[0].strip(), auth=('user', 'pass'))

window.close()