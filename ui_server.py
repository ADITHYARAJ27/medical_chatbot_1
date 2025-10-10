"""
Flask Web Server for Medical Chatbot UI
This server serves the web interface and acts as a proxy to the FastAPI backend.
It's designed to be simple and easy to understand for intermediate developers.
"""

# Import necessary Flask modules
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import os
from datetime import datetime

# Create Flask application instance
app = Flask(__name__)

# Configuration settings
# These can be changed based on your setup
FASTAPI_BASE_URL = "http://localhost:8000"  # URL of your FastAPI backend
DEBUG_MODE = True  # Set to False in production

# Configure Flask app
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['DEBUG'] = DEBUG_MODE

@app.route('/')
def index():
    """
    Main route that serves the chat interface
    This is the entry point for users accessing the medical chatbot
    """
    try:
        # Render the main HTML template
        return render_template('index.html')
    except Exception as e:
        # If there's an error loading the template, return a simple error page
        return f"""
        <html>
            <head><title>Error - Medical Assistant</title></head>
            <body>
                <h1>Error Loading Medical Assistant</h1>
                <p>Sorry, there was an error loading the interface. Please try again later.</p>
                <p>Error: {str(e)}</p>
            </body>
        </html>
        """, 500

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    """
    Proxy endpoint that forwards chat requests to the FastAPI backend
    This allows the frontend to communicate with the medical assistant
    """
    try:
        # Get the JSON data from the frontend request
        data = request.get_json()
        
        # Validate that we have the required data
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message in request',
                'status': 'error'
            }), 400
        
        # Prepare the request to send to FastAPI backend
        fastapi_payload = {
            'message': data['message'],
            'thread_id': data.get('thread_id', 'default')
        }
        
        # Make request to FastAPI backend
        response = requests.post(
            f"{FASTAPI_BASE_URL}/chat",
            json=fastapi_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30  # 30 second timeout
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the response from FastAPI
            return jsonify(response.json())
        else:
            # Handle errors from FastAPI
            error_message = "Sorry, the medical assistant is temporarily unavailable."
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    error_message = error_data['detail']
            except:
                pass
            
            return jsonify({
                'response': error_message,
                'status': 'error'
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        # Handle connection errors (FastAPI server not running)
        return jsonify({
            'response': 'Cannot connect to the medical assistant service. Please make sure the backend server is running.',
            'status': 'error'
        }), 503
        
    except requests.exceptions.Timeout:
        # Handle timeout errors
        return jsonify({
            'response': 'The request timed out. Please try again with a shorter message.',
            'status': 'error'
        }), 408
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Error in chat_proxy: {str(e)}")
        return jsonify({
            'response': 'An unexpected error occurred. Please try again.',
            'status': 'error'
        }), 500

@app.route('/api/health')
def health_check():
    """
    Health check endpoint to verify if the service is running
    This also checks if the FastAPI backend is accessible
    """
    try:
        # Check if FastAPI backend is accessible
        response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            backend_data = response.json()
            return jsonify({
                'status': 'healthy',
                'message': 'Flask UI server and FastAPI backend are both running',
                'backend_status': backend_data.get('status', 'unknown'),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'degraded',
                'message': 'Flask UI server is running, but FastAPI backend is not responding properly',
                'backend_status': 'unhealthy',
                'timestamp': datetime.now().isoformat()
            }), 503
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'status': 'degraded',
            'message': 'Flask UI server is running, but cannot connect to FastAPI backend',
            'backend_status': 'unreachable',
            'timestamp': datetime.now().isoformat()
        }), 503
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Health check failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/info')
def get_hospital_info():
    """
    Get hospital information from the FastAPI backend
    This provides details about the hospital and available services
    """
    try:
        # Get hospital info from FastAPI backend
        response = requests.get(f"{FASTAPI_BASE_URL}/info", timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            # Return fallback information if backend is not available
            return jsonify({
                'hospital_name': 'Community Health Center Harichandanpur',
                'location': 'Keonjhar, Odisha, India',
                'owner': 'Dr. Hari',
                'services': [
                    'Hospital policies and procedures information',
                    'Visiting hours and visitor guidelines',
                    'General medical information',
                    'Hospital management inquiries'
                ],
                'features': [
                    '24/7 AI assistance',
                    'Multi-conversation support',
                    'Policy document search',
                    'Real-time information'
                ],
                'note': 'Backend service temporarily unavailable'
            })
            
    except Exception as e:
        print(f"Error getting hospital info: {str(e)}")
        return jsonify({
            'error': 'Could not retrieve hospital information',
            'message': str(e)
        }), 500

@app.route('/api/tokens', methods=['GET', 'POST'])
def token_proxy():
    """
    Proxy endpoint for token booking operations
    This forwards token-related requests to the FastAPI backend
    """
    try:
        if request.method == 'GET':
            # Handle GET requests (searching tokens)
            params = request.args.to_dict()
            response = requests.get(f"{FASTAPI_BASE_URL}/tokens", params=params, timeout=10)
        else:
            # Handle POST requests (creating tokens)
            data = request.get_json()
            response = requests.post(f"{FASTAPI_BASE_URL}/tokens", json=data, timeout=10)
        
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Cannot connect to token booking service',
            'message': 'Please make sure the backend server is running'
        }), 503
        
    except Exception as e:
        print(f"Error in token_proxy: {str(e)}")
        return jsonify({
            'error': 'Token operation failed',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors (page not found)
    """
    return jsonify({
        'error': 'Page not found',
        'message': 'The requested page does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors (internal server errors)
    """
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end. Please try again later.'
    }), 500

