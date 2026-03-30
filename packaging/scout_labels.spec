# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Scout Advancement Labels."""

import os
import sys

block_cipher = None

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))
ICON = os.path.join(ROOT, "packaging", "icon.icns")

a = Analysis(
    [os.path.join(ROOT, "src", "main.py")],
    pathex=[ROOT],
    binaries=[],
    datas=[],
    hiddenimports=[
        "reportlab.graphics.barcode.common",
        "reportlab.graphics.barcode.code39",
        "reportlab.graphics.barcode.code93",
        "reportlab.graphics.barcode.code128",
        "reportlab.graphics.barcode.usps",
        "reportlab.graphics.barcode.usps4s",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "unittest",
        "pydoc",
        "doctest",
        "PySide6.QtNetwork",
        "PySide6.QtQml",
        "PySide6.QtQuick",
        "PySide6.QtWebEngine",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtMultimedia",
        "PySide6.QtBluetooth",
        "PySide6.QtDBus",
        "PySide6.QtDesigner",
        "PySide6.QtHelp",
        "PySide6.QtOpenGL",
        "PySide6.QtPositioning",
        "PySide6.QtRemoteObjects",
        "PySide6.QtSensors",
        "PySide6.QtSerialPort",
        "PySide6.QtSql",
        "PySide6.QtTest",
        "PySide6.QtXml",
        "PySide6.Qt3DCore",
        "PySide6.Qt3DRender",
        "PySide6.Qt3DInput",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Collect reportlab font/data files
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
reportlab_data = collect_data_files("reportlab")
# Convert 2-tuples (src, dest_dir) to 3-tuples (dest_name, src_name, typecode) for TOC
for src, dest in reportlab_data:
    a.datas.append((os.path.join(dest, os.path.basename(src)), src, "DATA"))
a.hiddenimports += collect_submodules("reportlab")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Scout Advancement Labels",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=ICON,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Scout Advancement Labels",
)

app = BUNDLE(
    coll,
    name="Scout Advancement Labels.app",
    icon=ICON,
    bundle_identifier="com.scoutadvancement.labels",
    info_plist={
        "CFBundleShortVersionString": "0.3.0",
        "CFBundleVersion": "0.3.0",
        "NSHighResolutionCapable": True,
        "CFBundleDocumentTypes": [
            {
                "CFBundleTypeName": "CSV Document",
                "CFBundleTypeExtensions": ["csv"],
                "CFBundleTypeRole": "Viewer",
            }
        ],
    },
)
