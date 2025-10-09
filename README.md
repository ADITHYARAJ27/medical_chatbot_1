# Medical Assistant FastAPI 🏥

A FastAPI-based medical assistant for Community Health Center Harichandanpur, Keonjhar, Odisha. This AI-powered assistant helps with hospital policies, procedures, visiting hours, and general medical inquiries.

## Features ✨

- **AI-Powered Responses**: Uses LangChain and Groq for intelligent conversations
- **Hospital Policy Search**: Vector-based search through hospital policies PDF
- **Multi-conversation Support**: Maintains conversation history with thread IDs
- **RESTful API**: Clean and well-documented FastAPI endpoints
- **Real-time Information**: Current date/time and hospital information

## Setup Instructions 🚀

### 1. Prerequisites

- Python 3.8 or higher
- Groq API key (sign up at [Groq Console](https://console.groq.com))

### 2. Installation

```bash
# Clone or download the project
cd your-project-directory

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Prepare Hospital Policies (Optional)

If you have a hospital policies PDF:
- Create a folder: `utils/data/`
- Place your PDF file as: `utils/data/hospital_policies.pdf`

If no PDF is available, the system will use fallback content.

### 5. Run the Application

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

## API Endpoints 📡

### 1. Root Information
```bash
GET /
```
Returns basic API information and available endpoints.

### 2. Health Check
```bash
GET /health
```
Check if the service is running properly.

### 3. Hospital Information
```bash
GET /info
```
Get details about the hospital and available services.

### 4. Chat with Assistant
```bash
POST /chat
Content-Type: application/json

{
    "message": "What are the visiting hours?",
    "thread_id": "optional-thread-id"
}
```

### 5. Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Examples 💡

### Python Requests
```python
import requests

# Chat with the assistant
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What are the visiting hours?",
        "thread_id": "user-123"
    }
)

result = response.json()
print(result["response"])
```

### Curl
```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Chat
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Who is the hospital owner?"}'
```

### JavaScript/Fetch
```javascript
fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: "What are the hospital policies?",
        thread_id: "web-user-1"
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## Project Structure 📁

```
project/
├── main.py                 # FastAPI application
├── agent.py               # LangGraph agent setup
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── utils/
│   ├── __init__.py       # Package initialization
│   ├── llm.py           # Groq LLM configuration
│   ├── nodes.py         # Agent nodes
│   ├── state.py         # State management
│   ├── tools.py         # Agent tools
│   └── data/            # Data folder
│       └── hospital_policies.pdf
└── test_api.py          # API testing script
```

## Available Tools 🛠️

The assistant has access to these tools:

1. **search_hospital_policies**: Search through hospital policies and procedures
2. **get_current_datetime**: Get current date and time
3. **get_owner_info**: Information about Dr. Harshin and hospital leadership

## Example Questions 🤔

Try asking the assistant:

- "What are the visiting hours?"
- "Who is the hospital owner?"
- "What are the visitor policies?"
- "What is the current date?"
- "Tell me about patient care policies"
- "How many visitors are allowed at a time?"

## Troubleshooting 🔧

### Common Issues:

1. **"Agent not initialized" error**
   - Check if your Groq API key is valid
   - Ensure all dependencies are installed

2. **PDF loading fails**
   - Check if the PDF file exists at `utils/data/hospital_policies.pdf`
   - The system will use fallback content if PDF is missing

3. **Connection errors**
   - Verify the server is running on the correct port
   - Check firewall settings if accessing remotely

### Logs
The application provides helpful logs during startup and operation. Check the console for any error messages.

## Production Deployment 🚀

For production deployment:

1. Set `reload=False` in the uvicorn configuration
2. Use a production WSGI server like Gunicorn
3. Set up proper logging
4. Configure environment variables securely
5. Use HTTPS in production

```bash
# Example production command
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing 🤝

Feel free to contribute to this project by:
- Adding new features
- Improving error handling
- Enhancing documentation
- Adding more hospital-specific tools

---

**Community Health Center Harichandanpur**  
*Keonjhar, Odisha, India*  
*Under the guidance of Dr. Harshin*
