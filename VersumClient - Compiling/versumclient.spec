# -*- mode: python -*-

block_cipher = None
from kivy.deps import sdl2, glew


a = Analysis(['PATH TO MAIN.PY'],	#path to main.py file
             pathex=['DESTINATION PATH'],	#current path (where to build the .exe)
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='versumclient',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='PATH TO ICON')	#path to icon

coll = COLLECT(exe, Tree('PATH TO /SRC FOLDER'),	#path to src folder
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='VersumClient-alpha')
