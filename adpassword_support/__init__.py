#! /usr/bin/env python
#
# Support module generated by PAGE version 4.7
# In conjunction with Tcl version 8.6
#    Jun 22, 2016 02:53:04 PM


import sys
import subprocess

import os
import pwd

import ldap
import ldap.sasl

import re
import time,datetime

import locale
locale.setlocale(locale.LC_ALL, '')


def locate_ad_ldap_data():
    ldap_server="" 
    realm=""
    cmd = subprocess.Popen('net ads info', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in cmd.stdout.readlines():
        items=re.search("LDAP server name:\s*(.*)\n", line)
        if items:
            ldap_server=items.groups(0)[0]
            break

    if (cmd.wait() == 0):
        print _("LDAP Server:"), ldap_server
        return ldap_server


def query_user_password_policy(ldap_server,user):
    password_expiration_datetime=""
    ldap_server=ldap_server.lower()
    rpccall='rpcclient %s -k -c "queryuser %s"' % (ldap_server,user)
    print rpccall 
    cmd = subprocess.Popen(rpccall, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in cmd.stdout.readlines():
        items=re.search("Password must change Time:\s*(.*)\n", line)
        if items:
            cleardate=items.groups(0)[0]
# If password never expires, just exit.
            if (cleardate == "never"):
                sys.exit()
            else:
                password_expiration_datetime=datetime.datetime.strptime(cleardate, "%a, %d %b %Y %H:%M:%S %Z")
            break
   
    if (cmd.wait() == 0):
        print _("Password Must Change:"), cleardate
        return password_expiration_datetime

def get_username():
    return pwd.getpwuid(os.getuid()).pw_name


try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

def set_Tk_var(alert):
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global lbl_pwd_expiration
    lbl_pwd_expiration = StringVar()
    lbl_pwd_expiration.set(alert)

def bt_cancel_clicked():
    sys.exit()

def bt_chg_pwd_clicked():
    print('adpassword_support.bt_chg_pwd_clicked')
    global top_level
    top_level.destroy()
    import adpassword_change
    win_change=adpassword_change.vp_start_gui()     


def init(top, gui, *args, **kwargs):
    global w, top_level, root 
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
#    import adpassword
    adpassword.vp_start_gui()


