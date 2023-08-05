#oython 1.0.0 
#func 0.0.1

import os
import pygame
import requests
import platform
import urllib.request
import urllib.parse
from lxml import etree

user_system = platform.system()

def broadcast(mp3,time):

    if not isinstance(mp3,str):
        err("请正确输入mp3文件地址")
    pygame.mixer.init()
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()
    if time is not None:
        time.sleep(time)
        pygame.mixer.music.stop()
    elif time != 0:
        time.sleep(time)
        pygame.mixer.music.stop()
        

def desktop_path():
    return os.path.join(os.path.expanduser("~"), 'Desktop')+"/"
            
def save_user():
    try:
        path = desktop_path()
        file = path + "用户.txt"
        f = open(file,"x")
        us = input("请输入用户名：")
        f.write(us)
        f.close()
        fn = open(file,"r")
        fnr = fn.read()
        fn.close()
        return us
    except:
        fn = open(file,"r")
        fnr = fn.read()
        fn.close()
        return fnr

def find_letter(a,b):
    c = False
    for letter in a:
        if letter == b:
            c = True
            return True
            break
    if c == False:
        return c
