from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, \
     ReferenceListProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.uix.dropdown import DropDown

from Savoir import Savoir
import random
import os.path
import json
from datetime import datetime
from requests import post
import time
import platform

from conf import *
from dropdownwithdraw import CustomDropDownWithdraw
from dropdowndeposit import CustomDropDownDeposit
from dropdownmenu import CustomDropDownMenu


if platform.system() == "Linux":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "/data/"
    rpc = "/home/"+os.getenv('username')+"/.multichain/"+chainname+"/multichain.conf"
elif platform.system() == "Windows":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "\\data\\"
    rpc = "C:\\Users\\"+os.getenv('username')+"\\AppData\\Roaming\\MultiChain\\"+chainname+"\\multichain.conf"

class Wallet(Screen):
    def load_data(self):
        """
        Loads wallet for given currency
        """
        self.dropdownw = CustomDropDownWithdraw()
        self.dropdownd = CustomDropDownDeposit()
        self.dropdownm = CustomDropDownMenu()
        with open(rpc, "r") as rpcfile: 
            data = rpcfile.read().split("\n")
            rpcuser = data[0][8:]
            rpcpassword = data[1][12:]
            rpchost = 'localhost'
            rpcport = '6804'
            chainname= "testchain"
        self.api = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
        self.load_balances()
        self.load_tx_history()
        Clock.schedule_interval(lambda dt: self.load_balances(), 5)
        Clock.schedule_interval(lambda dt: self.load_tx_history(), 5)

    def load_tx_history(self):
        data = self.api.listwallettransactions(50)
        self.history.clear_widgets()
        for tx in data[::-1]:
            for asset in tx["balance"]["assets"]:
                lay = RelativeLayout()
                self.history.add_widget(self.create_histo_layout(asset["qty"],\
                asset["name"], tx["confirmations"], datetime.fromtimestamp(tx["timereceived"])))

    def create_histo_layout(self, qty, name, confirmations, time):
        Layout = RelativeLayout(bcolor=(1,0.2,1,1))
        if qty > 0:
            text="Incoming                                                                    " + str(qty) + " " + str(name) + "\n" 
            Layout.add_widget(Image(source="gui/versumwallet/histo_green.png", size_hint=(1,0.9), allow_stretch=True, keep_ratio=False))
            
        elif qty < 0:
            text="Outgoing                                                                    " + str(qty) + " " + str(name) + "\n" 
            Layout.add_widget(Image(source="gui/versumwallet/histo_red.png", size_hint=(1,0.9), allow_stretch=True, keep_ratio=False))
                              
        text += str(time) + "\n" 
        text += "Confirmations: " + str(confirmations)
                   
        title = Label(text = text, color=(0,0,0,1), halign="left") 
        Layout.add_widget(title)                    
        return Layout
        
    def load_balances(self):
        balance = self.api.gettotalbalances()
        for asset in balance:
            if asset["name"] == "BTC":
                self.vbtc_balance.text = str(asset["qty"])
            if asset["name"] == "LTC":
                self.vltc_balance.text = str(asset["qty"])
            if asset["name"] == "ETH":
                self.veth_balance.text = str(asset["qty"])
       
    def vsend(self):
        """
        Open the withdraw screen for actual currency
        """
        assets={}
        if not self.veth_amount.text and not self.vbtc_amount.text and not self.vltc_amount.text:
            self.notification("Enter an amount to send.")
            return
        if self.vbtc_amount.text:
            assets["BTC"] = float(self.vbtc_amount.text)
            self.vbtc_amount.text = ""
        if self.vltc_amount.text:
            assets["LTC"] = float(self.vltc_amount.text)
            self.vltc_amount.text = ""
        if self.veth_amount.text:
            assets["ETH"] = float(self.veth_amount.text)
            self.veth_amount.text = ""
        lay = RelativeLayout()
        lbl = Label(text="""
Note: Only send assets to addresses inside the Versum Ecosystem,\n
if you need to send funds outside of Versum, open a Gateway at first.""",\
                    size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
        lay.add_widget(lbl)
        btn = Button(text="Send",size_hint=(0.5,0.1),pos_hint={"x":0.25,"y":0.1},\
                     on_press=lambda *args: self.make_payment(assets,*args))
        lay.add_widget(btn)
        self.to_addr = TextInput(size_hint=(0.6,0.1),pos_hint={"x":0.2,"y":0.3},\
                                 hint_text="Recipient Address")
        lay.add_widget(self.to_addr)
        
        self.sendbox = Popup(title="vSend",content=lay, size_hint=(0.5,0.5))
        self.sendbox.open()

    def make_payment(self, assets, *args):
        x = self.api.send(self.to_addr.text, assets)
        self.sendbox.dismiss()
        try:
            text = x["error"]["message"]
            Clock.schedule_once(lambda dt:self.notification(text), 2)
        except:
            Clock.schedule_once(lambda dt:self.notification("Payment Successful."), 2)
        Clock.schedule_once(lambda dt: self.load_balances(), 1.5)

    def copy_add(self, x):
        """
        Copys current address to Clipboard
        """
        Clipboard.copy(x[12:])

    def receive(self):
        with open(path + "wallet.json", "r") as wallet_file:
            address = json.load(wallet_file)["address"]
            Clipboard.copy(address)
        self.notification("Your address was copied to the clipboard.")

    def notification(self, content):
        lay = RelativeLayout()
        lbl = Label(text=content)
        lay.add_widget(lbl)
        x = Popup(title="Notification",content=lay, size_hint=(0.25,0.15), pos_hint={"x":0.7,"y":0.85})
        x.open()
        Clock.schedule_once(lambda dt: self.dismiss_popup(x), 1.5)
        
    def dismiss_popup(self,popup):
        popup.dismiss()





