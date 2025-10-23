#!/usr/bin/env python3
"""
Simple demonstration of the sequential information collection flow
This script shows how the conversation flow works step by step
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.conversation_state import conversation_manager, CollectionStep
import re

def update_conversation_state_simple(conv_state, user_input: str):
    """Simplified version of update_conversation_state for demonstration"""
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
            return True
    
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
                        return True
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
                    return True
    
    elif conv_state.current_step == CollectionStep.COLLECTING_DETAILS:
        # Look for medical details in user input
        if len(user_input_clean) > 5:
            conv_state.set_user_info(details=user_input_clean)
            conv_state.update_step(CollectionStep.COMPLETED)
            return True
    
    return False

def simulate_conversation():
    """Simulate a conversation with the medical assistant"""
    print("🏥 Medical Assistant - Sequential Information Collection Demo")
    print("=" * 70)
    print("📍 Community Health Center Harichandanpur, Keonjhar, Odisha")
    print("👨‍⚕️ Under guidance of Dr. Harshin")
    print()
    
    # Initialize conversation
    thread_id = "demo_conversation"
    conversation_manager.reset_state(thread_id)
    state = conversation_manager.get_state(thread_id)
    
    print("🤖 Assistant: Hello! I'm your medical assistant. To help you better, may I please have your full name?")
    print()
    
    # Simulate user responses
    user_responses = [
        {
            "input": "John Doe",
            "expected_step": CollectionStep.COLLECTING_AGE,
            "assistant_response": "Thank you! What is your age?"
        },
        {
            "input": "25",
            "expected_step": CollectionStep.COLLECTING_PHONE,
            "assistant_response": "Great! What is your phone number?"
        },
        {
            "input": "9876543210",
            "expected_step": CollectionStep.COLLECTING_DETAILS,
            "assistant_response": "Perfect! Please tell me about your medical concerns or symptoms."
        },
        {
            "input": "I have a headache and fever for the past 2 days",
            "expected_step": CollectionStep.COMPLETED,
            "assistant_response": "Thank you for providing all the information. I can now help you with booking an appointment or other services."
        }
    ]
    
    for i, response_data in enumerate(user_responses, 1):
        print(f"👤 User: {response_data['input']}")
        
        # Update conversation state
        success = update_conversation_state_simple(state, response_data['input'])
        
        # Get updated state
        state = conversation_manager.get_state(thread_id)
        
        print(f"🤖 Assistant: {response_data['assistant_response']}")
        print(f"📊 Current step: {state.current_step.value}")
        print(f"📋 Collected info: Name={state.user_info.name}, Age={state.user_info.age}, Phone={state.user_info.phone}")
        print(f"✅ Step transition successful: {state.current_step == response_data['expected_step']}")
        print(f"🔄 State updated: {success}")
        print()
    
    # Final summary
    print("🎉 Conversation Complete!")
    print("=" * 50)
    print(f"Final state: {state.current_step.value}")
    print(f"All information collected: {state.is_info_complete()}")
    print(f"Missing fields: {state.get_missing_fields()}")
    print()
    print("📋 Complete User Information:")
    print(f"  👤 Name: {state.user_info.name}")
    print(f"  🎂 Age: {state.user_info.age}")
    print(f"  📞 Phone: {state.user_info.phone}")
    print(f"  🏥 Medical Details: {state.user_info.details}")
    print(f"  📅 Collected at: {state.user_info.collected_at}")

def demonstrate_edge_cases():
    """Demonstrate how the system handles edge cases"""
    print("\n🧪 Edge Case Demonstrations")
    print("=" * 40)
    
    edge_cases = [
        {
            "description": "Invalid age input",
            "input": "not a number",
            "expected": "Should ask for age again"
        },
        {
            "description": "Short phone number",
            "input": "123",
            "expected": "Should ask for phone again"
        },
        {
            "description": "Empty response",
            "input": "",
            "expected": "Should handle gracefully"
        }
    ]
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\n--- Edge Case {i}: {case['description']} ---")
        print(f"Input: '{case['input']}'")
        print(f"Expected: {case['expected']}")
        
        # Create a new thread for each edge case
        thread_id = f"edge_case_{i}"
        conversation_manager.reset_state(thread_id)
        state = conversation_manager.get_state(thread_id)
        
        # Simulate the edge case
        success = update_conversation_state_simple(state, case['input'])
        
        print(f"State after input: {state.current_step.value}")
        print(f"Information collected: {state.user_info}")
        print(f"State updated: {success}")

def show_sequential_flow_benefits():
    """Show the benefits of the sequential flow"""
    print("\n✨ Benefits of Sequential Information Collection")
    print("=" * 50)
    
    benefits = [
        "🎯 **Focused Interaction**: Users provide one piece of information at a time",
        "🧠 **Reduced Cognitive Load**: No overwhelming forms or long questionnaires",
        "📱 **Mobile Friendly**: Perfect for mobile devices and small screens",
        "🔄 **Natural Flow**: Mimics human conversation patterns",
        "✅ **Validation**: Each input is validated before moving to the next step",
        "🛡️ **Error Handling**: Invalid inputs don't break the entire flow",
        "📊 **Progress Tracking**: Users know exactly what information is still needed",
        "🎨 **User Experience**: Clean, simple, and intuitive interface"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n🔄 Sequential Flow Steps:")
    steps = [
        "1. 👤 Ask for Full Name",
        "2. 🎂 Ask for Age (in years)",
        "3. 📞 Ask for Phone Number",
        "4. 🏥 Ask for Medical Details/Symptoms",
        "5. ✅ Complete - Ready for booking or other services"
    ]
    
    for step in steps:
        print(f"  {step}")

if __name__ == "__main__":
    try:
        simulate_conversation()
        demonstrate_edge_cases()
        show_sequential_flow_benefits()
        print("\n🎉 Sequential Flow Demonstration Complete!")
        print("\nTo use this in the actual application:")
        print("1. Run: python start_sequential_ui.py")
        print("2. Open: http://localhost:5000")
        print("3. Start chatting with the medical assistant!")
    except Exception as e:
        print(f"\n❌ Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()
