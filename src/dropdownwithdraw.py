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
from conf import *

class CustomDropDownWithdraw(DropDown):
    def request_address(self, currency):
        lay = RelativeLayout()
        lbl = Label(text="""
Note: A gateway will be opened and the appearing vaddres \n
can be used ONE TIME to send assets to, which will \n
then appear on the linked address outside the Versum Ecosystem""",\
                    size_hint=(0.75,0.1),pos_hint={"x":0.125,"y":0.8})
        lay.add_widget(lbl)
        btn = Button(text="Open Gateway",size_hint=(0.5,0.1),pos_hint={"x":0.25,"y":0.1},\
                     on_press=lambda x: self.get_address(currency))
        lay.add_widget(btn)
        self.raddress = TextInput(size_hint=(0.6,0.1),pos_hint={"x":0.2,"y":0.3},\
                                 hint_text="Recipient Address")
        lay.add_widget(self.raddress)
        self.vaddress = Label(size_hint=(0.5,0.1),pos_hint={"x":0.25,"y":0.5})
        lay.add_widget(self.vaddress)
        btn2 = Button(text="Copy",size_hint=(0.1,0.1),pos_hint={"x":0.85,"y":0.5},\
                     on_press=lambda x: self.copy_add(self.vaddress.text))
        lay.add_widget(btn2)
        self.sendbox = Popup(title="Withdraw",content=lay, size_hint=(0.5,0.5))
        self.sendbox.open()

    def get_address(self, currency):
        url = gateway_ip+currency+"/get/vaddress"
        data = json.dumps({"raddress":self.raddress.text})
        resp = post(url, data).text
        if resp != "Error" and len(resp) < 50:
            self.vaddress.text = resp
        else:
            self.vaddress.text = "Seems like to Gateway is currently down. Sorry!"

    def copy_add(self, x):
        """
        Copys current address to Clipboard
        """
        Clipboard.copy(x)
