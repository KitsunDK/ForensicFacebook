import sqlite3, os, sys, platform
import PySimpleGUI as sg
from ppadb.client import Client as AdbClient
from datetime import datetime as dt

def pull_from_db(db, command, facebook_name=False):
    '''Send queries to a database and return the results'''
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(command)
        return c.fetchall()
    except Exception as e:
        if facebook_name:
            return [("Name Unavailable %s" % e,)]
        else:
            sg.Popup("Error reading the database: %s" % e)

def dump_logcat_by_line(connect):
    file_obj = connect.socket.makefile()
    for index in range(0, 10):
        print("Line {}: {}".format(index, file_obj.readline().strip()))

    file_obj.close()
    connect.close()
