# Medical Chatbot Troubleshooting Guide

## 🚨 Current Issue: "Sorry, I encountered an error processing your request"

### Root Cause
The error message indicates that the chatbot cannot communicate with the backend server. This happens when:
1. The FastAPI backend server is not running
2. The Flask UI server is not running  
3. There's a connection issue between the servers

## 🔧 Quick Fix

### Option 1: Use the Simple Startup Script (Recommended)
```bash
python simple_start.py
```

This script will:
- Check and install missing dependencies
- Start both servers step by step
- Test the connection
- Show you exactly what's working and what's not

### Option 2: Manual Startup

#### Step 1: Start FastAPI Backend
Open a terminal/command prompt and run:
```bash
python main.py
```

You should see output like:
```
🏥 Initializing Medical Assistant for Community Health Center Harichandanpur...
✅ Medical Assistant initialized successfully!
🚀 Starting Medical Assistant FastAPI Server...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 2: Start Flask UI Server
Open another terminal/command prompt and run:
```bash
python ui_server.py
```

You should see output like:
```
🏥 Starting Medical Assistant Web Interface...
🌐 Flask UI Server
🔗 UI Server: http://localhost:5000
```

#### Step 3: Test the Connection
1. Open your web browser
2. Go to http://localhost:5000
3. Try asking a question like "What are the visiting hours?"

## 🔍 Common Issues and Solutions

### Issue 1: "No module named 'langchain'"
**Solution:**
```bash
pip install langchain langchain-groq langchain-community langchain-huggingface langgraph
```

### Issue 2: "No module named 'fastapi'"
**Solution:**
```bash
pip install fastapi uvicorn
```

### Issue 3: "No module named 'flask'"
**Solution:**
```bash
pip install flask requests
```

### Issue 4: Port 8000 or 5000 already in use
**Solution:**
1. Find and kill the process using the port:
   ```bash
   # For Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID_NUMBER> /F
   ```
2. Or restart your computer

### Issue 5: "Cannot connect to backend"
**Solution:**
1. Make sure FastAPI server is running on port 8000
2. Check if you can access http://localhost:8000/health
3. If not, restart the FastAPI server

### Issue 6: "Cannot connect to UI server"
**Solution:**
1. Make sure Flask server is running on port 5000
2. Check if you can access http://localhost:5000
3. If not, restart the Flask server

## 🧪 Testing Your Setup

### Test 1: Check if servers are running
```bash
# Check port 8000 (FastAPI)
netstat -an | findstr :8000

# Check port 5000 (Flask)
netstat -an | findstr :5000
```

### Test 2: Test FastAPI backend
Open browser and go to: http://localhost:8000/health
You should see: `{"status":"healthy","message":"Medical Assistant is running and ready to help!"}`

### Test 3: Test Flask UI
Open browser and go to: http://localhost:5000
You should see the chat interface

### Test 4: Test the complete flow
1. Go to http://localhost:5000
2. Type "Hello" in the chat
3. You should get a response from the medical assistant

## 📋 Step-by-Step Debugging

### If the chatbot still shows errors:

1. **Check the terminal where you started the servers**
   - Look for error messages
   - Check if the servers are still running

2. **Test the backend directly**
   ```bash
   curl http://localhost:8000/health
   ```
   Or open http://localhost:8000/health in your browser

3. **Test the UI server**
   ```bash
   curl http://localhost:5000/
   ```
   Or open http://localhost:5000 in your browser

4. **Check the browser console**
   - Press F12 in your browser
   - Go to the Console tab
   - Look for JavaScript errors

5. **Run the diagnostic script**
   ```bash
   python diagnose_issue.py
   ```

## 🆘 Still Having Issues?

If you're still experiencing problems:

1. **Check your Python version**
   ```bash
   python --version
   ```
   Make sure you're using Python 3.8 or higher

2. **Check your working directory**
   Make sure you're running the commands from the `medical_chatbot` folder

3. **Check file permissions**
   Make sure you have read/write permissions in the project folder

4. **Try a clean restart**
   ```bash
   # Stop all Python processes
   taskkill /F /IM python.exe
   
   # Start fresh
   python simple_start.py
   ```

## 📞 Getting Help

If none of the above solutions work:

1. Run the diagnostic script and save the output
2. Check the terminal output when starting the servers
3. Note any error messages you see
4. Provide this information when asking for help

## ✅ Success Indicators

You'll know everything is working when:
- ✅ FastAPI server shows "Uvicorn running on http://0.0.0.0:8000"
- ✅ Flask server shows "Running on http://0.0.0.0:5000"
- ✅ You can access http://localhost:5000 in your browser
- ✅ The chat interface loads without errors
- ✅ You can send messages and get responses

---

**Remember:** Both servers must be running for the chatbot to work properly!
