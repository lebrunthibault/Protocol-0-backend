# Protocol0 script backend and audio libraries

This monolithic repo is the backend of my ableton control surface script ([protocol0](
the https://github.com/lebrunthibault/Protocol-0-Surface-Script))
It started because the python environment in the control surface script executes in ableton and is limited while it in
several ways
(cannot use threading, async, python3, a bunch of system libraries etc ...)
This repo has no limitations and exposes an API to ableton while also being able to call scripts methods via MIDI.

It is composed by the following packages:

- lib : common backend library used by other components
- scripts : globally accessible (via cli / ahk hotkeys and api) scripts for tasks related to ableton / speech
  recognition
- sdk_generation : SDK generation scripts to build 2 clients for backend / surface script bidirectional communication
  via midi
- server : backend API for the script
- sr : speech recognition component (in progress) for identifying specific commands and pushing them to the script. 
