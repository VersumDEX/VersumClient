from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import os.path
import json
from Savoir import Savoir
from requests import post
import platform
import conf


if platform.system() == "Linux":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "/data/"
    rpc = "/home/"+os.getenv('username')+"/.multichain/testchain/multichain.conf"
elif platform.system() == "Windows":
    path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)))) + "\\data\\"
    rpc = "C:\\Users\\"+os.getenv('username')+"\\AppData\\Roaming\\MultiChain\\testchain\\multichain.conf"
    
class Register(Screen):
    def create_wallet(self, password, username):
        """
        Takes a seed and a Password as arguments.
        Creates private Key for each currency and stores it with password in wallet.json file
        """
        with open(rpc, "r+") as rpcfile: 
            data = rpcfile.read().split("\n")
            rpcuser = data[0][8:]
            rpcpassword = data[1][12:]
            rpchost = 'localhost'
            rpcport = '6804'
            chainname= "testchain"
        self.api = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
        
        address = self.api.getnewaddress()
        wallet = {"password": password,
                  "address": address,
                  "username": username
                    }        
        if self.register_address(address) == "Success":
            json.dump(wallet, open(path + "wallet.json", "w+"))
            self.manager.current = 'wallet'
            self.manager.get_screen("wallet").load_data()
    
    def register_address(self, address):
        data = json.dumps({"vaddress":address})
        url = gateway_ip+"/register"
        return post(url, data).text
           
