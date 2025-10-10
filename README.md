# Medical Assistant Platform (FastAPI + Flask UI) 🏥

A FastAPI-based medical assistant with a simple Flask web UI for Community Health Center Harichandanpur, Keonjhar, Odisha. This AI-powered assistant helps with hospital policies, visiting hours, general medical inquiries, and includes a token booking system.

## Features ✨

- **AI-Powered Responses**: LangGraph + LangChain with Groq LLM
- **Hospital Policy Search**: Vector-based search through `utils/data/hospital_policies.pdf`
- **Multi-conversation Support**: Conversation memory via thread IDs
- **RESTful API**: Clean FastAPI endpoints (+ Swagger/ReDoc)
- **Flask Web UI**: Simple UI server proxying to FastAPI backend
- **Token Booking System**: Book, search, update, cancel, and view stats for tokens
- **Real-time Information**: Current date/time and hospital information

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

```bash
# Start FastAPI backend (recommended during development)
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, start the Flask UI
python ui_server.py  # serves UI at http://localhost:5000
```

- FastAPI API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Flask UI: `http://localhost:5000`

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
├── main.py                 # FastAPI application
├── ui_server.py            # Flask UI server (proxy to FastAPI)
├── agent.py                # LangGraph agent setup
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── utils/
│   ├── __init__.py
│   ├── llm.py             # Groq LLM configuration
│   ├── nodes.py           # Agent nodes
│   ├── state.py           # State management
│   ├── tools.py           # Agent tools (incl. token helpers)
│   ├── token_booking.py   # Token booking domain/model/manager
│   └── token_routes.py    # FastAPI routes for tokens
├── templates/
│   └── index.html         # Web UI template
├── static/                # CSS/JS for UI
└── utils/data/
    └── hospital_policies.pdf (optional)
```

## Available Tools 🛠️

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

## Troubleshooting 🔧

- See `TROUBLESHOOTING.md` for common startup and runtime issues.
- If policies PDF fails to load, ensure `utils/data/hospital_policies.pdf` exists; fallback content will be used otherwise.
- If the UI cannot chat, verify the FastAPI backend is running and reachable by the Flask server.
- If the agent fails to initialize, check `GROQ_API_KEY` and internet access.

## Token Booking Guide 📖

For end-to-end examples and best practices, see `TOKEN_BOOKING_GUIDE.md`.

## Production Deployment 🚀

- Run Uvicorn without reload, behind a process manager / reverse proxy.
- Configure HTTPS, logging, and secure env management.

Example:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing 🤝

- Add new features or tools
- Improve error handling and logs
- Enhance documentation
- Extend the token booking workflows

---

**Community Health Center Harichandanpur**  
*Keonjhar, Odisha, India*  
*Under the guidance of Dr. Harshin*
