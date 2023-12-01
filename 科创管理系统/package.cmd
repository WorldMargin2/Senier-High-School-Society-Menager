pyinstaller --add-data "d:\desktop\科创管理系统\WebFiles;\WebFiles" --add-data "d:\desktop\科创管理系统\WebFiles\CSS;\WebFiles\CSS" --add-data "d:\desktop\科创管理系统\WebFiles\JS;\WebFiles\JS" -F d:\desktop\科创管理系统\main.py
@REM del /f .\build
rmdir /s /q build
copy .\dist\main.exe .\main.exe
@REM del /f .\dist
rmdir /s /q dist
del /f /q .\*.spec