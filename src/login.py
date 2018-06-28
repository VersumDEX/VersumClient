from kivy.uix.screenmanager import ScreenManager, Screen

from threading import Thread
import os.path
import json
import platform


if platform.system() == "Linux":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "/data/" 
elif platform.system() == "Windows":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "\\data\\"

class Login(Screen):
    def load_wallet(self, password, username):
        """
        Checks password. If correct, loads wallet file and opens start menu
        """
        wallet = json.load(open(path + "wallet.json", "r"))
        if wallet["password"] == password and wallet["username"] == username:
            self.manager.current = 'wallet'
            self.manager.get_screen("wallet").load_data()
             
