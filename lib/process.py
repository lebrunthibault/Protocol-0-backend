import os.path
import subprocess
import sys


def execute_in_new_window(path: str, *args):
    assert path.endswith(".py")
    cwd = os.path.dirname(path)
    basename = os.path.basename(path)
    p = subprocess.Popen(["powershell.exe",
                          "invoke-expression",
                          f"'cmd /c start powershell -Command {{ set-location \"%s\"; py {basename} {' '.join(args)} }}'" % cwd],
                         stdout=sys.stdout)
    p.communicate()
