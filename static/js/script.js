// Medical Chatbot UI JavaScript
// This file handles all the interactive functionality for the medical assistant interface

// Global variables to store chat state and configuration
let currentThreadId = 'main_conversation'; // Unique identifier for this chat session
let isTyping = false; // Flag to prevent multiple simultaneous requests

// Prefer talking to Flask UI proxy (same-origin) to avoid CORS and port issues.
// If you want to hit FastAPI directly, set USE_PROXY to false.
const USE_PROXY = true;
const HEALTH_ENDPOINT = USE_PROXY ? '/api/health' : 'http://localhost:8000/health';
const CHAT_ENDPOINT = USE_PROXY ? '/api/chat' : 'http://localhost:8000/chat';

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Set the current time in the welcome message
    updateWelcomeTime();
    
    // Set up event listeners for user interactions
    setupEventListeners();
    
    // Check if the backend (via proxy) is available
    checkBackendHealth();
    
    console.log('Medical Assistant UI initialized successfully');
});

/**
 * Set up all event listeners for user interactions
 * This includes keyboard events, button clicks, and form submissions
 */
function setupEventListeners() {
    // Get references to important DOM elements
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const charCounter = document.getElementById('charCounter');
    
    // Handle Enter key press in the message input
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent form submission
            sendMessage(); // Send the message
        }
    });
    
    // Handle input changes to update character counter
    messageInput.addEventListener('input', function() {
        const currentLength = this.value.length;
        const maxLength = 500;
        
        // Update character counter
        charCounter.textContent = `${currentLength}/${maxLength}`;
        
        // Change color if approaching limit
        if (currentLength > maxLength * 0.9) {
            charCounter.style.color = '#e74c3c'; // Red color
        } else if (currentLength > maxLength * 0.7) {
            charCounter.style.color = '#f39c12'; // Orange color
        } else {
            charCounter.style.color = '#7f8c8d'; // Default gray color
        }
        
        // Enable/disable send button based on input
        sendButton.disabled = currentLength === 0 || currentLength > maxLength;
    });
    
    // Handle send button click
    sendButton.addEventListener('click', sendMessage);
    
    // Auto-focus on the input field when page loads
    messageInput.focus();
}

/**
 * Update the welcome message timestamp
 * This shows when the chat session started
 */
function updateWelcomeTime() {
    const welcomeTimeElement = document.getElementById('welcomeTime');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
    welcomeTimeElement.textContent = timeString;
}

/**
 * Check if the backend API is healthy and available
 * This helps users know if the service is working
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(HEALTH_ENDPOINT);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('Backend is healthy and ready');
            // You could show a green indicator here if needed
        } else {
            showErrorMessage('Backend service is not healthy. Some features may not work properly.');
        }
    } catch (error) {
        console.error('Backend health check failed:', error);
        showErrorMessage('Cannot connect to the medical assistant service. Please check your connection.');
    }
}

/**
 * Send a message to the medical assistant
 * This is the main function that handles user input and gets responses
 */
async function sendMessage() {
    // Get the message input element and its value
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    // Validate the message
    if (!message) {
        showErrorMessage('Please enter a message before sending.');
        return;
    }
    
    if (message.length > 500) {
        showErrorMessage('Message is too long. Please keep it under 500 characters.');
        return;
    }
    
    // Prevent multiple simultaneous requests
    if (isTyping) {
        return;
    }
    
    // Clear the input field immediately for better UX
    messageInput.value = '';
    updateCharacterCounter();
    
    // Add the user's message to the chat
    addMessageToChat(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    // Set the typing flag
    isTyping = true;
    
    try {
        // Send the message to the backend API
        const response = await fetch(CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                thread_id: currentThreadId
            })
        });
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse the response data
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add the assistant's response to the chat
        addMessageToChat(data.response, 'assistant');
        
    } catch (error) {
        console.error('Error sending message:', error);
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Show error message to user
        const errorMessage = 'Sorry, I encountered an error processing your request. Please try again.';
        addMessageToChat(errorMessage, 'assistant', true);
    } finally {
        // Reset the typing flag
        isTyping = false;
        
        // Focus back on the input field
        messageInput.focus();
    }
}

/**
 * Send a quick message using the quick action buttons
 * @param {string} message - The message to send
 */
function sendQuickMessage(message) {
    // Set the message in the input field
    const messageInput = document.getElementById('messageInput');
    messageInput.value = message;
    
    // Update character counter
    updateCharacterCounter();
    
    // Send the message
    sendMessage();
}

/**
 * Add a message to the chat interface
 * @param {string} content - The message content
 * @param {string} sender - Either 'user' or 'assistant'
 * @param {boolean} isError - Whether this is an error message
 */
