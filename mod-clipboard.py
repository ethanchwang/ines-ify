import modstring
import tkinter as tk
import subprocess

def copy_to_clipboard(text):
    cmd = 'echo '+text.strip()+'|pbcopy'
    return subprocess.check_call(cmd, shell=True)

def main():
    root = tk.Tk()
    root.withdraw()

    ines_bac = .2
    text = 'hello i am ines'

    while 'ines':
        input('press enter to ines-ify clipboard')
        text = root.clipboard_get()
        
        inesified_str = modstring.randomize_str(text=text,spelling_ability=ines_bac)

        copy_to_clipboard(inesified_str)

if __name__ == '__main__':
    main()