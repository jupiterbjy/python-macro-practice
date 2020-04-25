from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": [], "excludes": []}


base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("MainUIController.py", base=base, targetName="pym")]

setup(
    name="Python Image Macro Project",
    version="0.0.5",
    description="cx-freeze",
    options={"build_exe": build_options},
    executables=executables,
)
