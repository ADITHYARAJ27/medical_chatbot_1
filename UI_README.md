# Medical Chatbot Web Interface

A simple, user-friendly web interface for the Medical Assistant at Community Health Center Harichandanpur, Keonjhar, Odisha, India.

## 🏥 What This Interface Provides

This web interface allows users to interact with the AI Medical Assistant through a modern, easy-to-use chat interface. Users can:

- **Ask Questions**: Get information about hospital policies, procedures, and medical information
- **Book Tokens**: Schedule medical appointments and consultations
- **Check Status**: View token booking status and statistics
- **Get Help**: Access visiting hours, guidelines, and general information

## 🚀 Quick Start

### Option 1: Easy Startup (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start both servers automatically
python start_ui.py
```

### Option 2: Manual Startup
```bash
# Terminal 1: Start the FastAPI backend
python main.py

# Terminal 2: Start the Flask UI server
python ui_server.py
```

## 🌐 Access the Interface

Once both servers are running:

- **Main Interface**: http://localhost:5000
- **Test Page**: http://localhost:5000/test
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 File Structure

```
medical_chatbot/
├── templates/
│   └── index.html          # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css       # Styling for the interface
│   └── js/
│       └── script.js       # JavaScript functionality
├── ui_server.py            # Flask server for the web interface
├── start_ui.py             # Easy startup script
├── main.py                 # FastAPI backend (existing)
├── agent.py                # AI agent logic (existing)
└── requirements.txt        # Python dependencies
```

## 🎨 Interface Features

### Modern Design
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Clean Interface**: Easy-to-read chat interface with clear message bubbles
- **Professional Styling**: Medical-themed colors and icons
- **Smooth Animations**: Fade-in effects for new messages

### User-Friendly Features
- **Quick Action Buttons**: Common questions with one-click access
- **Character Counter**: Shows message length (500 character limit)
- **Typing Indicator**: Shows when the assistant is processing
- **Auto-Scroll**: Automatically scrolls to show new messages
- **Error Handling**: Clear error messages when something goes wrong

### Accessibility
- **Keyboard Support**: Press Enter to send messages
- **Clear Typography**: Easy-to-read fonts and colors
- **Icon Indicators**: Visual cues for different message types
- **Mobile Friendly**: Touch-friendly buttons and responsive design

## 💬 How to Use

### 1. Starting a Conversation
- Open http://localhost:5000 in your web browser
- The assistant will greet you with available services
- Type your question in the input field at the bottom

### 2. Quick Actions
Use the quick action buttons for common tasks:
- **Visiting Hours**: Get information about hospital visiting times
- **Book Token**: Learn how to schedule an appointment
- **Hospital Policies**: Access hospital rules and procedures
- **Statistics**: View token booking statistics

### 3. Sending Messages
- Type your question in the input field
- Press Enter or click the Send button
- Wait for the assistant's response
- Continue the conversation as needed

### 4. Example Questions
Try asking:
- "What are the visiting hours?"
- "How do I book a token for cardiology?"
- "What are the hospital policies for visitors?"
- "Check my token status with ID ABC123"
- "Show me today's token statistics"

## 🔧 Technical Details

### Frontend (Client-Side)
- **HTML5**: Semantic markup for accessibility
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Vanilla JS for functionality (no frameworks needed)
- **Font Awesome**: Icons for better visual experience

### Backend (Server-Side)
- **Flask**: Lightweight web framework for serving the UI
- **FastAPI**: High-performance API for the medical assistant
- **Requests**: HTTP client for communication between servers
- **Jinja2**: Template engine for dynamic HTML generation

### Communication Flow
```
User Browser → Flask UI Server → FastAPI Backend → AI Agent → Response
```

## 🛠️ Customization

### Changing Colors
Edit `static/css/style.css` to modify the color scheme:
```css
/* Main background gradient */
body {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}

/* Header background */
.header {
    background: linear-gradient(135deg, #your-header-color-1, #your-header-color-2);
}
```

### Adding New Quick Actions
Edit `templates/index.html` to add more quick action buttons:
```html
<button class="quick-btn" onclick="sendQuickMessage('Your question here')">
    <i class="fas fa-your-icon"></i> Button Text
</button>
```

### Modifying the Welcome Message
Edit the welcome message in `templates/index.html`:
```html
<div class="message-text">
    <p>Your custom welcome message here...</p>
</div>
```

## 🐛 Troubleshooting

### Common Issues

**1. "Cannot connect to backend" error**
- Make sure the FastAPI server is running on port 8000
- Check if `python main.py` is running in another terminal

**2. "Page not found" error**
- Ensure you're accessing http://localhost:5000 (not 8000)
- Check if the Flask server is running

**3. Messages not sending**
- Check the browser console for JavaScript errors
- Verify both servers are running and accessible

**4. Styling issues**
- Clear your browser cache (Ctrl+F5)
- Check if CSS files are loading properly

### Debug Mode
Enable debug mode in `ui_server.py`:
```python
DEBUG_MODE = True  # Set to True for detailed error messages
```

### Logs
Check the terminal where you started the servers for error messages and logs.

## 📱 Mobile Usage

The interface is fully responsive and works great on mobile devices:
- Touch-friendly buttons and inputs
- Optimized layout for small screens
- Swipe-friendly chat interface
- Mobile-optimized typography

## 🔒 Security Notes

- This is a development interface - not suitable for production without additional security measures
- The Flask server runs on all interfaces (0.0.0.0) - restrict access in production
- Consider adding authentication and HTTPS for production use

## 🤝 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure both servers are running
4. Check the browser console for JavaScript errors

## 📝 Code Comments

All code is thoroughly commented to help intermediate developers understand:
- **HTML**: Each section explains its purpose
- **CSS**: Comments explain styling choices and responsive design
- **JavaScript**: Functions are documented with clear explanations
- **Python**: Flask routes and logic are well-commented

This makes it easy to modify and extend the interface according to your needs.

---

**Developed for Community Health Center Harichandanpur**  
**Under the guidance of Dr. Harshin**  
**Keonjhar, Odisha, India**
