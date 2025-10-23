# Medical Assistant Platform (FastAPI + Flask UI) 🏥

A FastAPI-based medical assistant with a simple Flask web UI for Community Health Center Harichandanpur, Keonjhar, Odisha. This AI-powered assistant helps with hospital policies, visiting hours, general medical inquiries, and includes a comprehensive token booking system with **intelligent sequential information collection**.

## Features ✨

- **🧠 Intelligent Sequential Information Collection**: Collects user details step-by-step (Name → Age → Phone → Medical Details) with smart validation
- **🤖 AI-Powered Responses**: LangGraph + LangChain with Groq LLM for natural conversations
- **🏥 Hospital Policy Search**: Vector-based search through `utils/data/hospital_policies.pdf`
- **💬 Multi-conversation Support**: Advanced conversation memory via thread IDs with state management
- **🔗 RESTful API**: Clean FastAPI endpoints with comprehensive Swagger/ReDoc documentation
- **🌐 Modern Web UI**: Responsive Flask UI with sequential flow support and mobile optimization
- **🎫 Advanced Token Booking System**: Complete booking management with search, update, cancel, and analytics
- **⏰ Real-time Information**: Current date/time and hospital information with live updates
- **📊 Conversation State Management**: Intelligent tracking of information collection progress
- **🧪 Comprehensive Testing**: Full test suite for conversation state, sequential flow, and token booking
- **📱 Mobile-First Design**: Optimized for mobile devices with touch-friendly interface

## Setup Instructions 🚀

### 1. Prerequisites

- Python 3.10 or higher
- Groq API key (sign up at `https://console.groq.com`)

### 2. Installation

```bash
# From project root
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```bash
# .env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Prepare Hospital Policies (Optional)

If you have a hospital policies PDF:
- Place your PDF file at `utils/data/hospital_policies.pdf`

If no PDF is available, the system will use fallback content.

### 5. Run the Services

You have two servers: FastAPI backend (core API) and Flask UI (web interface proxy).

**Option 1: Start both servers automatically (Recommended)**
```bash
# Start both servers with sequential flow support
python start_sequential_ui.py
```

**Option 2: Start servers manually**
```bash
# Start FastAPI backend (recommended during development)
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, start the Flask UI
python ui_server.py  # serves UI at http://localhost:5000
```

**Option 3: Start with basic UI (legacy)**
```bash
# Start with basic UI (without sequential flow)
python start_ui.py
```

- FastAPI API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Flask UI: `http://localhost:5000`

### 6. Sequential Information Collection Flow

The assistant now collects user information in a specific order with intelligent validation:

1. **👤 Full Name**: "Hello! I'm your medical assistant. To help you better, may I please have your full name?"
2. **🎂 Age**: "Thank you! What is your age?" (validates 0-150 years)
3. **📞 Phone Number**: "Great! What is your phone number?" (validates 10+ digits)
4. **🏥 Medical Details**: "Perfect! Please tell me about your medical concerns or symptoms." (validates meaningful text)

After collecting all information, the assistant can help with token booking and other services.

**Key Benefits:**
- 🎯 **Focused Interaction**: One question at a time
- 📱 **Mobile Optimized**: Perfect for mobile devices
- ✅ **Smart Validation**: Each input is validated before proceeding
- 🔄 **Natural Flow**: Mimics human conversation patterns
- 🛡️ **Error Handling**: Graceful handling of invalid inputs

## API Endpoints 📡

### Core
- `GET /` – API info
- `GET /health` – health check
- `GET /info` – hospital and features info
- `POST /chat` – chat with assistant

Request example:
```json
{
  "message": "What are the visiting hours?",
  "thread_id": "optional-thread-id"
}
```

### Token Booking (`/tokens`)
The token booking API enables patient token management.

- `POST /tokens/book` – create a token
- `GET /tokens/{token_id}` – get details
- `PUT /tokens/{token_id}/status` – update status
- `DELETE /tokens/{token_id}` – cancel
- `GET /tokens/search` – filter by patient, phone, department, date, status, token number
- `GET /tokens/daily/{date}` – bookings for a date (optional `department`)
- `GET /tokens/stats` – summary stats
- `GET /tokens/departments` – list departments
- `GET /tokens/statuses` – list statuses
- `POST /tokens/current/set` – set the token currently being served by a doctor
- `GET /tokens/current/{doctor_name}` – get which token a doctor is serving now

