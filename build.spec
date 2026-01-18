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
        ('start.bat', '.'),                    # 英文启动脚本（推荐）
        ('start_debug.bat', '.'),              # 英文调试脚本（推荐）
        ('启动.bat', '.'),                      # 中文启动脚本（备用）
        ('调试模式启动.bat', '.'),              # 中文调试脚本（备用）
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
        'urllib3',
        'charset_normalizer',
        'certifi',
        'idna',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 排除不必要的模块以减小体积（保守策略，只排除明确不需要的）
    excludes=[
        'matplotlib',
        'scipy',
        'tkinter',
        'test',
        'tests',
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
    strip=False,  # 禁用strip，避免破坏DLL
    upx=False,    # 禁用UPX，避免加载问题
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
    strip=False,  # 禁用strip，确保DLL完整性
    upx=False,    # 禁用UPX，确保兼容性
    name='excel-draw-tool',
)

