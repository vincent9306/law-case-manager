# -*- mode: python ; coding: utf-8 -*-
"""
案件管理系统 - Windows 独立 EXE 打包配置（--onefile 模式）
生成单个 case-manager.exe，无需安装 Python，下载即用
"""

import os

block_cipher = None

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
        # Flask 核心
        'flask',
        'flask.json',
        'flask.app',
        'flask.helpers',
        'flask.templating',
        'flask.blueprints',
        'flask.signals',
        'flask.sessions',
        'flask.wrappers',
        'flask.config',
        'flask.globals',
        # Jinja2
        'jinja2',
        'jinja2.ext',
        'jinja2.nodes',
        'jinja2.utils',
        'jinja2.compiler',
        'jinja2.defaults',
        'jinja2.lexer',
        'jinja2.parser',
        'markupsafe',
        'markupsafe._native',
        # Werkzeug
        'werkzeug',
        'werkzeug.middleware',
        'werkzeug.routing',
        'werkzeug.serving',
        'werkzeug.http',
        'werkzeug.urls',
        'werkzeug.datastructures',
        'werkzeug.wrappers',
        # python-docx
        'docx',
        'docx.shared',
        'docx.enum.text',
        'docx.oxml.ns',
        'docx.opc.part',
        'docx.opc.pkgreader',
        'docx.opc.constants',
        # PyPDF2
        'PyPDF2',
        'PyPDF2.generic',
        'PyPDF2._reader',
        'PyPDF2._writer',
        'PyPDF2.constants',
        'PyPDF2.errors',
        # openpyxl
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.utils',
        'openpyxl.worksheet',
        'openpyxl.workbook',
        'openpyxl.cell',
        'openpyxl.reader',
        'openpyxl.writer',
        # 标准库
        'sqlite3',
        'json',
        'uuid',
        're',
        'datetime',
        'io',
        'os',
        'sys',
        'subprocess',
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.base',
        'email.utils',
        'email.encoders',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'IPython',
        'jupyter',
        'notebook',
        'setuptools',
        'pip',
    ],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='case-manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    icon=None,
)
