#!/usr/bin/env python3
"""
Test script for the sequential information collection flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import create_agent, run_agent
from utils.conversation_state import conversation_manager, CollectionStep

def test_sequential_flow():
    """Test the sequential information collection flow"""
    print("🧪 Testing Sequential Information Collection Flow")
    print("=" * 60)
    
    # Create agent
    agent_executor = create_agent()
    thread_id = "test_sequential_flow"
    
    # Test conversation flow
    test_messages = [
        "Hello",
        "John Doe",
        "25",
        "9876543210",
        "I have a fever and cough for 3 days"
    ]
    
    print(f"Thread ID: {thread_id}")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"👤 User {i}: {message}")
        
        # Get response from agent
        response = run_agent(agent_executor, message, thread_id)
        print(f"🤖 Assistant: {response}")
        
        # Check conversation state
        conv_state = conversation_manager.get_state(thread_id)
        print(f"📊 State: {conv_state.current_step.value}")
        print(f"📋 Collected: Name={conv_state.user_info.name}, Age={conv_state.user_info.age}, Phone={conv_state.user_info.phone}, Details={conv_state.user_info.details}")
        print("-" * 40)
        print()
    
    # Final state check
    final_state = conversation_manager.get_state(thread_id)
    print("🎯 Final State Summary:")
    print(f"   Step: {final_state.current_step.value}")
    print(f"   Complete: {final_state.is_info_complete()}")
    print(f"   Missing: {final_state.get_missing_fields()}")
    print()
    
    if final_state.is_info_complete():
        print("✅ SUCCESS: All information collected successfully!")
        print(f"   Name: {final_state.user_info.name}")
        print(f"   Age: {final_state.user_info.age}")
        print(f"   Phone: {final_state.user_info.phone}")
        print(f"   Details: {final_state.user_info.details}")
    else:
        print("❌ FAILED: Information collection incomplete")
        print(f"   Missing fields: {final_state.get_missing_fields()}")

if __name__ == "__main__":
    test_sequential_flow()


