"""
Example usage of the Medical Assistant FastAPI

This file demonstrates how to interact with the FastAPI endpoints
using Python requests library.
"""

import requests
import json

# Base URL for the API (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_basic_info():
    """Test the basic info endpoint"""
    print("ℹ️  Testing basic info...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_hospital_info():
    """Test the hospital info endpoint"""
    print("🏥 Testing hospital info...")
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_chat(message: str, thread_id: str = "test-thread"):
    """Test the chat endpoint"""
    print(f"💬 Testing chat with message: '{message}'")
    
    payload = {
        "message": message,
        "thread_id": thread_id
    }
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Assistant Response: {result['response']}")
        print(f"Thread ID: {result['thread_id']}")
        print(f"Status: {result['status']}")
    else:
        print(f"Error: {response.json()}")
    
    print("-" * 50)

def main():
    """Main function to run all tests"""
    print("🤖 Testing Medical Assistant FastAPI")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        test_health_check()
        test_basic_info()
        test_hospital_info()
        
        # Test chat functionality
        test_chat("What are the visiting hours?")
        test_chat("Who is the hospital owner?")
        test_chat("What are the hospital policies for visitors?")
        test_chat("What is the current date and time?")
        
        print("✅ All tests completed!")
        
    except requests.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()


# Alternative: Using curl commands
"""
You can also test the API using curl commands:

# Health check
curl -X GET "http://localhost:8000/health"

# Basic info
curl -X GET "http://localhost:8000/"

# Hospital info
curl -X GET "http://localhost:8000/info"

# Chat endpoint
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the visiting hours?", "thread_id": "test"}'
"""