cd %~dp0
cd ..
for %%f in (./Qt_UI/*.ui) do pyuic5 ./Qt_UI/%%f -o ./Qt_UI/%%~nf.py
