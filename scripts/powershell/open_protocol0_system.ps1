. C:\Users\thiba\google_drive\music\dev\scripts\powershell\libs\VirtualDesktop.ps1

Start-Sleep 20  # waiting for loop midi

vdesk on:4 run:C:\Users\thiba\AppData\Local\Microsoft\WindowsApps\wt.exe --maximized -p "Protocol0 System midi server"

Start-Sleep 3

Get-Desktop 1 | Switch-Desktop
