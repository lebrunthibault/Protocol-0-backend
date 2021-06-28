#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
#SingleInstance force
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, 2
CoordMode,mouse,screen

#Include %A_ScriptDir%/utils.ahk

; Control: ^
; Alt: !
; Shift: +
; Win: #


; global hotkeys
HotkeyCommand("^#+n", "reload_ableton")
HotkeyCommand("^#+l", "refresh_logs")

; literal hotkeys should be defined *after* the executable code
#IfWinActive, ahk_exe Ableton Live 10 Suite.exe
^#+s::
    Send ^,  ; works best from ahk
    executeCliCommand("save_set_as_template")
return
#IfWinActive

#IfWinActive, ahk_exe Ableton Live 10 Suite.exe
^+f::
    executeCliCommand("search_set_gui")
return
#IfWinActive

; closes clink terminal window
#IfWinActive, ahk_class ConsoleWindowClass
    !F4::WinClose, A
#IfWinActive