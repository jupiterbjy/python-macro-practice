from cx_Freeze import setup, Executable
import sys

version = "0.0.6"

build_options = {"packages": [], "excludes": [], "build_exe": "X:\\builds\\",
                 "include_files": ['Sequence_Sample/', 'icons/']}


base = "Win32GUI" if sys.platform == "win32" else None
# base = None

executables = [Executable("MainUIController.py", base=base, targetName="pym")]

setup(
    name="Python Image Macro Project",
    version=version,
    description="Image Based macro project.",
    options={"build_exe": build_options},
    executables=executables,
)
