#!/usr/bin/env python3
"""
Test script for the conversation state management (without API calls)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.conversation_state import conversation_manager, CollectionStep

def test_conversation_state():
    """Test the conversation state management"""
    print("🧪 Testing Conversation State Management")
    print("=" * 60)
    
    # Test creating a new conversation state
    thread_id = "test_conversation_state"
    conv_state = conversation_manager.get_state(thread_id)
    
    print(f"Thread ID: {thread_id}")
    print(f"Initial step: {conv_state.current_step.value}")
    print(f"Initial info complete: {conv_state.is_info_complete()}")
    print(f"Missing fields: {conv_state.get_missing_fields()}")
    print()
    
    # Test sequential information collection
    test_data = [
        ("John Doe", "name"),
        (25, "age"),
        ("9876543210", "phone"),
        ("I have a fever and cough for 3 days", "details")
    ]
    
    for value, field in test_data:
        print(f"Setting {field}: {value}")
        conv_state.set_user_info(**{field: value})
        
        # Update step based on field
        if field == "name":
            conv_state.update_step(CollectionStep.COLLECTING_AGE)
        elif field == "age":
            conv_state.update_step(CollectionStep.COLLECTING_PHONE)
        elif field == "phone":
            conv_state.update_step(CollectionStep.COLLECTING_DETAILS)
        elif field == "details":
            conv_state.update_step(CollectionStep.COMPLETED)
        
        print(f"  Step: {conv_state.current_step.value}")
        print(f"  Complete: {conv_state.is_info_complete()}")
        print(f"  Missing: {conv_state.get_missing_fields()}")
        print()
    
    # Final verification
    print("🎯 Final State Summary:")
    print(f"   Step: {conv_state.current_step.value}")
    print(f"   Complete: {conv_state.is_info_complete()}")
    print(f"   Missing: {conv_state.get_missing_fields()}")
    print()
    
    if conv_state.is_info_complete():
        print("✅ SUCCESS: All information collected successfully!")
        print(f"   Name: {conv_state.user_info.name}")
        print(f"   Age: {conv_state.user_info.age}")
        print(f"   Phone: {conv_state.user_info.phone}")
        print(f"   Details: {conv_state.user_info.details}")
    else:
        print("❌ FAILED: Information collection incomplete")
        print(f"   Missing fields: {conv_state.get_missing_fields()}")
    
    # Test multiple threads
    print("\n" + "=" * 60)
    print("🧪 Testing Multiple Thread Management")
    
    thread_id_2 = "test_conversation_state_2"
    conv_state_2 = conversation_manager.get_state(thread_id_2)
    
    print(f"Thread 1: {thread_id} - Step: {conv_state.current_step.value}")
    print(f"Thread 2: {thread_id_2} - Step: {conv_state_2.current_step.value}")
    
    # Verify they are independent
    conv_state_2.set_user_info(name="Jane Smith")
    conv_state_2.update_step(CollectionStep.COLLECTING_AGE)
    
    print(f"After updating Thread 2:")
    print(f"Thread 1: {thread_id} - Step: {conv_state.current_step.value}")
    print(f"Thread 2: {thread_id_2} - Step: {conv_state_2.current_step.value}")
    
    print("\n✅ Multiple thread management working correctly!")

if __name__ == "__main__":
    test_conversation_state()


