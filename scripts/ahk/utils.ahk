global funs := {}, args := {}

executeCliCommand(command)
{
    Run py cli.py %command%, %A_ScriptDir%\.., hide
}

HotkeyCommand(hk, arg*)
{
    Hotkey("", hk, "executeCliCommand", arg*)
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
