"""
Simple Test Script for Medical Chatbot UI
This script tests if all components are working correctly.
"""

import os
import sys

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
    print("\nTesting Python imports...")
    
    try:
        import flask
        print("  OK Flask")
    except ImportError as e:
        print(f"  X Flask: {e}")
        return False
    
    try:
        import requests
        print("  OK Requests")
    except ImportError as e:
        print(f"  X Requests: {e}")
        return False
    
    try:
        import fastapi
        print("  OK FastAPI")
    except ImportError as e:
        print(f"  X FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("  OK Uvicorn")
    except ImportError as e:
        print(f"  X Uvicorn: {e}")
        return False
    
    print("OK All required modules can be imported!")
    return True

def test_fastapi_import():
    """Test if the FastAPI app can be imported"""
    print("\nTesting FastAPI app import...")
    
    try:
        sys.path.insert(0, os.getcwd())
        import main
        print("  OK main.py imported successfully")
        
        if hasattr(main, 'app'):
            print("  OK FastAPI app found")
        else:
            print("  X FastAPI app not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"  X Error importing main.py: {e}")
        return False

def test_flask_import():
    """Test if the Flask app can be imported"""
    print("\nTesting Flask app import...")
    
    try:
        import ui_server
        print("  OK ui_server.py imported successfully")
        
        if hasattr(ui_server, 'app'):
            print("  OK Flask app found")
        else:
            print("  X Flask app not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"  X Error importing ui_server.py: {e}")
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
        test_flask_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"X Test failed with error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"OK Passed: {passed}/{total}")
    print(f"X Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\nALL TESTS PASSED!")
        print("Your Medical Chatbot UI is ready to use!")
        print("\nTo start the servers:")
        print("  python start_ui.py")
        print("\nThen visit: http://localhost:5000")
    else:
        print(f"\n{total - passed} test(s) failed.")
        print("Please fix the issues above before running the UI.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
