import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

options = {
    "build_exe": r"X:\build",
    # 'include-files':
}

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Python Macro Sequencer",
    version="0.0.4",
    description="Image-based macro sequencer providing GUI",
    options={"build_exe": options},
    executables=[Executable(r"Z:\github\python-macro-practice\ui_main.py", base=base)],
)
