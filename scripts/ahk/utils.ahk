global funs := {}, args := {}

join(array) {
    str := ""
    For i, value In array
       str .= "|" . value
    str := LTrim(str, "|")

    return str
}

clearSearchBox()
{
	Send ^f
	Send ^a
	Send {BackSpace}
	Sleep 100
}

; Link Hotkey to function
HotkeyAbleton(hk, fun, arg*)
{
    winActiveCondition = ahk_exe %ableton%.exe
    Hotkey(winActiveCondition, hk, fun, arg*)
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
