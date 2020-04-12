# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui_main.py'],
             pathex=['Z:\\github\\python-macro-practice\\venv\\Lib\\site-packages', 'Z:\\github\\python-macro-practice'],
             binaries=[],
             datas=[('./icons/*', 'icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PythonMacro_win_x86.exe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PythonMacro_win_x86.exe')
