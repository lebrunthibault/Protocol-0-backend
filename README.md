# Protocol0 script backend and audio libraries

This monolithic repo is the backend of my ableton control surface
script ([protocol0 repo](https://github.com/lebrunthibault/Protocol-0-Surface-Script))
I created it because the python environment in the control surface script executes in ableton and is limited in several
ways
(cannot use threading, asyncio, python3, a bunch of system libraries etc ...)
This repo has no limitations and exposes an API to ableton while also being able to do the opposite : calling exposed
scripts methods via MIDI.

> legend:
>- script: the ableton control surface script
>- backend : this repo

It is composed of the following packages:

- lib : common backend library used by backend components
- scripts : globally accessible (via cli / ahk hotkeys and api) scripts for tasks related to ableton / speech
  recognition
- sdk_generation : SDK code generation scripts to build 2 clients for backend / surface script bidirectional
  communication via midi (why 2 and not 1 ? because midi protocol is much simpler than http and unidirectional. Also
  typing gets stronger).
- server : backend API for the script. Using openAPI as API contract
- sr : speech recognition component (in progress) for identifying specific vocal commands and pushing them to the
  script.

### Installation

> This script is more here to showcase development techniques and is not ready for distribution / installation but you can try.

- Add to your PYTHON_PATH : your remote scripts folder and this folder

- Some commands are specific to windows, adapt to mac if necessary
- Create LoopMidi virtual ports (P0_IN and P0_OUT)
- Install openapi-generator, make

- `pip install -r ./requirements.txt`
- `make sdk`
- `make midi`
