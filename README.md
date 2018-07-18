**Versum Client - Desktop**

We're currently testing our Gateways / Client on an internal testnet basis. To see how it works we've prepared a small presentation for you:
https://www.youtube.com/watch?v=mnBDMfXUf5s



Versum is an open-source Project to build a decentralized, blockchain based payment/trading system & value storage. Starting with the most common cryptos, we're working hard to add more and more asset classes to our system (fiat money, stocks, real estate, licenses, etc. - there are no limitations at all)

This repository contains the full code to build the Versum Desktop Client. To see have a look at our gateway prototype, go here: https://github.com/VersumDEX/VerumGateways

/src contains all code 

Compilable with PyInstaller for linux/mac/windows - currently only tested on Windows & Ubuntu. 


**How to compile**

1. At first you'll need to set up a Python 2.7 enviroment on your PC - https://www.python.org/downloads/

2. Install Kivy on you PC. Kivy is a cross platform framework for building applications in python - https://kivy.org/docs/installation/installation.html

3. Install dependencies. Type in your terminal/cmd:
```
pip install savoir
pip install pyinstaller

```

4. Clone this Repo:
```
git clone https://github.com/VersumDEX/VersumClient.git
```

5. Now you need to get the Blockchain Node. You can either build it yourself or just download a precompiled version. All build instractions are in /src/node. A precompiled version is available in the links in /src/node/README.md

6. Place the multichaind binaries in /src/node/win/ or /src/node/linux/ depending on your operating system.

7. Now you should be able to run the main.py and start the Client. If it runs without errors you can now create a compiled version. Therefore confirgure /VersumClient-Compiling/versumclient.spec 

8. In the folder /VersumClient-Compiling/versumclient.spec open a terminal/cmd and type:
```
PyInstaller versumclient.spec 
```