@app.route('/test')
def test_page():
    """
    Simple test page to verify the Flask server is working
    This is useful for debugging and testing
    """
    return """
    <html>
        <head>
            <title>Medical Assistant - Test Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
                .success { background-color: #d4edda; color: #155724; }
                .error { background-color: #f8d7da; color: #721c24; }
                .info { background-color: #d1ecf1; color: #0c5460; }
            </style>
        </head>
        <body>
            <h1>Medical Assistant - System Test</h1>
            
            <div class="status info">
                <strong>Flask UI Server:</strong> Running ✅
            </div>
            
            <div id="backend-status" class="status">
                <strong>FastAPI Backend:</strong> Checking...
            </div>
            
            <div class="status info">
                <strong>Current Time:</strong> <span id="current-time"></span>
            </div>
            
            <h2>Available Endpoints:</h2>
            <ul>
                <li><a href="/">Main Chat Interface</a></li>
                <li><a href="/api/health">Health Check</a></li>
                <li><a href="/api/info">Hospital Information</a></li>
            </ul>
            
            <script>
                // Update current time
                document.getElementById('current-time').textContent = new Date().toLocaleString();
                
                // Check backend status
                fetch('/api/health')
                    .then(response => response.json())
                    .then(data => {
                        const statusDiv = document.getElementById('backend-status');
                        if (data.status === 'healthy') {
                            statusDiv.className = 'status success';
                            statusDiv.innerHTML = '<strong>FastAPI Backend:</strong> Running ✅';
                        } else {
                            statusDiv.className = 'status error';
                            statusDiv.innerHTML = '<strong>FastAPI Backend:</strong> Not Available ❌';
                        }
                    })
                    .catch(error => {
                        const statusDiv = document.getElementById('backend-status');
                        statusDiv.className = 'status error';
                        statusDiv.innerHTML = '<strong>FastAPI Backend:</strong> Connection Failed ❌';
                    });
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    """
    Main entry point for the Flask application
    This starts the web server when the script is run directly
    """
    print("Starting Medical Assistant Web Interface...")
    print("Flask UI Server")
    print("Community Health Center Harichandanpur")
    print("Under the guidance of Dr. Harshin")
    print("-" * 50)
    print(f"UI Server: http://localhost:5000")
    print(f"Test Page: http://localhost:5000/test")
    print(f"Backend API: {FASTAPI_BASE_URL}")
    print("-" * 50)
    print("Make sure your FastAPI backend is running on port 8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the Flask development server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,       # Port for the Flask server
        debug=DEBUG_MODE, # Enable debug mode for development
        threaded=True    # Enable threading for better performance
    )