function addMessageToChat(content, sender, isError = false) {
    // Get the chat messages container
    const chatMessages = document.getElementById('chatMessages');
    
    // Create a new message element
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    
    // Get current time for the message
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
    
    // Create the message HTML structure
    messageElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${sender === 'user' ? 'fa-user' : 'fa-robot'}"></i>
        </div>
        <div class="message-content ${isError ? 'error-message' : ''}">
            <div class="message-header">
                <span class="sender-name">${sender === 'user' ? 'You' : 'Medical Assistant'}</span>
                <span class="message-time">${timeString}</span>
            </div>
            <div class="message-text">
                ${formatMessageContent(content)}
            </div>
        </div>
    `;
    
    // Add the message to the chat
    chatMessages.appendChild(messageElement);
    
    // Scroll to the bottom to show the new message
    scrollToBottom();
}

/**
 * Format message content for better display
 * This handles line breaks, lists, and other formatting
 * @param {string} content - The raw message content
 * @returns {string} - Formatted HTML content
 */
function formatMessageContent(content) {
    // Replace line breaks with HTML breaks
    let formatted = content.replace(/\n/g, '<br>');
    
    // Handle bullet points and lists
    formatted = formatted.replace(/^[\s]*[-•]\s*(.+)$/gm, '<li>$1</li>');
    
    // Wrap consecutive list items in ul tags
    formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    
    // Handle bold text (text between **)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Handle italic text (text between *)
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Handle code blocks (text between `)
    formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
    
    return formatted;
}

/**
 * Show typing indicator when the assistant is processing
 */
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = 'flex';
    
    // Scroll to bottom to show the typing indicator
    scrollToBottom();
}

/**
 * Hide typing indicator when the assistant finishes processing
 */
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = 'none';
}

/**
 * Scroll the chat messages to the bottom
 * This ensures users always see the latest messages
 */
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Update the character counter display
 */
function updateCharacterCounter() {
    const messageInput = document.getElementById('messageInput');
    const charCounter = document.getElementById('charCounter');
    const currentLength = messageInput.value.length;
    
    charCounter.textContent = `${currentLength}/500`;
    
    // Change color based on length
    if (currentLength > 450) {
        charCounter.style.color = '#e74c3c';
    } else if (currentLength > 350) {
        charCounter.style.color = '#f39c12';
    } else {
        charCounter.style.color = '#7f8c8d';
    }
}

/**
 * Show an error message to the user
 * @param {string} message - The error message to display
 */
function showErrorMessage(message) {
    // Create a temporary error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.position = 'fixed';
    errorElement.style.top = '20px';
    errorElement.style.right = '20px';
    errorElement.style.zIndex = '1000';
    errorElement.style.padding = '15px';
    errorElement.style.borderRadius = '10px';
    errorElement.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
    
    // Add to the page
    document.body.appendChild(errorElement);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.parentNode.removeChild(errorElement);
        }
    }, 5000);
}

/**
 * Show a success message to the user
 * @param {string} message - The success message to display
 */
function showSuccessMessage(message) {
    // Create a temporary success message element
    const successElement = document.createElement('div');
    successElement.className = 'success-message';
    successElement.textContent = message;
    successElement.style.position = 'fixed';
    successElement.style.top = '20px';
    successElement.style.right = '20px';
    successElement.style.zIndex = '1000';
    successElement.style.padding = '15px';
    successElement.style.borderRadius = '10px';
    successElement.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
    
    // Add to the page
    document.body.appendChild(successElement);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (successElement.parentNode) {
            successElement.parentNode.removeChild(successElement);
        }
    }, 3000);
}

/**
 * Show loading overlay during long operations
 */
function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'flex';
}

/**
 * Hide loading overlay
 */
function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';
}

/**
 * Clear the chat history
 * This function can be called to start a fresh conversation
 */
function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Clear all messages except the welcome message
    const messages = chatMessages.querySelectorAll('.message');
    messages.forEach((message, index) => {
        if (index > 0) { // Keep the first message (welcome message)
            message.remove();
        }
    });
    
    // Generate a new thread ID for the fresh conversation
    currentThreadId = 'conversation_' + Date.now();
    
    showSuccessMessage('Chat history cleared. Starting fresh conversation.');
}

/**
 * Copy text to clipboard
 * @param {string} text - The text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccessMessage('Text copied to clipboard!');
    }).catch(() => {
        showErrorMessage('Failed to copy text to clipboard.');
    });
}

// Export functions for potential use in other scripts
window.MedicalChatbot = {
    sendMessage,
    sendQuickMessage,
    clearChat,
    copyToClipboard,
    showErrorMessage,
    showSuccessMessage
};
