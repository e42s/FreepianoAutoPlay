# coding:utf-8
__author__ = 'rmk'

import win32api
import win32con
import win32gui
import win32process
import pythoncom
import pyHook
from Queue import Queue
from ctypes import *
import time
import os
import threading
import subprocess
import signal
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'space': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'num_0': 0x60,
    'num_1': 0x61,
    'num_2': 0x62,
    'num_3': 0x63,
    'num_4': 0x64,
    'num_5': 0x65,
    'num_6': 0x66,
    'num_7': 0x67,
    'num_8': 0x68,
    'num_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    }

class POINT(Structure): 
    _fields_ = [("x", c_ulong),("y", c_ulong)]

def get_mouse_point(): 
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)

def mouse_click(x=None,y=None): 
    if not x is None and not y is None: 
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def mouse_dclick(x=None,y=None): 
    if not x is None and not y is None: 
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def mouse_move(x,y): 
    windll.user32.SetCursorPos(x, y)


class Keyboard:
    def __init__(self, data_path):
        self.musics={}
        self.data_path = data_path
        self.state = "play"
        self.cur_song=0
        pass
    def _read_data(self, path):
        files = os.listdir(path)
        files.sort()
        print "Playlist"
        for i,file in enumerate(files):
            print "Song No.",i,"=>",file
            with open(os.path.join(path, file)) as f:
                self.musics[os.path.basename(file)] = [[item for item in line.split()] for line in f.readlines()]
        pass

    def hook(self):
        # st1art hook manager and receive message globally
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()
        pass
    pass
    def play(self):
        self.fp = subprocess.Popen(r".\freepiano\freepiano.exe")
        self._read_data(self.data_path)
        if len(self.musics) <= 0:
            print "No music file found in", self.data_path, "Exiting"
            exit(-1)

        while (True):
            time.sleep(1)
            local_cur_song = self.cur_song
            print "Playing", local_cur_song, ":", self.musics.keys()[local_cur_song]

            for line in self.musics[self.musics.keys()[local_cur_song]]:
                while self.state == "pause" \
                        or str(win32gui.GetWindowText(win32gui.GetForegroundWindow())).find("piano") == -1:
                    time.sleep(1)
                if not local_cur_song == self.cur_song:
                    break
                # hardware scan code. for those with modified keyboard layout
                hwsc = win32api.MapVirtualKey(VK_CODE[line[0]], 0)
                win32api.keybd_event(VK_CODE[line[0]], hwsc, 0, 0)
                time.sleep(float(line[1]) / 1000)  # press for a long time
                win32api.keybd_event(VK_CODE[line[0]], hwsc, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(float(line[2]) / 1000)
            pass
        pass
    def start_main(self):
        hookthread = threading.Thread(target=self.hook)
        hookthread.start()
        playthread = threading.Thread(target=self.play)
        playthread.start()

    def OnKeyboardEvent(self,event):
        if str(win32gui.GetWindowText(win32gui.GetForegroundWindow())).find("piano") is not -1:
            #control only when piano is not at foreground
            return True
        if chr(event.Ascii).isdigit():
            self.cur_song = int(chr(event.Ascii))
            print "switch to",self.cur_song,":",self.musics.keys()[self.cur_song]
        elif chr(event.Ascii) =='s':
            self.state='pause'
        elif chr(event.Ascii) == 'p':
            self.state='play'
        elif chr(event.Ascii) == 'q':
            self.state='stop'
            exit(0)
        # return True to pass the event to other handlers
        return True

if __name__ == "__main__":

    kb = Keyboard(".\data")
    kb.start_main()
    print "exit"
    exit(0)
