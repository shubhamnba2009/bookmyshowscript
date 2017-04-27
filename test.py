from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time
import urllib2
from bs4 import BeautifulSoup
from time import sleep
import yagmail
import smtplib
import datetime

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(190)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)

if __name__ == '__main__':
    book_my_show_url = "https://in.bookmyshow.com/buytickets/baahubali-2-the-conclusion-hindi-chennai/movie-chen-ET00050679-MT/20170429"
    while True:
        ltime=datetime.datetime.now()
        requester = urllib2.Request(book_my_show_url, headers={'User-Agent': "Magic Browser"})
        connector = urllib2.urlopen(requester)
        connector_reader = connector.read()
        soup = BeautifulSoup(connector_reader, "lxml")
        text = soup.get_text()
        if "PVR: Velachery, Chennai" in text:
            print "Found at "+ltime.strftime("%X")
            balloon_tip("Jai Mahesmati", "Tickets are for sale dude!!! Hurry up/ndsfsdf sdf/nfsdfsdf/nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        else:
            print "Nope yet Last checked at "+ltime.strftime("%X")
            sleep(60)
  
