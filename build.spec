# -*- mode: python -*-

block_cipher = None

added_files = [
         ( 'quantisync/ui/assets/icons/*.ico', 'ui/assets/icons' )
         ]

a = Analysis(['quantisync\__main__.py'],
             pathex=['F:\\Projetos\\quantifico\\quantifico-sync\\quantisync'],
             binaries=[],
             datas=added_files,
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
          name='QuantiSync',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
