pyinstaller --add-data "d:\desktop\�ƴ�����ϵͳ\WebFiles;\WebFiles" --add-data "d:\desktop\�ƴ�����ϵͳ\WebFiles\CSS;\WebFiles\CSS" --add-data "d:\desktop\�ƴ�����ϵͳ\WebFiles\JS;\WebFiles\JS" -F d:\desktop\�ƴ�����ϵͳ\main.py
@REM del /f .\build
rmdir /s /q build
copy .\dist\main.exe .\main.exe
@REM del /f .\dist
rmdir /s /q dist
del /f /q .\*.spec