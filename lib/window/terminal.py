import subprocess


def clear_terminal():
    subprocess.Popen("cls",
                     shell=True).communicate()  # I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine
