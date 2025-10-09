from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from contextlib import asynccontextmanager

# Import your existing agent modules
from agent import create_agent
from agent import run_agent
from utils.token_routes import router as token_router

# Global variable to store the agent
agent_executor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    Initializes the agent on startup and cleans up on shutdown.
    """
    global agent_executor
    print("🏥 Initializing Medical Assistant for Community Health Center Harichandanpur...")
    
    try:
        # Initialize the agent on startup
        agent_executor = create_agent()
        print("✅ Medical Assistant initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        raise
    
    yield  # Application runs here
    
    # Cleanup on shutdown (if needed)
    print("👋 Shutting down Medical Assistant...")

# Create FastAPI app with lifespan events
app = FastAPI(
    title="Medical Assistant API",
    description="AI-powered medical assistant for Community Health Center Harichandanpur, Keonjhar, Odisha",
    version="1.0.0",
    lifespan=lifespan
)

# Include token booking routes
app.include_router(token_router)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat interactions"""
    message: str
    thread_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    """Response model for chat interactions"""
    response: str
    thread_id: str
    status: str = "success"

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str

# API Routes

@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint - Basic API information
    """
    return {
        "message": "Medical Assistant API for Community Health Center Harichandanpur",
        "status": "active",
        "description": "AI-powered assistant for hospital policies, procedures, and medical information",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify if the service is running
    """
    global agent_executor
    
    if agent_executor is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return HealthResponse(
        status="healthy",
        message="Medical Assistant is running and ready to help!"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    Main chat endpoint for interacting with the medical assistant.
    
    Args:
        request: ChatRequest containing user message and optional thread_id
    
    Returns:
        ChatResponse with assistant's reply and thread information
    """
    global agent_executor
    
    # Validate agent is initialized
    if agent_executor is None:
        raise HTTPException(
            status_code=503, 
            detail="Medical Assistant is not available. Please try again later."
        )
    
    # Validate input
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400, 
            detail="Message cannot be empty"
        )
    
    try:
        # Get response from the agent
        assistant_response = run_agent(
            agent_executor, 
            request.message.strip(), 
            request.thread_id
        )
        
        return ChatResponse(
            response=assistant_response,
            thread_id=request.thread_id,
            status="success"
        )
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in chat endpoint: {str(e)}")
        
        raise HTTPException(
            status_code=500, 
            detail="I apologize, but I encountered an error processing your request. Please try again."
        )

@app.get("/info")
async def get_hospital_info():
    """
    Get basic information about the hospital and available services
    """
    return {
        "hospital_name": "Community Health Center Harichandanpur",
        "location": "Keonjhar, Odisha, India",
        "owner": "Dr. Hari",
        "services": [
            "Hospital policies and procedures information",
            "Visiting hours and visitor guidelines",
            "General medical information",
            "Hospital management inquiries"
        ],
        "features": [
            "24/7 AI assistance",
            "Multi-conversation support",
            "Policy document search",
            "Real-time information"
        ]
    }

# Fixed Error handlers - returning JSONResponse objects instead of dicts
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 error handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist. Visit /docs for available endpoints."
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 error handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please try again later."
        }
    )

# Development server runner
if __name__ == "__main__":
    print("🚀 Starting Medical Assistant FastAPI Server...")
    print("🏥 Community Health Center Harichandanpur - AI Assistant")
    print("📍 Location: Keonjhar, Odisha, India")
    print("👨‍⚕️ Under the guidance of Dr. Harshin")
    print("-" * 50)
    
    # Run the server
    uvicorn.run(
        "main:app",  # Change this to your filename if different
        host="0.0.0.0",  # Allow external connections (changed from 127.0.0.1)
        port=8000,       # Your server port
        reload=True,     # Auto-reload on code changes (development only)
        log_level="info"
    )