#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
#SingleInstance force
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, 2
CoordMode,mouse,screen


#Include %A_ScriptDir%/lib.ahk
; this https://github.com/Ciantic/VirtualDesktopAccessor for switching desktops
#Include %A_ScriptDir%/virtual_desktop.ahk

; Control: ^
; Alt: !
; Shift: +
; Win: #


; global hotkeys
^#+n::
	GoToDesktopNumber(0) ; doing this from ahk, it's faster and works every time
	callBackend("reload_ableton")
return

; ableton hotkeys
#IfWinActive, ahk_exe Ableton Live 10 Suite.exe

^#+s::
    Send ^,  ; works best from ahk
    callBackend("save_set_as_template")
return
^#+l::
	callBackend("tail_logs")
return
^!+l::
	callBackend("tail_logs_raw")
return
^l::
	callBackend("toggle_scene_loop")
return
^space::
	callBackend("fire_scene_to_position")
return

!f:: ; fold / unfold set
	Send `t
	Send !u
	Send !u
	Send `t
return

#IfWinActive
