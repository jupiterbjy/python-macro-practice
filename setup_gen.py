from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": [], "excludes": []}


base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("MainUI.py", base=base, targetName="pym")]

setup(
    name="test",
    version="0.0.4",
    description="cx-freeze",
    options={"build_exe": build_options},
    executables=executables,
)
