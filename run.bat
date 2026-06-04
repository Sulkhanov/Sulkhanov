@echo off
title Bank Customer Service System
echo ================================================
echo   Bank Customer Service System
echo   TSI Software Engineering Course Project
echo   Farrukh Sulkhanov - ST79251 - Group 4302BDA
echo ================================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    echo Make sure to tick "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo Starting application...
echo Login with:  username = admin   password = admin123
echo.
python main.py
pause
