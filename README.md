# ForensicFacebook
This repository was made to finish a college task in the topic of Forensics. This program is used to do forensic analysis on the Facebook and Facebook Messenger app

# Requirements
1. Android phone with SuperUser Access (Rooted)
2. USB Debugging is active
3. Both Facebook and Facebook Messenger are installed in the android phone
4. Python installed (preferably python ver 3.0)
5. ADB and latest USB Driver Installed (if it's not installed you can run the adbinstaller.bat while connected to the android phone)
6. Install the required modules (PySimpleGUI, pure-python-adb, and pillow. Tutorial to install are below)

# Installation
If you have not installed ADB and the latest USB drivers, you can connect to your rooted android phone and run the adbinstaller.bat and follow the instructions to install it.

To install the required python modules, type these commands in the command prompt:
```bash
pip install PySimpleGUI
pip install pure-python-adb
pip install Pillow
```

To install both Facebook and Facebook Messenger, you can find both apps in the Google Play Store in your android phone

# Usage
After meeting all the requirements, you first need to connect your rooted android phone to your device. After that, make sure to allow USB Debugging on your rooted android phone after running adb on your device.

To run adb on your device, type in this command in the command prompt:
```bash
adb devices -l
```

If you see your rooted android phone in the output of the command prompt after putting in the previous command, you can finally start to run the main program by typing in this command in the command prompt of the program's directory:
```bash
python main.py
```

Once the program has started, you can make sure if your rooted android device has actually been connected through adb by clicking the "Refresh" button. This will also pull the facebook and facebook messenger database and put them in a folder named "facebook_databases" and "facebookM_databases" (note in order to pull the latest database folder, you need to make sure there are no folders named "facebook_databases" and "facebookM_databases" in the program directory before you click "Refresh").

In order to analyse and show the data on the program, you first need to choose a target from the dropdown menu and choose a target. After choosing the target the program will ask you for the DB Path of the database that is related to the target. If you don't know which file is related, you can just choose a target and leave the DB Path field empty and click "Scrap", the program will tell you what database file it requires. Once you input the correct target and DB Path, the program will analyse and show you the relevant information regarding the target that was able to be pulled from the android database.
