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

import json
from requests import post
import os
from conf import *

path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "/data/" #to compile for

class CustomDropDownDeposit(DropDown):
    def request_address(self, currency):
        url = gateways_ip+currency+"/get/raddress"
        data = json.dumps({"vaddress":json.load(open(path + "wallet.json", "r"))["address"]})
        resp = post(url, data).text
        if resp != "Error" and len(resp) < 50:  #server is up 
            lay = RelativeLayout()
            lbl = Label(text="""
Note: Use the displayed address ONLY ONCE to depsit funds.\n
Do not deposit currencys other than """ + currency,\
            size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
            lay.add_widget(lbl)
            self.raddress = Label(text=resp,size_hint=(0.5,0.1),pos_hint={"x":0.25,"y":0.5})
            lay.add_widget(self.raddress)
            btn = Button(text="Copy",size_hint=(0.1,0.1),pos_hint={"x":0.8,"y":0.5},\
                     on_press=lambda x: self.copy_add(self.raddress.text))
            lay.add_widget(btn)
            self.sendbox = Popup(title="Deposit",content=lay, size_hint=(0.5,0.5))
            self.sendbox.open()
        else:                                   #server is down
            lay = RelativeLayout()
            lbl = Label(text="Seems like the Gateway is currently down. Sorry!",\
            size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
            lay.add_widget(lbl)
            self.sendbox = Popup(title="Deposit",content=lay, size_hint=(0.5,0.5))
            self.sendbox.open()
            
            
    def copy_add(self, x):
        """
        Copys current address to Clipboard
        """
        Clipboard.copy(x)

