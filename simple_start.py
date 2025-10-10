"""
Simple Startup Script for Medical Chatbot
This script provides a step-by-step approach to start the chatbot.
"""

import subprocess
import sys
import time
import os

def print_step(step_num, description):
    """Print a step with clear formatting"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print('='*60)

def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(1, "CHECKING DEPENDENCIES")
    
    required_packages = {
        'flask': 'Flask',
        'requests': 'Requests', 
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is missing")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
            print("✓ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("✗ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing)}")
            return False
    
    return True

def start_fastapi():
    """Start the FastAPI backend"""
    print_step(2, "STARTING FASTAPI BACKEND")
    
    print("Starting FastAPI server on port 8000...")
    print("This may take a few moments...")
    
    try:
        # Start FastAPI in background
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ FastAPI server started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print("✗ FastAPI server failed to start")
            print("Error output:", stderr.decode())
            return None
            
    except Exception as e:
        print(f"✗ Error starting FastAPI: {e}")
        return None

def start_flask():
    """Start the Flask UI server"""
    print_step(3, "STARTING FLASK UI SERVER")
    
    print("Starting Flask UI server on port 5000...")
    
    try:
        # Start Flask in background
        process = subprocess.Popen([
            sys.executable, 'ui_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Flask UI server started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print("✗ Flask UI server failed to start")
            print("Error output:", stderr.decode())
            return None
            
    except Exception as e:
        print(f"✗ Error starting Flask: {e}")
        return None

def test_servers():
    """Test if both servers are working"""
    print_step(4, "TESTING SERVERS")
    
    import requests
    
    # Test FastAPI
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✓ FastAPI backend is responding")
        else:
            print("✗ FastAPI backend is not responding properly")
            return False
    except:
        print("✗ Cannot connect to FastAPI backend")
        return False
    
    # Test Flask
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✓ Flask UI server is responding")
        else:
            print("✗ Flask UI server is not responding properly")
            return False
    except:
        print("✗ Cannot connect to Flask UI server")
        return False
    
    return True

def main():
    """Main startup process"""
    print("MEDICAL CHATBOT - SIMPLE STARTUP")
    print("This script will help you start the chatbot step by step.")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n✗ Please install missing dependencies and try again.")
        return
    
    # Step 2: Start FastAPI
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("\n✗ Failed to start FastAPI backend.")
        print("Please check the error messages above and try again.")
        return
    
    # Step 3: Start Flask
    flask_process = start_flask()
    if not flask_process:
        print("\n✗ Failed to start Flask UI server.")
        print("Please check the error messages above and try again.")
        return
    
    # Step 4: Test servers
    if test_servers():
        print_step(5, "SUCCESS!")
        print("🎉 Your Medical Chatbot is now running!")
        print("\nAccess your chatbot at:")
        print("🌐 Web Interface: http://localhost:5000")
        print("🔗 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop both servers.")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if fastapi_process.poll() is not None:
                    print("\n✗ FastAPI server stopped unexpectedly")
                    break
                    
                if flask_process.poll() is not None:
                    print("\n✗ Flask server stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\n\nStopping servers...")
            fastapi_process.terminate()
            flask_process.terminate()
            print("✓ Servers stopped. Goodbye!")
    else:
        print("\n✗ Servers are not responding properly.")
        print("Please check the error messages and try again.")

if __name__ == "__main__":
    main()
