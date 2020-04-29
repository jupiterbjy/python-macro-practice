rem @echo off
rem cd %~dp0
cd ..\qtUI
for %%f in (./*.ui) do pyside2-uic ./%%f -o ./%%~nf.py
