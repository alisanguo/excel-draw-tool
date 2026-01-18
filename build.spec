# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('sample_defect_data.xlsx', '.'),
        ('启动.bat', '.'),
        ('调试模式启动.bat', '.'),
    ],
    hiddenimports=[
        'openpyxl',
        'pandas',
        'flask',
        'werkzeug',
        'jinja2',
        'click',
        'itsdangerous',
        'markupsafe',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 排除不必要的模块以减小体积
    excludes=[
        'matplotlib',
        'scipy',
        'numpy.distutils',
        'tkinter',
        'test',
        'tests',
        'unittest',
        'setuptools',
        'distutils',
        'pkg_resources',
        'lib2to3',
        'pydoc',
        'email',
        'xml',
        'html',
        'http.client',
        'urllib',
        'xmlrpc',
        'sqlite3',
        'curses',
        'multiprocessing',
        'concurrent',
        'asyncio',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'PIL',
        'PIL.Image',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='excel-draw-tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 启用strip减小体积
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
    a.zipfiles,
    a.datas,
    strip=True,  # 启用strip减小体积
    upx=True,
    upx_exclude=[
        # UPX压缩可能导致某些DLL问题，排除关键文件
        'vcruntime*.dll',
        'python*.dll',
    ],
    name='excel-draw-tool',
)

