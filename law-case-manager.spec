# -*- mode: python ; coding: utf-8 -*-
"""个人案件管理系统 PyInstaller 打包配置"""

import os
import sys

block_cipher = None

# 项目根目录
ROOT = os.path.dirname(os.path.abspath(SPECPATH))

a = Analysis(
    ['app.py'],
    pathex=[ROOT],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ],
    hiddenimports=[
        'flask',
        'jinja2',
        'jinja2.ext',
        'werkzeug',
        'docx',
        'docx.shared',
        'docx.enum.text',
        'docx.oxml.ns',
        'PyPDF2',
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.utils',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='案件管理系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='案件管理系统',
)
