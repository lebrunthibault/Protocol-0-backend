# waiting for loop midi
. C:\Users\thiba\google_drive\music\dev\scripts\powershell\libs\VirtualDesktop.ps1
vdesk on:3 run:pycharm64.exe
Start-Sleep 4
vdesk on:4 run:C:\Users\thiba\AppData\Local\Microsoft\WindowsApps\wt.exe -p "Protocol0 System midi server"
Start-Sleep 1
Get-Desktop 1 | Switch-Desktop
#invoke-item 'C:\\Users\\thiba\\OneDrive\\Bureau\\midi_server.lnk'
