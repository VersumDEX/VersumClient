from kivy.properties import ObjectProperty, NumericProperty, \
     ReferenceListProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.uix.dropdown import DropDown

from requests import post
from Savoir import Savoir
import platform
import json
import os
from conf import *

if platform.system() == "Linux":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "/data/"
    rpc = "/home/"+os.getenv('username')+"/.multichain/"+chainname+"/multichain.conf"
elif platform.system() == "Windows":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "\\data\\"
    rpc = "C:\\Users\\"+os.getenv('username')+"\\AppData\\Roaming\\MultiChain\\"+chainname+"\\multichain.conf"


class CustomDropDownMenu(DropDown):
    def paper_wallet(self):
        with open(rpc, "r") as rpcfile: 
            data = rpcfile.read().split("\n")
            rpcuser = data[0][8:]
            rpcpassword = data[1][12:]
            rpchost = 'localhost'
            rpcport = '6804'
            chainname= "testchain"
        api = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
        keypair = api.createkeypairs(1)[0]
        paperwallet = "Private Key: " + keypair["privkey"]+ " \n\n"\
        + "Public Key: " + keypair["pubkey"]+ " \n\n"\
        + "Address: " + keypair["address"]
        data = json.dumps({"vaddress":keypair["address"]})
        url = "http://185.239.236.219/register"
        r = post(url, data).text
        lay = RelativeLayout()
        if r == "Success":
            lbl = Label(text="""
Note: This keypair will not be stored!\n\
Write it down and store it in a safe place.\n\n\n""",\
                    size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
        else:
            lbl = Label(text="""Something went wrong. Try again later.""",\
                    size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
        lay.add_widget(lbl)
        lbl2 = Label(text=paperwallet,size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.6})
        lay.add_widget(lbl2)        
        btn = Button(text="Copy",size_hint=(0.5,0.1),pos_hint={"x":0.25,"y":0.2},\
                     on_press=lambda x: self.copy_add(paperwallet))
        lay.add_widget(btn)
        self.sendbox = Popup(title="New Paper Wallet",content=lay, size_hint=(0.5,0.5))
        self.sendbox.open()
    
    def show_priv_key(self):
        with open(rpc) as rpcfile: 
            data = rpcfile.read().split("\n")
            rpcuser = data[0][8:]
            rpcpassword = data[1][12:]
            rpchost = 'localhost'
            rpcport = '6804'
            chainname= "testchain"
        api = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
        privkey = api.dumpwallet("C:\\Users\\"+os.getenv('username')+"\\Desktop\\wallet.txt")
        lay = RelativeLayout()
        lbl = Label(text="""
Note: Your wallet file has been dumped!\n
You can view it in C:\\Users\\"""+os.getenv('username')+"""\\Desktop\\wallet.txt\n
Do not share any of your private keys with anyone!\n""",\
                    size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.6})
        lay.add_widget(lbl)
        self.sendbox = Popup(title="New Paper Wallet",content=lay, size_hint=(0.5,0.5))
        self.sendbox.open()

    def copy_add(self, x):
        """
        Copys current address to Clipboard
        """
        Clipboard.copy(x)

