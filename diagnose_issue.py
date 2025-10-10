"""
Diagnostic Script for Medical Chatbot Issues
This script helps identify why the chatbot is not responding.
"""

import requests
import subprocess
import sys
import time
import os

def check_port(port):
    """Check if a port is listening"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def test_fastapi_health():
    """Test if FastAPI backend is responding"""
    print("Testing FastAPI backend health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  OK FastAPI is healthy: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"  X FastAPI returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  X Cannot connect to FastAPI backend (port 8000)")
        return False
    except requests.exceptions.Timeout:
        print("  X FastAPI request timed out")
        return False
    except Exception as e:
        print(f"  X Error testing FastAPI: {e}")
        return False

def test_fastapi_chat():
    """Test if FastAPI chat endpoint is working"""
    print("Testing FastAPI chat endpoint...")
    try:
        test_message = {
            "message": "Hello, this is a test message",
            "thread_id": "test_thread"
        }
        
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  OK Chat endpoint working. Response: {data.get('response', 'No response')[:50]}...")
            return True
        else:
            print(f"  X Chat endpoint returned status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  X Error details: {error_data}")
            except:
                print(f"  X Error response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  X Cannot connect to FastAPI chat endpoint")
        return False
    except requests.exceptions.Timeout:
        print("  X Chat request timed out")
        return False
    except Exception as e:
        print(f"  X Error testing chat: {e}")
        return False

def test_flask_ui():
    """Test if Flask UI server is responding"""
    print("Testing Flask UI server...")
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("  OK Flask UI server is responding")
            return True
        else:
            print(f"  X Flask UI returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  X Cannot connect to Flask UI server (port 5000)")
        return False
    except Exception as e:
        print(f"  X Error testing Flask UI: {e}")
        return False

def test_flask_api():
    """Test if Flask API proxy is working"""
    print("Testing Flask API proxy...")
    try:
        test_message = {
            "message": "Hello, this is a test message",
            "thread_id": "test_thread"
        }
        
        response = requests.post(
            "http://localhost:5000/api/chat",
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  OK Flask API proxy working. Response: {data.get('response', 'No response')[:50]}...")
            return True
        else:
            print(f"  X Flask API proxy returned status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  X Error details: {error_data}")
            except:
                print(f"  X Error response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  X Cannot connect to Flask API proxy")
        return False
    except Exception as e:
        print(f"  X Error testing Flask API: {e}")
        return False

def check_processes():
    """Check if the required processes are running"""
    print("Checking running processes...")
    
    try:
        # Check for Python processes
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        
        if 'python.exe' in result.stdout:
            print("  OK Python processes are running")
            lines = result.stdout.split('\n')
            python_count = sum(1 for line in lines if 'python.exe' in line)
            print(f"  Found {python_count} Python process(es)")
        else:
            print("  X No Python processes found")
            
    except Exception as e:
        print(f"  X Error checking processes: {e}")

def main():
    """Run all diagnostic tests"""
    print("=" * 60)
    print("MEDICAL CHATBOT DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Check ports
    print("Checking ports...")
    port_8000 = check_port(8000)
    port_5000 = check_port(5000)
    
    print(f"  Port 8000 (FastAPI): {'OK' if port_8000 else 'X'}")
    print(f"  Port 5000 (Flask): {'OK' if port_5000 else 'X'}")
    
    print("\n" + "-" * 40)
    
    # Check processes
    check_processes()
    
    print("\n" + "-" * 40)
    
    # Test FastAPI
    fastapi_health = test_fastapi_health()
    fastapi_chat = test_fastapi_chat() if fastapi_health else False
    
    print("\n" + "-" * 40)
    
    # Test Flask
    flask_ui = test_flask_ui()
    flask_api = test_flask_api() if flask_ui else False
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC RESULTS")
    print("=" * 60)
    
    if not port_8000:
        print("ISSUE: FastAPI backend is not running on port 8000")
        print("SOLUTION: Start the FastAPI server with: python main.py")
        
    elif not fastapi_health:
        print("ISSUE: FastAPI backend is running but not healthy")
        print("SOLUTION: Check the FastAPI server logs for errors")
        
    elif not fastapi_chat:
        print("ISSUE: FastAPI chat endpoint is not working")
        print("SOLUTION: Check if the agent is properly initialized")
        
    elif not port_5000:
        print("ISSUE: Flask UI server is not running on port 5000")
        print("SOLUTION: Start the Flask server with: python ui_server.py")
        
    elif not flask_ui:
        print("ISSUE: Flask UI server is running but not responding")
        print("SOLUTION: Check the Flask server logs for errors")
        
    elif not flask_api:
        print("ISSUE: Flask API proxy is not working")
        print("SOLUTION: Check the connection between Flask and FastAPI")
        
    else:
        print("ALL SYSTEMS WORKING!")
        print("The chatbot should be responding normally.")
    
    print("\n" + "=" * 60)
    print("QUICK FIX COMMANDS")
    print("=" * 60)
    print("1. Start FastAPI backend:")
    print("   python main.py")
    print("\n2. Start Flask UI server:")
    print("   python ui_server.py")
    print("\n3. Start both servers:")
    print("   python start_ui.py")
    print("\n4. Check if servers are running:")
    print("   netstat -an | findstr :8000")
    print("   netstat -an | findstr :5000")

if __name__ == "__main__":
    main()
