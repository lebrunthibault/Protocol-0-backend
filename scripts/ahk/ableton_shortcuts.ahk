#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
; SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, 2
CoordMode,mouse,screen



#Include %A_ScriptDir%/utils.ahk

; closes clink terminal window
#IfWinActive, ahk_class ConsoleWindowClass
    !F4::WinClose, A
#IfWinActive

#IfWinActive ahk_exe Ableton Live 10 Suite.exe
; Control: ^
; Alt: !
; Shift: +
; Win: #
; EnvGet, abletonFullVersion, AbletonVersion
; versionArray := StrSplit(abletonFullVersion, ".")
; MajorVersion := versionArray[1]
; global ableton := "Ableton Live %MajorVersion% Suite"
; global ableton := "Ableton Live 10 Suite"

#SingleInstance force

; global hotkeys
Hotkey("", "^#+n", "reloadAbleton")
Hotkey("", "^#+l", "refreshLogs")
; ableton hotkeys
HotkeyAbleton("^+f", "searchSet")
HotkeyAbleton("^#+s", "saveAndSetAsTemplate")

; literal hotkeys should be defined *after* the executable code
^+z::
    Send ^y
return

refreshLogs()
{
    MsgBox "toto"
    setkeydelay, 0
    Send {Esc}
    Sleep 1000

    loop 10 {
        Send {LWin down}
        Sleep 10
    }
    Send {LWin up}
    Sleep 100
    Send tailAbletonLogs.ps
    Sleep 100
    Send 1
    Sleep 500
    Send {Enter}
}

searchSet()
{
    Run search_set.bat, %A_ScriptDir%\..\python\commands, hide
}


saveAndSetAsTemplate()
{
    Send ^,
    MouseClick, left, 711, 351 ; click on File Folder
    MouseClick, left, 1032, 201
    Sleep 50
    MouseClick, left, 1032, 228
    Sleep 50
    Send {Enter}
    Sleep 200
    Send {Escape}
}

;#IfWinActive