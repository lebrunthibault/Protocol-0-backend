global funs := {}, args := {}
global python3 := "C:\Users\thiba\AppData\Local\Programs\Python\Python39\python.exe"
global ableton := "Ableton Live 10 Suite"


executeCliCommand(command)
{
    Run %python3% cli.py %command%, %A_ScriptDir%\.., hide
}

HotkeyCommand(hk, arg*)
{
    Hotkey("", hk, "executeCliCommand", arg*)
}


HotkeyCommandAbleton(hk, arg*)
{
    winActiveCondition = ahk_exe %ableton%.exe
    Hotkey(winActiveCondition, hk, "executeCliCommand", arg*)
}

; Link Hotkey to function
Hotkey(ifWinActiveCondition, hk, fun, arg*)
{
    funs[hk] := Func(fun), args[hk] := arg
    if ifWinActiveCondition {
        Hotkey, IfWinActive, %ifWinActiveCondition%
    }
    Hotkey, %hk%, Hotkey_Handle
    Return

    Hotkey_Handle:
        funs[A_ThisHotkey].(args[A_ThisHotkey]*)

        Return
}
