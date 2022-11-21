import PySimpleGUI as sg
import os.path
from PIL import Image
from ppadb.client import Client as AdbClient
import subprocess
try:
    from facebook_scanner import *
except ImportError:
    sg.Popup("Could not find facebook_scanner.py...")

phone_viewer = [
    [sg.Text("Please connect your device!", size=(20, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", filename="public\\vivo.png")],
    [sg.Push(),sg.Button('Refresh'),sg.Push()]
]

scrap = [
    [sg.Push(),sg.Text("Facebook Scrapper"),sg.Push()],
    [
        sg.Text("Target"),
        sg.Push(),
        sg.OptionMenu(values=['user', 'contacts', 'messages', 'searches'], key='_target_', size=(40, 1)),
    ],
    [
        sg.Text("DB Path"),
        sg.Push(),
        sg.In(size=(36, 1), enable_events=True, key="_db_"),
        sg.FileBrowse(),
    ],
    [
        sg.Button('Scrap'),
    ],
]

list_viewer = [
    [sg.Text("List Viewer"),],
    [sg.Listbox([], key="-LIST-", size=(35,20)),]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(phone_viewer),
        sg.VSeperator(),
        sg.Column(scrap),
        sg.VSeperator(),
        sg.Column(list_viewer),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Logcat"),
    ],
    [
        sg.Output(size=(124,15), key="-LOGCAT-"),
    ],
]

window = sg.Window("Facebook Scrapper", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if event == 'Refresh':
        print("Connecting the device...")
        subprocess.call("adb devices -l",shell=True)
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            devices = client.devices()

            i = 1

            for d in devices:
                if i == 1:
                    device = d

            if device.serial != "":
                print(device.shell("logcat", handler=dump_logcat_by_line))
                window["-TOUT-"].update(device.serial +" is Connected!")
                print("Connected!")
                if os.path.exists("facebook_databases") or os.path.exists("facebookM_databases"):
                    print("Either facebook_databases folder or facebookM_databases folder already exists! please delete the folder in order to get the updated database folder")
                else:
                    print("Scrapping the facebook database...")
                    procID = subprocess.Popen("adb shell su", stdin=subprocess.PIPE)
                    procID.communicate(b'cp -r /data/data/com.facebook.katana/databases /sdcard/fbDatabases\ncp -r /data/data/com.facebook.orca/databases /sdcard/fbMDatabases\nexit\nexit')
                    print("Pulling the database...")
                    print(subprocess.call("adb pull /sdcard/fbDatabases facebook_databases"))
                    print(subprocess.call("adb pull /sdcard/fbMDatabases facebookM_databases"))
                    print("Database has been pulled!")
            else:
                window["-TOUT-"].update("Device not found!")
        except Exception as e:
            window["-TOUT-"].update("Device not found!")
            print("Error :", e)
    if event == 'Scrap':
        if not values['_target_']:
            sg.Popup("please enter a target!")
        elif values['_target_'] == "user" and not values['_db_']:
            sg.Popup("please enter the correct database path! (facebook_databases/prefs_db)")
        elif values['_target_'] == "contacts" and not values['_db_']:
            sg.Popup("please enter the correct database path! (facebook_databases/ssus.100000628321702.android_facebook_contacts_db)")
        elif values['_target_'] == "messages" and not values['_db_']:
            sg.Popup("please enter the correct database path! (facebookM_databases/threads_db2)")
        elif values['_target_'] == "searches" and not values['_db_']:
            sg.Popup("please enter the correct database path! (facebookM_databases/search_cache_db)")
        elif not values['_db_']:
            sg.Popup("please enter the correct database path!")
        elif values['_target_'] == "user":
            user = get_user_information(core_db=values['_db_'])
            window["-LIST-"].update(user)
        elif values['_target_'] == "contacts":
            contacts_list, contacts = read_fb_contacts(core_db=values['_db_'])
            window["-LIST-"].update(contacts_list)
        elif values['_target_'] == "messages":
            senders, messages = read_fb_messages(core_db=values['_db_'])
            window["-LIST-"].update(senders)
        elif values['_target_'] == "searches":
            users, time_searched = read_fb_searches(core_db=values['_db_'])
            window["-LIST-"].update(users)

window.close()