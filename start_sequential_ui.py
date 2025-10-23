#!/usr/bin/env python3
"""
Start the medical chatbot with sequential information collection flow
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import flask
        import requests
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        # Start the FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ FastAPI backend server started successfully!")
                return process
            else:
                print("❌ FastAPI server not responding properly")
                return None
        except Exception as e:
            print(f"❌ Could not connect to FastAPI server: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        return None

def start_frontend():
    """Start the Flask frontend server"""
    print("🌐 Starting Flask frontend server...")
    try:
        # Start the Flask server
        process = subprocess.Popen([
            sys.executable, "ui_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        print("✅ Flask frontend server started successfully!")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return None

def main():
    """Main function to start both servers"""
    print("🏥 Medical Chatbot with Sequential Information Collection")
    print("=" * 60)
    print("📍 Community Health Center Harichandanpur, Keonjhar, Odisha")
    print("👨‍⚕️ Under guidance of Dr. Harshin")
    print()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Exiting.")
        backend_process.terminate()
        return
    
    print()
    print("🎉 Both servers started successfully!")
    print()
    print("📱 Access the application at:")
    print("   🌐 Frontend (UI): http://localhost:5000")
    print("   🔧 Backend (API): http://localhost:8000")
    print("   📚 API Docs: http://localhost:8000/docs")
    print()
    print("🔄 Sequential Information Collection Flow:")
    print("   1. 👤 Full Name")
    print("   2. 🎂 Age")
    print("   3. 📞 Phone Number")
    print("   4. 🏥 Medical Details/Symptoms")
    print()
    print("Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        # Terminate both processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ Servers stopped successfully")
        print("👋 Thank you for using the Medical Chatbot!")

if __name__ == "__main__":
    main()


