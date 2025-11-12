@echo off
echo ====================================
echo  Shatarupa's Artree - Gallery Updater
echo ====================================
echo.

echo [INFO] Checking for Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Checking for required Python modules...
python -c "import os, re, hashlib" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Required Python modules are missing
    echo Installing required modules...
    pip install os re hashlib
)

echo.
echo [INFO] Starting gallery update process...
python update_gallery.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Gallery updated successfully!
    echo Your new artworks are now live on your website.
) else (
    echo.
    echo [ERROR] Failed to update gallery. Please check for any error messages above.
)

echo.
echo ====================================
echo  Update Instructions for Future Use
echo ====================================
echo 1. Add new images to: C:\Shatarupa\Art\Paintings\
echo 2. Add new videos to: C:\Shatarupa\Art\Short Painting Videos\
echo 3. Run this batch file to update your website
echo.
pause
