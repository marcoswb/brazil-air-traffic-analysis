@echo off
setlocal enabledelayedexpansion

REM .\.venv\Scripts\activate

for %%f in ("./screen_ui/*.ui") do (
    echo Convertendo: %%~nxf
    pyside6-uic "./screen_ui/%%f" > "./src/ui/%%~nf.py"
)

echo.
echo Conversao concluida!
pause
