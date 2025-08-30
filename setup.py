#!/usr/bin/env python3
"""
Setup script for Cluely-like AI Desktop Assistant
"""

import os
import sys
import subprocess
from setuptools import setup, find_packages

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR found")
        return True
    except Exception:
        print("⚠️  Tesseract OCR not found")
        print("   You can install it from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Or the app will use screen-ocr as fallback")
        return False

def check_gemini_key():
    """Check if Gemini API key is set"""
    if os.getenv('GEMINI_API_KEY'):
        print("✅ Gemini API key found")
        return True
    else:
        print("⚠️  Gemini API key not set")
        print("   Please set GEMINI_API_KEY environment variable")
        print("   Get a free key from: https://makersuite.google.com/app/apikey")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Cluely-like AI Desktop Assistant")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    print("✅ Python version compatible")
    
    # Install dependencies
    install_dependencies()
    
    # Check optional dependencies
    check_tesseract()
    check_gemini_key()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nTo start the assistant:")
    print("  python cluely_assistant.py")
    print("\nFor help:")
    print("  python cluely_assistant.py --help")

if __name__ == "__main__":
    main()
