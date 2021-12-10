. C:\Users\thiba\google_drive\music\dev\scripts\powershell\libs\VirtualDesktop.ps1

Start-Sleep 1

vdesk on:3 run:pycharm64.exe

Start-Sleep 10  # waiting for loop midi

vdesk on:4 run:C:\Users\thiba\AppData\Local\Microsoft\WindowsApps\wt.exe --maximized -p "Protocol0 System midi server"

Start-Sleep 1

Get-Desktop 1 | Switch-Desktop
#invoke-item 'C:\\Users\\thiba\\OneDrive\\Bureau\\midi_server.lnk'