See more in `utils/token_routes.py` and `utils/token_booking.py`.

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Examples 💡

### Test Sequential Flow
```bash
# Test the sequential information collection
python test_sequential_flow.py

# Test conversation state management
python test_conversation_state_simple.py

# Demo the sequential flow
python demo_sequential_simple.py
```

### Python (chat)
```python
import requests
resp = requests.post("http://localhost:8000/chat", json={
    "message": "What are the visiting hours?",
    "thread_id": "user-123"
})
print(resp.json()["response"])
```

### Curl (health + chat)
```bash
curl -s "http://localhost:8000/health"

curl -s -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is the hospital owner?"}'
```

### Token booking: create and check
```bash
# Book a token
curl -s -X POST "http://localhost:8000/tokens/book" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "patient_phone": "9998887777",
    "patient_age": 42,
    "department": "general_medicine",
    "booking_date": "2025-10-10",
    "booking_time": "10:30",
    "doctor_name": "Dr. Sharma",
    "symptoms": "fever, cough",
    "priority": "normal"
  }'

# Get token details
curl -s "http://localhost:8000/tokens/{token_id}"

# Set current serving token for a doctor
curl -s -X POST "http://localhost:8000/tokens/current/set" \
  -H "Content-Type: application/json" \
  -d '{
    "department": "cardiology",
    "doctor_name": "Dr. Sharma",
    "token_id": "abc-123"
  }'

# Query which token the doctor is on
curl -s "http://localhost:8000/tokens/current/Dr.%20Sharma"
```

## Project Structure 📁

```
project/
├── main.py                           # FastAPI application
├── ui_server.py                      # Flask UI server (proxy to FastAPI)
├── agent.py                          # LangGraph agent setup
├── start_sequential_ui.py            # Start both servers with sequential flow
├── start_ui.py                       # Start with basic UI (legacy)
├── test_sequential_flow.py           # Test script for sequential collection
├── test_conversation_state_simple.py # Test conversation state management
├── demo_sequential_simple.py        # Demo sequential flow
├── requirements.txt                  # Dependencies
├── .env                             # Environment variables
├── utils/
│   ├── __init__.py
│   ├── llm.py                       # Groq LLM configuration
│   ├── nodes.py                     # Agent nodes with sequential flow
│   ├── state.py                     # State management
│   ├── conversation_state.py       # Sequential conversation state management
│   ├── tools.py                     # Agent tools (incl. token helpers)
│   ├── token_booking.py            # Token booking domain/model/manager
│   └── token_routes.py             # FastAPI routes for tokens
├── templates/
│   └── index.html                   # Web UI template with sequential flow
├── static/                          # CSS/JS for UI
│   ├── css/style.css               # Responsive styling
│   └── js/script.js                # Interactive functionality
├── utils/data/
│   ├── hospital_policies.pdf       # Hospital policies (optional)
│   └── token_bookings.json         # Token booking data
├── SEQUENTIAL_FLOW_UPDATE.md        # Detailed sequential flow documentation
├── TOKEN_BOOKING_GUIDE.md          # Comprehensive token booking guide
├── UI_README.md                     # Web interface documentation
└── TROUBLESHOOTING.md              # Troubleshooting guide
```

## Available Tools 

From `utils/tools.py` the assistant can use:

1. `search_hospital_policies`
2. `get_current_datetime`
3. `get_owner_info`
4. `book_medical_token`
5. `check_token_status`
6. `search_tokens`
7. `get_daily_tokens`
8. `get_booking_statistics`
9. `get_current_serving_token` ← new

## Flask UI Endpoints (proxy) 🌐

The Flask server (`ui_server.py`) exposes convenient endpoints and proxies to the FastAPI backend:
- `GET /` – Chat UI
- `POST /api/chat` – proxies to `POST /chat`
- `GET /api/health` – checks backend health
- `GET /api/info` – proxies to `GET /info` with fallback
- `GET|POST /api/tokens` – basic proxy for token operations
- `GET /test` – simple test page

Ensure FastAPI is running at `http://localhost:8000` before starting the Flask UI.

## Testing 🧪

### Comprehensive Test Suite

