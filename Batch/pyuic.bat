rem @echo off
rem cd %~dp0
cd ..\qtUI
for %%f in (./*.ui) do pyuic5 ./%%f -o ./%%~nf.py
