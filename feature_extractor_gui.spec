# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

a = Analysis(
    ['feature_extractor_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='feature_extractor_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='feature_extractor_gui',
    icon=str(current_dir / 'icon.ico') if (current_dir / 'icon.ico').exists() else None
)

colle = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='feature_extractor_gui'
)