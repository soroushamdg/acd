# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Soroush\\PycharmProjects\\ac_downloader'],
             binaries=[('_acd_logo_1.png', 'DATA'), ('_acd_logo_icon.png', 'DATA'), ('acd_logo_Mzn_icon.ico', 'DATA'), ('bug.png', 'DATA'), ('github.png', 'DATA'), ('it.png', 'DATA'), ('ok.png', 'DATA')],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='acd',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='acd_logo_Mzn_icon.ico')
