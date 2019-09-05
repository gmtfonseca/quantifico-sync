# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'ui/assets/icons/*.ico', 'ui/assets/icons' ),
         ( 'ui/assets/images/*.png', 'ui/assets/images' )
         ]

a = Analysis(['run.py'],
             pathex=['F:\\Projetos\\quantifico\\quantifico-sync'],
             binaries=[],
             datas=added_files,
             hiddenimports=['win32timezone','quantisync.config.auth', 'win32ctypes.core', 'win32ctypes.core._common', 'win32ctypes.core._dll', 'win32ctypes.core._resource', 'win32ctypes.core._authentication'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy'],
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
          name='QuantiSync',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='quantifico.ico',
          console=False )
