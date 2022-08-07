#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
#SingleInstance force
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, 2
CoordMode,mouse,screen

#Include %A_ScriptDir%/lib.ahk

; Control: ^
; Alt: !
; Shift: +
; Win: #

; loop must be before any return
Loop, 9 {
    HotKey, ^NumPad%A_Index%, FireSceneToPosition
}
Return

; global hotkeys
^#+n::
	callBackend("reload_ableton")
return
^#+l::
	callBackend("tail_logs")
return

; ableton hotkeys
#IfWinActive, ahk_exe Ableton Live 10 Suite.exe
^#+s::
    Send ^,  ; works best from ahk
    callBackend("save_set_as_template")
return
^!+l::
	callBackend("tail_logs_raw")
return
^+a::
	callBackend("arm")
return
^l::
	callBackend("toggle_scene_loop")
return
^space::
	callBackend("fire_selected_scene")
return
+space::
	callBackend("fire_scene_to_position")
return
^NumPad0::
	callBackend("fire_scene_to_position", "-1")
return
FireSceneToPosition:
if WinActive("ahk_exe Ableton Live 10 Suite.exe") {
    barLength:=SubStr(A_ThisHotkey,"^NumPad") - 1
	callBackend("fire_scene_to_position", barLength)
}
Return
^Left::
	callBackend("scroll_scene_position", "left")
return
^Right::
	callBackend("scroll_scene_position", "right")
return
^+Left::
	callBackend("scroll_scene_tracks_fine", "left")
return
^+Right::
	callBackend("scroll_scene_tracks_fine", "right")
return
+Left::
	callBackend("scroll_scene_tracks", "left")
return
+Right::
	callBackend("scroll_scene_tracks", "right")
return
^Up::
	callBackend("scroll_scenes", "up")
return
^Down::
	callBackend("scroll_scenes", "down")
return
^e::
	callBackend("toggle_clip_notes")
return

!f:: ; fold / unfold set
	Send `t
	Send !u
	Sleep 10
	Send !u
	Send `t
return

#IfWinActive
