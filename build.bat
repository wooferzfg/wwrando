set /p key= < keys/build_key.txt

python3 -m PyInstaller wwrando.spec --key=%key%
if %errorlevel% neq 0 exit /b %errorlevel%
python3 build.py
if %errorlevel% neq 0 exit /b %errorlevel%

python3 -m PyInstaller wwrando.spec --key=%key%
if %errorlevel% neq 0 exit /b %errorlevel%
python3 -m build.py
if %errorlevel% neq 0 exit /b %errorlevel%
