"""
Test Script for Medical Chatbot UI
This script tests if all components are working correctly.
"""

import os
import sys
import requests
import time
from pathlib import Path

def test_file_structure():
    """Test if all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'templates/index.html',
        'static/css/style.css', 
        'static/js/script.js',
        'ui_server.py',
        'main.py',
        'agent.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"  X {file_path}")
        else:
            print(f"  OK {file_path}")
    
    if missing_files:
        print(f"\nX Missing files: {missing_files}")
        return False
    
    print("OK All required files exist!")
    return True

def test_imports():
    """Test if all required Python modules can be imported"""
    print("\n🔍 Testing Python imports...")
    
    try:
        import flask
        print("  ✅ Flask")
    except ImportError as e:
        print(f"  ❌ Flask: {e}")
        return False
    
    try:
        import requests
        print("  ✅ Requests")
    except ImportError as e:
        print(f"  ❌ Requests: {e}")
        return False
    
    try:
        import fastapi
        print("  ✅ FastAPI")
    except ImportError as e:
        print(f"  ❌ FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("  ✅ Uvicorn")
    except ImportError as e:
        print(f"  ❌ Uvicorn: {e}")
        return False
    
    print("✅ All required modules can be imported!")
    return True

def test_fastapi_import():
    """Test if the FastAPI app can be imported"""
    print("\n🔍 Testing FastAPI app import...")
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the main module
        import main
        print("  ✅ main.py imported successfully")
        
        # Check if the app exists
        if hasattr(main, 'app'):
            print("  ✅ FastAPI app found")
        else:
            print("  ❌ FastAPI app not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing main.py: {e}")
        return False

def test_flask_import():
    """Test if the Flask app can be imported"""
    print("\n🔍 Testing Flask app import...")
    
    try:
        # Try to import the UI server
        import ui_server
        print("  ✅ ui_server.py imported successfully")
        
        # Check if the app exists
        if hasattr(ui_server, 'app'):
            print("  ✅ Flask app found")
        else:
            print("  ❌ Flask app not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing ui_server.py: {e}")
        return False

def test_html_content():
    """Test if HTML template has required content"""
    print("\n🔍 Testing HTML template...")
    
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        required_elements = [
            'chatMessages',
            'messageInput',
            'sendButton',
            'quick-btn',
            'Medical Assistant'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in html_content:
                missing_elements.append(element)
                print(f"  ❌ Missing: {element}")
            else:
                print(f"  ✅ Found: {element}")
        
        if missing_elements:
            print(f"\n❌ Missing HTML elements: {missing_elements}")
            return False
        
        print("✅ HTML template looks good!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading HTML template: {e}")
        return False

def test_css_content():
    """Test if CSS file has required styles"""
    print("\n🔍 Testing CSS file...")
    
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        required_styles = [
            '.chat-messages',
            '.message',
            '.quick-btn',
            '.input-wrapper',
            'body'
        ]
        
        missing_styles = []
        for style in required_styles:
            if style not in css_content:
                missing_styles.append(style)
                print(f"  ❌ Missing: {style}")
            else:
                print(f"  ✅ Found: {style}")
        
        if missing_styles:
            print(f"\n❌ Missing CSS styles: {missing_styles}")
            return False
        
        print("✅ CSS file looks good!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading CSS file: {e}")
        return False

def test_javascript_content():
    """Test if JavaScript file has required functions"""
    print("\n🔍 Testing JavaScript file...")
    
    try:
        with open('static/js/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        required_functions = [
            'sendMessage',
            'addMessageToChat',
            'setupEventListeners',
            'showTypingIndicator'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in js_content:
                missing_functions.append(func)
                print(f"  ❌ Missing: {func}")
            else:
                print(f"  ✅ Found: {func}")
        
        if missing_functions:
            print(f"\n❌ Missing JavaScript functions: {missing_functions}")
            return False
        
        print("✅ JavaScript file looks good!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading JavaScript file: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("MEDICAL CHATBOT UI - INTEGRATION TEST")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_imports,
        test_fastapi_import,
        test_flask_import,
        test_html_content,
        test_css_content,
        test_javascript_content
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your Medical Chatbot UI is ready to use!")
        print("\n🚀 To start the servers:")
        print("   python start_ui.py")
        print("\n🌐 Then visit: http://localhost:5000")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please fix the issues above before running the UI.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
