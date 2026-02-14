# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import sys
from pathlib import Path

block_cipher = None

# Collect all Streamlit data files
streamlit_datas = collect_data_files('streamlit', include_py_files=True)

# Collect project resources (configs and prompts)
project_root = Path('.').resolve()
datas = [
    (str(project_root / 'configs'), 'configs'),
    (str(project_root / 'prompts'), 'prompts'),
]
datas.extend(streamlit_datas)

# Hidden imports for Streamlit and dependencies
hiddenimports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'openai',
    'tqdm',
    'python-dotenv',
    'dotenv',
    'altair',
    'plotly',
    'pandas',
    'numpy',
    'pyarrow',
    'pydeck',
    'tornado',
    'validators',
    'watchdog',
    'click',
]
hiddenimports.extend(collect_submodules('streamlit'))

a = Analysis(
    ['../src/llm_folder_organizer/standalone_entry.py'],
    pathex=[str(project_root / 'src')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'PIL', 'IPython'],
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
    name='lfo-webui',
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
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lfo-webui',
)
