@echo off
cd ../testingEnv/UML

goto Select

:Select
echo 1. Generate Project UML
echo 2. Generate Toolset UML
echo -----------------------
set /P option=">> ":

IF %option% == 1 goto Project
IF %option% == 2 goto Toolset
goto Select

:Project
IF EXIST classes_PMP.png (
    del classes_PMP.png
    del packages_PMP.png 2>nul
)
pyreverse -o png -p PMP ../../
goto EXIT

:Toolset
IF EXIST classes_TSet.png (
    del classes_TSet.png
    del packages_TSet.png 2>nul
)
pyreverse -o png -p TSet ../../ToolSet/
goto EXIT

:EXIT
PAUSE