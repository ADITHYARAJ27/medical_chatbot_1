#!/usr/bin/env python3
"""
Simple test for conversation state management without requiring API keys
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.conversation_state import conversation_manager, CollectionStep, ConversationState
from datetime import datetime

def test_conversation_state():
    """Test the conversation state management logic"""
    print("🧪 Testing Conversation State Management")
    print("=" * 50)
    
    # Test 1: Create new conversation state
    print("\n1. Testing new conversation state creation...")
    thread_id = "test_thread_1"
    state = conversation_manager.get_state(thread_id)
    
    print(f"Initial step: {state.current_step.value}")
    print(f"Thread ID: {state.thread_id}")
    print(f"User info: {state.user_info}")
    print(f"Is info complete: {state.is_info_complete()}")
    print(f"Missing fields: {state.get_missing_fields()}")
    
    # Test 2: Update state step by step
    print("\n2. Testing step-by-step state updates...")
    
    # Step 1: Collect name
    print("\n--- Step 1: Collecting Name ---")
    state = conversation_manager.update_state(thread_id, name="John Doe", current_step=CollectionStep.COLLECTING_AGE)
    print(f"Updated step: {state.current_step.value}")
    print(f"Name collected: {state.user_info.name}")
    print(f"Missing fields: {state.get_missing_fields()}")
    
    # Step 2: Collect age
    print("\n--- Step 2: Collecting Age ---")
    state = conversation_manager.update_state(thread_id, age=25, current_step=CollectionStep.COLLECTING_PHONE)
    print(f"Updated step: {state.current_step.value}")
    print(f"Age collected: {state.user_info.age}")
    print(f"Missing fields: {state.get_missing_fields()}")
    
    # Step 3: Collect phone
    print("\n--- Step 3: Collecting Phone ---")
    state = conversation_manager.update_state(thread_id, phone="9876543210", current_step=CollectionStep.COLLECTING_DETAILS)
    print(f"Updated step: {state.current_step.value}")
    print(f"Phone collected: {state.user_info.phone}")
    print(f"Missing fields: {state.get_missing_fields()}")
    
    # Step 4: Collect details
    print("\n--- Step 4: Collecting Details ---")
    state = conversation_manager.update_state(thread_id, details="I have a headache and fever", current_step=CollectionStep.COMPLETED)
    print(f"Updated step: {state.current_step.value}")
    print(f"Details collected: {state.user_info.details}")
    print(f"Missing fields: {state.get_missing_fields()}")
    print(f"Is info complete: {state.is_info_complete()}")
    
    # Test 3: Test state validation
    print("\n3. Testing state validation...")
    print(f"Final state: {state.current_step.value}")
    print(f"All information collected: {state.is_info_complete()}")
    
    if state.is_info_complete():
        print("✅ All required information has been collected!")
        print(f"Complete user info: {state.user_info}")
    else:
        print("❌ Information collection is incomplete")
        print(f"Missing: {state.get_missing_fields()}")
    
    # Test 4: Test multiple threads
    print("\n4. Testing multiple conversation threads...")
    thread_id_2 = "test_thread_2"
    state_2 = conversation_manager.get_state(thread_id_2)
    print(f"Thread 2 initial step: {state_2.current_step.value}")
    print(f"Thread 1 still exists: {thread_id in conversation_manager.states}")
    print(f"Thread 2 exists: {thread_id_2 in conversation_manager.states}")
    
    # Test 5: Test state reset
    print("\n5. Testing state reset...")
    conversation_manager.reset_state(thread_id)
    reset_state = conversation_manager.get_state(thread_id)
    print(f"Reset state step: {reset_state.current_step.value}")
    print(f"Reset user info: {reset_state.user_info}")
    print(f"Is info complete after reset: {reset_state.is_info_complete()}")
    
    print("\n🎉 Conversation state management test completed!")

def test_state_transitions():
    """Test the state transition logic"""
    print("\n🧪 Testing State Transitions")
    print("=" * 40)
    
    thread_id = "test_transitions"
    conversation_manager.reset_state(thread_id)
    
    # Test valid transitions
    transitions = [
        (CollectionStep.GREETING, CollectionStep.COLLECTING_NAME, "name", "John Doe"),
        (CollectionStep.COLLECTING_NAME, CollectionStep.COLLECTING_AGE, "age", 25),
        (CollectionStep.COLLECTING_AGE, CollectionStep.COLLECTING_PHONE, "phone", "9876543210"),
        (CollectionStep.COLLECTING_PHONE, CollectionStep.COLLECTING_DETAILS, "details", "I have a headache"),
        (CollectionStep.COLLECTING_DETAILS, CollectionStep.COMPLETED, None, None)
    ]
    
    for i, (from_step, to_step, field, value) in enumerate(transitions, 1):
        print(f"\n--- Transition {i}: {from_step.value} → {to_step.value} ---")
        
        # Set the current step
        state = conversation_manager.update_state(thread_id, current_step=from_step)
        print(f"Current step: {state.current_step.value}")
        
        # Update with field value if provided
        if field and value:
            update_data = {field: value, 'current_step': to_step}
            state = conversation_manager.update_state(thread_id, **update_data)
            print(f"Updated {field}: {getattr(state.user_info, field)}")
        
        print(f"New step: {state.current_step.value}")
        print(f"Missing fields: {state.get_missing_fields()}")
    
    print("\n✅ State transition test completed!")

if __name__ == "__main__":
    print("🏥 Medical Chatbot Conversation State Test")
    print("📍 Community Health Center Harichandanpur")
    print("👨‍⚕️ Under guidance of Dr. Harshin")
    print()
    
    try:
        test_conversation_state()
        test_state_transitions()
        print("\n✅ All conversation state tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
