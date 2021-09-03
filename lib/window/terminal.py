import subprocess


def clear_terminal():
    subprocess.Popen("cls", shell=True).communicate()
