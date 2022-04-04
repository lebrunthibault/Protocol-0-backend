# Protocol0 script backend and audio libraries

This monolithic repo is the backend of my ([Ableton control surface script](https://github.com/lebrunthibault/Protocol0-Ableton-Surface-Script))

I created it because the python environment in the control surface script executes in ableton and is limited in several
ways
(cannot use threading, asyncio, python3, a bunch of system libraries etc ...)

This repo has none of these limitations and exposes an API to the protocol0 script while also being able to do the opposite : 
calling the script by dispatching script commands.

- I used python 3.7
- I'm on windows 10 (So a some library code is relative to windows (in particular windows and keyboard management))

> legend:
>- script: the ableton control surface script
>- backend : this repo

I didn't work on a real architecture for the backend so it's not as clean as the one for the script.

It is composed of the following packages:

## ./api

The user facing APIs for the backend

### ./api/midi_server
A MIDI server exposing the backend API for consumption by the the [control surface script](https://github.com/lebrunthibault/Protocol0-Ableton-Surface-Script)
(the script communicates only via MIDI)

Also includes client code for
- accessing the backend API from the script (python2)
- accessing the backend API from python3 (needed to access the Backend from outside the MIDI server, see http_server below)
  - NB : due to windows limitations on MIDI ports (only one connection possible), "talking" to the script is only possible from the midi server
  - That means that sending a command to the script from outside the server, we first need to call the server that will forward the command to the script.
- Calling the script from the backend (server push)
  
NB : the backend API is not exposed in the same way as the script API (this should be fixed)
- The backend clients are generated using open API tools. They generate a python client that has a method per exposed backend `Route` method.
  It's nice to do code generation but replacing the `Route` class by Command objects would be simpler
- The script client just dispatches script Command objects over MIDI. 
  It's simpler (even though it creates a hard dependency on the script. but it's ok they are both on the same machine)
  
### ./api/http_server
I've also setup a minimal http server using FastAPI.
This server is there as a gateway to the midi server, for clients that cannot use MIDI
It serves two clients :
- ahk hotkeys : that's because hitting an API is considerably faster than executing scripts with python.
- my stream deck. The server pushes song state changes to the stream deck via a websocket endpoint

It's run independently from the midi server. 

## ./gui
Code used to create notifications and dialog boxes that are displayed on top of ableton interface.
- I'm using [PySimpleGui](https://pysimplegui.readthedocs.io/) based on Tkinter
- Instead of managing threads (Tkinter is picky about thread management) I chose a simpler setup by displaying each window in a celery worker process.
- Now I need to launch celery on startup but at least there is no threading problems and it's easier to stop workers by using celery features than threads.
  
## ./lib
This is the 'monolithic' common backend library used by most backend components.


## ./scripts
Mainly used from the windows system (logon / logoff) or as a way to start the components.

Spawning processes is slow so I'm usually using the http server when I want to hit the backend.

In this package, we have the following sub packages :

### ahk
I've setup a few [Auto Hotkey](https://www.autohotkey.com/) (AHK) hotkeys. Mostly they are a way to call the backend.
Even though some will simply execute a python script (e.g. display the log window)

Doing hotkey detection in python didn't work as well, that's why I kept this (windows) dependency.

In the 'standard' way of executing backend code via ahk, we usually follow these steps :
- hotkey pressed
- ahk dispatches a GET request to the gateway http server
- the gateway route calls the backend (over MIDI)
- the backend code executes, potentially forwarding the command to the script
- In this last case the ahk will in the end trigger a script command (like 'ToggleSceneLoopCommand')
  (a bit complex but fast) 

### commands
body of the click commands

### powershell
Startup command for my terminal

### cli.py
A few cli commands that I run from the terminal / windows task scheduler

### tail_protocol0_logs.py
A script tailing the ableton log file and applying filtering / formatting / colouring
to show only the script information.

## ./sr
Sidekick project : control ableton via vocal commands.
- Sounds crazy but it actually works quite well !
- I stopped using it because well .. it was also a bit stupid ^^. I thought it would liberate me from some button clicking
  but having to talk to the software is a bit boring in the end + it really works only with headphones etc ..
- I set this up using kaldi offline recognition (fastest solution)
- It works by generating before hand a kaldi dictionary 
- On identifying a dictionary word it sends it to the script that matches it to a specific action (like arm, solo ..)
- Been working with rxpy with some success on this. It's great to process a stream of sound / words and filter / process it.
- It's not connected to the script anymore but could be put back quite easily

## Installation

> This script is more here to showcase development techniques and is not ready for distribution / installation but you can try.

- Add to your PYTHON_PATH (both for python2.7 and 3.7) : your remote scripts folder and this folder

- Some commands / libraries are specific to windows, adapt to mac if necessary

### Install dependencies
- `pip install -r ./requirements.txt`
- [Celery](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html)
- [Open Api generator](https://openapi-generator.tech/docs/installation/) to generate the sdk for the backend api
- make
- [AHK](https://www.autohotkey.com/) if you're on windows 
  
### Generate the backend api client
- `make sdk`

### Setup the midi ports
- Create LoopMidi virtual ports (P0_IN and P0_OUT)
- configure ableton midi as so :
    <img width="260px" src="https://raw.githubusercontent.com/lebrunthibault/Protocol-0-backend/master/doc/img/ableton_midi_config.PNG?sanitize=true" alt="ableton screenshot">

  
### Makefile
- most commands I run from the terminal are gathered here (starting processes, sdk generation, tests and lint)

### Start the backend server
- `make celery`
- `make midi_server`
- `make http_server`

I'm using [watchmedo](https://github.com/gorakhargosh/watchdog) to watch file changes for the midi server and celery.
The http server is watched by fastAPI itself.
  

## Development
- `make check` 
