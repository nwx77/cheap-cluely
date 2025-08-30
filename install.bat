@echo off
echo 🚀 Cluely AI Assistant - Windows Installer
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Run setup script
echo 🔧 Running setup checks...
python setup.py
if errorlevel 1 (
    echo ❌ Setup failed
    pause
    exit /b 1
)

echo.
echo 🎉 Installation complete!
echo.
echo To start the assistant:
echo   python cluely_assistant.py
echo.
echo To test the installation:
echo   python test_installation.py
echo.
pause
