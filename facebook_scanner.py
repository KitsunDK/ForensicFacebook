import os
import optparse
import sys
import json
from datetime import datetime
import PySimpleGUI as sg
try:
    from common_methods import *
except ImportError:
    sg.Popup("Could not find common_methods.py...")

def get_user_information(core_db):
    try:
        command = "SELECT value from preferences where key in ('/shared/device_id', '/messenger/fcm/token_owner', '/fb_android/user_last_used_app_time');"

        res = pull_from_db(core_db, command)
        data = []
        for item in res[0]:
            last_used = item
        for item in res[1]:
            user_id = item
        for item in res[2]:
            device_id = item

        data.append(user_id)
        data.append(device_id)
        data.append(datetime.fromtimestamp(int(last_used) / 1e3))

        print("User ID : "+str(data[0])+"; Device ID : "+str(data[1])+"; Last Used on : "+str(data[2]))

        print("Data scrap success!")
        return data
    except Exception as e:
        print(e)

def read_fb_contacts(core_db):
    print("(display_name, contact_id, phonebook_section_key, bday_day, bday_month)")
    command = "SELECT display_name, contact_id, phonebook_section_key, bday_day, bday_month" \
            + " from contacts;"

    res = pull_from_db(core_db, command)
    data = []
    dataList = []

    for row in res:
        print(row)
        dataList.append(row[0])
        data.append(row)

    print("Data scrap success!")
    return dataList, data

def read_fb_messages(core_db):

    command = "SELECT sender, text, timestamp_ms " \
            + "from messages" \

    res = pull_from_db(core_db, command)

    data = []
    dataList = []

    for row in res:
        if row[0] is not None:
            row = list(row)
            sender = json.loads(row[0])
            row[0] = sender["name"]
            row[2] = str(datetime.fromtimestamp(int(row[2]) / 1e3))
            print(row)
            dataList.append(row[0])
            data.append(row)

    print("Data scrap success!")
    return dataList, data

def read_fb_searches(core_db):

    command = "SELECT display_name, client_fetch_time_ms " \
            + "from search_items" \

    res = pull_from_db(core_db, command)

    data = []
    dataList = []

    for row in res:
        row = list(row)
        row[1] = str(datetime.fromtimestamp(int(row[1]) / 1e3))
        print(row)
        dataList.append(row[0])
        data.append(row)

    print("Data scrap success!")
    return dataList, data
