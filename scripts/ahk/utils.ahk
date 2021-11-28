global funs := {}, args := {}

executeCliCommand(command, args*)
{
    arg_string := Join(" ", args*)
    Run py cli.py %command% %arg_string%, %A_ScriptDir%\.., hide
}

HotkeyCommand(hk, args*)
{
    Hotkey("", "", hk, "executeCliCommand", args*)
}

HotkeyCommandNoPycharm(hk, args*)
{
    Hotkey("", "ahk_exe pycharm64.exe", hk, "executeCliCommand", args*)
}

; Link Hotkey to function
Hotkey(ifWinActiveCondition, ifWinNotActiveCondition, hk, fun, arg*)
{
    funs[hk] := Func(fun), args[hk] := arg
    if ifWinActiveCondition {
        Hotkey, IfWinActive, %ifWinActiveCondition%
    } else if ifWinNotActiveCondition {
        Hotkey, IfWinNotActive, %ifWinNotActiveCondition%
    }
    ; strange we don't use else but it works like this
    Hotkey, %hk%, Hotkey_Handle
    Return

    Hotkey_Handle:
        funs[A_ThisHotkey].(args[A_ThisHotkey]*)
        Return
}

Join(sep, params*) {
    str := ""
    for index,param in params
        str .= param . sep
    return SubStr(str, 1, -StrLen(sep))
}
