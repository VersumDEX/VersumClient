from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.image import Image

import json
import os
import sys
from threading import Thread
import platform

from login import Login
from wallet import Wallet
from register import Register
from conf import *

Window.size = (1300, 750)
#Window.fullscreen = True

if platform.system() == "Linux":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__))))
elif platform.system() == "Windows":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__))))

class Manager(ScreenManager):
    register_screen = ObjectProperty(None)
    login_screen = ObjectProperty(None)
    wallet_screen = ObjectProperty(None)

class MainApp(App):
    def build(self):
        """
        Check wheather a wallet file already exists, and choose the correct screen.
        """
        manager = Manager()
        if platform.system() == "Linux":
            self.load_linux(manager)
        elif platform.system() == "Windows":
            self.load_windows(manager)
        return manager

    def load_linux(self, manager):
        #try subprocess.STARTUPINFO to hide console window
        if os.path.exists(path + "/data/wallet.json"):
            cmd = path+"/node/linux/multichaind "+chainname+" -daemon -autosubscribe=assets"
            Thread(target=os.system, args=(cmd,)).start()
            manager.current = 'login'
        else:
            cmd = path+"/node/linux/multichaind "+chaindata+" -daemon -autosubscribe=assets"
            Thread(target=os.system, args=(cmd,)).start()
            manager.current = 'register'

    def load_windows(self, manager):
        if os.path.exists(path + "\\data\\wallet.json"):
            cmd = path+"\\node\\win\\multichaind.exe "+chainname+" -daemon -autosubscribe=assets"
            Thread(target=os.system, args=(cmd,)).start()
            manager.current = 'login'
        else:
            cmd = path+"\\node\\win\\multichaind.exe "+chaindata+" -daemon -autosubscribe=assets"
            Thread(target=os.system, args=(cmd,)).start()
            manager.current = 'register'

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


MainApp().run()