The project includes a full test suite to ensure all functionality works correctly:

```bash
# Test conversation state management (no API key required)
python test_conversation_state_simple.py

# Test sequential flow (requires API key)
python test_sequential_flow.py

# Demo sequential flow (no API key required)
python demo_sequential_simple.py

# Test token booking system
python test_token_booking.py

# Test UI functionality
python test_ui_simple.py
```

### Test Coverage

- ✅ **Conversation State Management**: Tests state transitions and data collection
- ✅ **Sequential Flow**: Tests the complete information collection process
- ✅ **Token Booking**: Tests booking, search, update, and cancellation
- ✅ **UI Components**: Tests web interface functionality
- ✅ **Edge Cases**: Tests error handling and validation
- ✅ **Multi-threading**: Tests concurrent conversation support

### Running Tests

```bash
# Run all tests
python -m pytest test_*.py

# Run specific test categories
python test_conversation_state_simple.py  # State management
python demo_sequential_simple.py        # Flow demonstration
```

## Troubleshooting 🔧

### Common Issues

**1. "Cannot connect to backend" error**
- Ensure FastAPI server is running on port 8000
- Check if `python main.py` is running
- Verify firewall settings

**2. Sequential flow not working**
- Check if `start_sequential_ui.py` is being used
- Verify conversation state is being maintained
- Check browser console for JavaScript errors

**3. Token booking issues**
- Verify `utils/data/token_bookings.json` exists and is writable
- Check if all required fields are provided
- Ensure date format is YYYY-MM-DD

**4. API key issues**
- Verify `GROQ_API_KEY` is set in `.env` file
- Check if API key is valid and has sufficient credits
- Ensure internet connectivity

### Debug Mode

Enable debug mode for detailed logging:
```bash
# Set environment variable
export DEBUG_MODE=True

# Or modify in code
DEBUG_MODE = True  # In ui_server.py
```

### Logs and Monitoring

- Check terminal output for error messages
- Monitor browser console for JavaScript errors
- Verify API responses in network tab
- Check file permissions for data storage

### Additional Resources

- See `TROUBLESHOOTING.md` for detailed troubleshooting guide
- Check `SEQUENTIAL_FLOW_UPDATE.md` for sequential flow documentation
- Review `TOKEN_BOOKING_GUIDE.md` for booking system details
- Consult `UI_README.md` for web interface help

## Documentation 📚

### Comprehensive Guides

- **📋 TOKEN_BOOKING_GUIDE.md**: Complete token booking system documentation
- **🔄 SEQUENTIAL_FLOW_UPDATE.md**: Detailed sequential information collection guide
- **🌐 UI_README.md**: Web interface documentation and customization
- **🔧 TROUBLESHOOTING.md**: Common issues and solutions

### Quick Reference

| Feature | Documentation | Test File |
|---------|---------------|-----------|
| Sequential Flow | `SEQUENTIAL_FLOW_UPDATE.md` | `demo_sequential_simple.py` |
| Token Booking | `TOKEN_BOOKING_GUIDE.md` | `test_token_booking.py` |
| Web UI | `UI_README.md` | `test_ui_simple.py` |
| State Management | - | `test_conversation_state_simple.py` |

## Production Deployment 🚀

### Recommended Setup

```bash
# Production deployment with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# With environment variables
export GROQ_API_KEY=your_production_key
export DEBUG_MODE=False
```

### Security Considerations

- Configure HTTPS for production
- Set up proper authentication
- Use environment variables for sensitive data
- Implement rate limiting
- Set up monitoring and logging

### Performance Optimization

- Use a reverse proxy (Nginx)
- Configure caching
- Optimize database queries
- Monitor resource usage

## Contributing 🤝

### Development Areas

- **🧠 AI Enhancement**: Improve conversation flow and response quality
- **🎫 Token System**: Add new booking features and analytics
- **🌐 UI/UX**: Enhance user interface and mobile experience
- **🧪 Testing**: Expand test coverage and automation
- **📚 Documentation**: Improve guides and examples

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

### Code Standards

- Follow PEP 8 for Python code
- Add comprehensive tests for new features
- Update documentation for changes
- Ensure mobile compatibility

---

**Community Health Center Harichandanpur**  
*Keonjhar, Odisha, India*  
*Under the guidance of Dr. Harshin*
