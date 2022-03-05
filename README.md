# Protocol0 script backend and audio libraries

This monolithic repo is the backend of my ableton control surface
script ([protocol0 repo](https://github.com/lebrunthibault/Protocol-0-Surface-Script))
I created it because the python environment in the control surface script executes in ableton and is limited in several
ways
(cannot use threading, asyncio, python3, a bunch of system libraries etc ...)
This repo has none of these limitations and exposes an API to the protocol0 script while also being able to do the opposite : 
calling the script by dispatching script commands. 

> legend:
>- script: the ableton control surface script
>- backend : this repo

I didn't work on a real architecture for the backend so it's not as clean as the one for the script.

It is composed of the following packages:

## api
MIDI server exposing the backend API for the script. Also includes client code for
- accessing the backend API from the script (python2)
- accessing the backend API from python3 (for example when executing a backend script from AHK)
  - NB : due to windows limitations on MIDI ports (only one connection possible), "talking" to the script is only possible from the midi server
  - That means that sending a command to the script from outside the server, we first need to call the server that will forward the command to the script.
- Calling the script from the backend
  
NB : the backend API is not exposed in the same way as the script API (this should be fixed)
- The backend clients are generated using open API tools that creates a client that has a method per exposed backend `Route` method
  It's nice to do code generation but replacing the `Route` class by Command objects would be simpler
- The script client just dispatches script Command objects over MIDI. It's simpler (even though it creates a hard dependency on the script. but it's ok they are both on the same machine)
  
## gui
Code used to create notifications and dialog boxes that are displayed on top of ableton interface.
- I'm using [PySimpleGui](https://pysimplegui.readthedocs.io/) based on Tkinter
- Instead of managing threads (Tkinter is picky about thread management) I chose a simpler setup by displaying each window in a celery worker process.
- Now I need to launch celery on startup but at least there is no threading problems and it's easier to stop workers by using celery features than threads.
  
## lib
This is the 'monolithic' common backend library used by backend components.


## scripts
Entrypoint for direct script execution. scripts can be executed via the command line directly (not really useful except for testing)
but can be executed from ahk. That's more interesting, see below.

### ahk
I've setup a few ahk hotkeys. Mostly they are a way to forward them to the backend.
Even though some will simply execute a python script (e.g. display the log window)
Doing hotkey detection in python didn't work as well, that's why I kept this dependency.
In this case we have usually :
- hotkey pressed
- ahk executes a python script using the `cli.py` command line (using [click](https://click.palletsprojects.com/en/8.0.x/))
- the click cli command calls the backend (over MIDI)
- the backend code executes, potentially forwarding the command to the script
- In this last case the ahk will in the end trigger a script command (like 'loop the current scene') (a bit complex but it's the only way really 

### commands
body of the click commands

## powershell
Startup command for the midi server and celery

## sr
Sidekick project : control ableton via vocal commands.
- Sounds crazy but it actually works quite well !
- I stopped using it because well .. it was also a bit stupid ^^. I thought it would liberate me from some button clicking
  but having to talk to the software is a bit boring in the end + it really works only with headphones etc ..
- I set this up using kaldi offline recognition (fast)
- It works by generating before hand a kaldi dictionary 
- On identifying a dictionary word it sends them to the script that would match it to a specific action (like arm, solo ..)
- Been working with rxpy with some success on this. It's great to process a stream of sound / words and filter / process it.
- It's not linked to the script anymore but could be put back quite easily

## Installation

> This script is more here to showcase development techniques and is not ready for distribution / installation but you can try.

- Add to your PYTHON_PATH : your remote scripts folder and this folder

- Some commands are specific to windows, adapt to mac if necessary
- Create LoopMidi virtual ports (P0_IN and P0_OUT)
- Install openapi-generator (if you want to modify the backend api), make

- `pip install -r ./requirements.txt`
- `make sdk` to generate the backend api clients
- See the `scripts\powershell` folder to startup the 
- configure ableton midi as so :
  <img width="260px" src="https://raw.githubusercontent.com/lebrunthibault/Protocol-0-backend/master/doc/img/ableton_midi_config.PNG?sanitize=true" alt="ableton screenshot">
