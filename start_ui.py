"""
Startup Script for Medical Chatbot UI
This script helps you start both the FastAPI backend and Flask UI server easily.
It's designed to be simple and user-friendly for intermediate developers.
"""

import subprocess
import sys
import time
import os
import threading
from pathlib import Path

def print_banner():
    """Print a nice banner for the medical chatbot"""
    print("=" * 60)
    print("🏥 MEDICAL CHATBOT - COMMUNITY HEALTH CENTER")
    print("📍 Harichandanpur, Keonjhar, Odisha, India")
    print("👨‍⚕️ Under the guidance of Dr. Harshin")
    print("=" * 60)
    print()

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = ['flask', 'requests', 'fastapi', 'uvicorn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements are satisfied!")
    return True

def start_fastapi_server():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI Backend Server...")
    
    try:
        # Start the FastAPI server using uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ FastAPI server started on http://localhost:8000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        return None

def start_flask_server():
    """Start the Flask UI server"""
    print("🌐 Starting Flask UI Server...")
    
    try:
        # Start the Flask server
        process = subprocess.Popen([
            sys.executable, "ui_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Flask UI server started on http://localhost:5000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return None

def wait_for_server(url, name, timeout=30):
    """Wait for a server to be ready"""
    import requests
    
    print(f"⏳ Waiting for {name} to be ready...")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ {name} is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print(f"  Still waiting... ({i}/{timeout}s)")
    
    print(f"❌ {name} failed to start within {timeout} seconds")
    return False

def main():
    """Main function to start both servers"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("💡 Please run this script from the medical_chatbot directory")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    print("\n" + "=" * 60)
    print("🚀 STARTING SERVERS")
    print("=" * 60)
    
    # Start FastAPI server
    fastapi_process = start_fastapi_server()
    if not fastapi_process:
        return
    
    # Wait a bit for FastAPI to start
    time.sleep(3)
    
    # Start Flask server
    flask_process = start_flask_server()
    if not flask_process:
        fastapi_process.terminate()
        return
    
    # Wait for servers to be ready
    print("\n⏳ Waiting for servers to be ready...")
    time.sleep(5)
    
    print("\n" + "=" * 60)
    print("🎉 SERVERS ARE RUNNING!")
    print("=" * 60)
    print("🌐 Web Interface: http://localhost:5000")
    print("🔗 Backend API: http://localhost:8000")
    print("🧪 Test Page: http://localhost:5000/test")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    print("💡 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ FastAPI server stopped unexpectedly")
                break
                
            if flask_process.poll() is not None:
                print("❌ Flask server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        
        # Terminate both processes
        if fastapi_process:
            fastapi_process.terminate()
            print("✅ FastAPI server stopped")
            
        if flask_process:
            flask_process.terminate()
            print("✅ Flask server stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
