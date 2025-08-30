#!/usr/bin/env python3
"""
Test script to verify Cluely AI Assistant installation
"""

import sys
import os
import importlib
from typing import List, Tuple

def test_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        return True, f"✅ {package_name or module_name}"
    except ImportError as e:
        return False, f"❌ {package_name or module_name}: {e}"

def test_environment() -> List[Tuple[bool, str]]:
    """Test environment setup"""
    results = []
    
    print("🔍 Testing environment setup...")
    
    # Test Python version
    if sys.version_info >= (3, 9):
        results.append((True, f"✅ Python {sys.version_info.major}.{sys.version_info.minor}"))
    else:
        results.append((False, f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (3.9+ required)"))
    
    # Test Gemini API key
    if os.getenv('GEMINI_API_KEY'):
        results.append((True, "✅ Gemini API key found"))
    else:
        results.append((False, "❌ Gemini API key not set"))
    
    return results

def test_dependencies() -> List[Tuple[bool, str]]:
    """Test required dependencies"""
    results = []
    
    print("📦 Testing dependencies...")
    
    # Core dependencies
    dependencies = [
        ("google.genai", "Google GenAI"),
        ("PyQt5", "PyQt5"),
        ("whisper", "OpenAI Whisper"),
        ("sounddevice", "SoundDevice"),
        ("keyboard", "Keyboard"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
    ]
    
    for module, name in dependencies:
        success, message = test_import(module, name)
        results.append((success, message))
    
    # Optional dependencies
    optional_deps = [
        ("pytesseract", "Tesseract OCR"),
        ("screen_ocr", "Screen OCR"),
    ]
    
    print("🔧 Testing optional dependencies...")
    for module, name in optional_deps:
        success, message = test_import(module, name)
        if success:
            results.append((True, f"✅ {name} (optional)"))
        else:
            results.append((False, f"⚠️  {name} (optional): not found"))
    
    return results

def test_components() -> List[Tuple[bool, str]]:
    """Test local components"""
    results = []
    
    print("🧩 Testing local components...")
    
    # Test local modules
    local_modules = [
        ("config", "Configuration"),
        ("screen_capture", "Screen Capture"),
        ("audio_capture", "Audio Capture"),
        ("gemini_client", "Gemini Client"),
        ("overlay_ui", "Overlay UI"),
        ("hotkey_manager", "Hotkey Manager"),
        ("cluely_assistant", "Main Assistant"),
    ]
    
    for module, name in local_modules:
        success, message = test_import(module, name)
        results.append((success, message))
    
    return results

def test_ocr_capability() -> List[Tuple[bool, str]]:
    """Test OCR capabilities"""
    results = []
    
    print("👁️  Testing OCR capabilities...")
    
    # Test Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        results.append((True, "✅ Tesseract OCR available"))
    except Exception:
        results.append((False, "❌ Tesseract OCR not available"))
    
    # Test screen-ocr
    try:
        from screen_ocr import Reader
        results.append((True, "✅ Screen OCR available"))
    except Exception:
        results.append((False, "❌ Screen OCR not available"))
    
    return results

def test_audio_capability() -> List[Tuple[bool, str]]:
    """Test audio capabilities"""
    results = []
    
    print("🎤 Testing audio capabilities...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_inputs'] > 0]
        if input_devices:
            results.append((True, f"✅ Audio input devices found ({len(input_devices)} devices)"))
        else:
            results.append((False, "❌ No audio input devices found"))
    except Exception as e:
        results.append((False, f"❌ Audio system error: {e}"))
    
    return results

def main():
    """Run all tests"""
    print("🧪 Cluely AI Assistant - Installation Test")
    print("=" * 50)
    
    all_results = []
    
    # Run all test suites
    test_suites = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Components", test_components),
        ("OCR Capability", test_ocr_capability),
        ("Audio Capability", test_audio_capability),
    ]
    
    for suite_name, test_func in test_suites:
        print(f"\n{suite_name}:")
        print("-" * 20)
        results = test_func()
        all_results.extend(results)
        for success, message in results:
            print(f"  {message}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    total_tests = len(all_results)
    passed_tests = sum(1 for success, _ in all_results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"  Total tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    
    if failed_tests == 0:
        print("\n🎉 All tests passed! The assistant should work correctly.")
        print("\nTo start the assistant:")
        print("  python cluely_assistant.py")
    else:
        print(f"\n⚠️  {failed_tests} test(s) failed. Please check the issues above.")
        print("\nCommon fixes:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Set GEMINI_API_KEY environment variable")
        print("  3. Install Tesseract OCR for better text recognition")
        print("  4. Check audio device permissions")

if __name__ == "__main__":
    main()
