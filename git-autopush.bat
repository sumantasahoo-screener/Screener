@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist ".git" (
    echo ERROR: .git folder nahi mila. Screener folder mein rakhkar chalao.
    pause
    exit /b
)

echo Git Auto Push chal raha hai...
echo Band karne ke liye Ctrl+C dabao.
echo.

:LOOP
git status --short > "%TEMP%\gitcheck.txt" 2>nul

set SIZE=0
for %%A in ("%TEMP%\gitcheck.txt") do set SIZE=%%~zA

if !SIZE! GTR 0 (
    echo [%TIME%] Change mila - commit aur push ho raha hai...
    git add -A
    git commit -m "auto update %DATE% %TIME%"
    git push
    echo [%TIME%] Done.
    echo.
)

timeout /t 5 /nobreak >nul
goto LOOP
