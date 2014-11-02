# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.datas += [('img/icon.gif', 'img/icon.gif', 'DATA')]
a.datas += [('img/0.gif', 'img/0.gif', 'DATA')]
a.datas += [('img/16.gif', 'img/16.gif', 'DATA')]
a.datas += [('img/32.gif', 'img/32.gif', 'DATA')]
a.datas += [('img/48.gif', 'img/48.gif', 'DATA')]
a.datas += [('img/64.gif', 'img/64.gif', 'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OOT Heart Piece Display.exe',
          icon = 'icon.ico',
          debug=False,
          strip=None,
          upx=True,
          console=False )
