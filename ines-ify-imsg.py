import modstring
import os
from tqdm import tqdm
from functools import partialmethod

def send_imsg(phone_number,msg):
    os.system(f'osascript sendMessage.applescript {phone_number} "{msg}"')

def main():
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

    ines_bac = .2
    with open('target_phonenum.txt') as file:
        phone_num = file.read()

    text = input('enter message:\n')

    msg = modstring.randomize_str(text=text,spelling_ability=ines_bac)

    send_imsg(phone_number=phone_num,msg=msg)
    print(f'sent: {msg}')

if __name__ == '__main__':
    main()