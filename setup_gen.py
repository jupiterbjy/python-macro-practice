from cx_Freeze import setup, Executable
from datetime import datetime
import sys

version = '0.0.5'
date = datetime.now().strftime('%Y-%m-%d')


# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": [], "excludes": []}


# base = "Win32GUI" if sys.platform == "win32" else None
base = None

executables = [Executable("MainUIController.py", base=base, targetName="pym")]

setup(
    name="Python Image Macro Project",
    version=version,
    description="cx-freeze",
    options={"build_exe": build_options},
    executables=executables,
)
