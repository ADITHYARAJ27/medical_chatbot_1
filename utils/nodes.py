from langchain_core.messages import SystemMessage
from utils.state import State
from utils.llm import llm_with_tools
from utils.conversation_state import conversation_manager, CollectionStep 

def assistant(state: State):
    """Main assistant function that calls the model with sequential information collection"""
    
    messages = state['messages']
    
    # Get thread_id from the last message or use default
    thread_id = "default"
    if messages:
        # Try to extract thread_id from message metadata if available
        last_message = messages[-1]
        if hasattr(last_message, 'additional_kwargs') and 'thread_id' in last_message.additional_kwargs:
            thread_id = last_message.additional_kwargs['thread_id']
    
    # Get conversation state
    conv_state = conversation_manager.get_state(thread_id)
    
    # Check if this is a new conversation or continuing
    is_new_conversation = len(messages) <= 1 or not any(isinstance(msg, SystemMessage) for msg in messages)
    
    # Add system message if it's the first interaction
    if is_new_conversation:
        system_prompt = f"""You are a helpful medical assistant for Community Health Center Harichandanpur in Keonjhar, Odisha.

CRITICAL INSTRUCTION: You MUST collect user information in this EXACT sequential order:
1. FIRST: Ask for the user's FULL NAME
2. SECOND: Ask for their AGE (in years) 
3. THIRD: Ask for their PHONE NUMBER
4. FOURTH: Ask for their MEDICAL DETAILS/SYMPTOMS

Current conversation state: {conv_state.current_step.value}
Collected information so far:
- Name: {conv_state.user_info.name or 'Not collected'}
- Age: {conv_state.user_info.age or 'Not collected'}
- Phone: {conv_state.user_info.phone or 'Not collected'}
- Details: {conv_state.user_info.details or 'Not collected'}

SEQUENTIAL COLLECTION RULES:
- If this is the first message, immediately ask: "Hello! I'm your medical assistant. To help you better, may I please have your full name?"
- Only after getting the name, ask for age: "Thank you! What is your age?"
- Only after getting age, ask for phone: "Great! What is your phone number?"
- Only after getting phone, ask for details: "Perfect! Please tell me about your medical concerns or symptoms."
- Validate each response (age should be a number, phone should be 10+ digits)
- Be friendly, professional, and encouraging
- Once all 4 pieces of information are collected, you can help with booking or other services

You have access to tools that can help you:
1. Search hospital policies and procedures
2. Get current date and time
3. Get information about the hospital owner Dr. Hari
4. Book medical consultation tokens for patients
5. Check token booking status
6. Search and manage token bookings
7. Get daily token schedules
8. View booking statistics

For token booking, you can help patients:
- Book appointments with specific departments (general_medicine, cardiology, pediatrics, gynecology, orthopedics, emergency, dental, dermatology, psychiatry)
- Check their token status using token ID
- Search for their bookings
- View daily schedules

Always use the appropriate tools to provide accurate information. Be professional, helpful, and caring in your responses. If medical advice is requested that requires professional diagnosis, remind users to consult with healthcare professionals."""
        messages = [SystemMessage(content=system_prompt)] + messages
    
    # Process the conversation and update state
    response = llm_with_tools.invoke(messages)
    
    # Update conversation state based on the response and user input
    if messages and len(messages) > 1:
        user_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        update_conversation_state(conv_state, user_message, response.content)
   
    return {"messages": [response]}

def update_conversation_state(conv_state, user_input: str, assistant_response: str):
    """Update conversation state based on user input and assistant response"""
    import re
    user_input_lower = user_input.lower().strip()
    user_input_clean = user_input.strip()
    
    # Check if user provided information based on current step
    if conv_state.current_step == CollectionStep.GREETING:
        # Look for name in user input - be more specific about what constitutes a name
        if (len(user_input_clean) > 2 and 
            not any(word in user_input_lower for word in ['hello', 'hi', 'help', 'book', 'appointment', 'token', 'visit', 'hour']) and
            not user_input_clean.isdigit() and  # Not just numbers
            not re.match(r'^\d+$', user_input_clean)):  # Not just digits
            conv_state.set_user_info(name=user_input_clean)
            conv_state.update_step(CollectionStep.COLLECTING_AGE)
    
    elif conv_state.current_step == CollectionStep.COLLECTING_AGE:
        # Look for age in user input - more flexible age detection
        age_patterns = [
            r'\b(\d{1,3})\b',  # Basic number
            r'(\d{1,3})\s*(?:years?|yrs?|old)',  # "25 years", "30 yrs old"
            r'(?:age|i am|i\'m)\s*(\d{1,3})',  # "age 25", "i am 25"
        ]
        
        for pattern in age_patterns:
            age_match = re.search(pattern, user_input_lower)
            if age_match:
                try:
                    age = int(age_match.group(1))
                    if 0 <= age <= 150:
                        conv_state.set_user_info(age=age)
                        conv_state.update_step(CollectionStep.COLLECTING_PHONE)
                        break
                except ValueError:
                    continue
    
    elif conv_state.current_step == CollectionStep.COLLECTING_PHONE:
        # Look for phone number in user input - more flexible phone detection
        phone_patterns = [
            r'\b(\d{10,15})\b',  # Basic 10-15 digits
            r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # Formatted numbers
            r'(\+\d{1,3}[-.\s]?\d{10,15})',  # International format
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, user_input)
            if phone_match:
                phone = re.sub(r'[-.\s]', '', phone_match.group(1))  # Clean the number
                if len(phone) >= 10:
                    conv_state.set_user_info(phone=phone)
                    conv_state.update_step(CollectionStep.COLLECTING_DETAILS)
                    break
    
    elif conv_state.current_step == CollectionStep.COLLECTING_DETAILS:
        # Look for medical details in user input
        if len(user_input_clean) > 5:
            conv_state.set_user_info(details=user_input_clean)
            conv_state.update_step(CollectionStep.COMPLETED)