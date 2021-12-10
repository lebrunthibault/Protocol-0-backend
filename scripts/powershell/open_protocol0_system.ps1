. C:\Users\thiba\google_drive\music\dev\scripts\powershell\libs\VirtualDesktop.ps1

vdesk on:3 run:pycharm64.exe

Start-Sleep 12  # waiting for loop midi

vdesk on:4 run:C:\Users\thiba\AppData\Local\Microsoft\WindowsApps\wt.exe -p "Protocol0 System midi server"

Start-Sleep 2

Get-Desktop 1 | Switch-Desktop
#invoke-item 'C:\\Users\\thiba\\OneDrive\\Bureau\\midi_server.lnk'
