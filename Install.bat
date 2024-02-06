@ECHO OFF

echo [+] Installing dependencies...
python -m venv venv
.\venv\Scripts\activate.bat && pip install -r requirements.txt

echo [#] Installation complete.
echo [#] Double click on "Run.bat" to start the script

pause .