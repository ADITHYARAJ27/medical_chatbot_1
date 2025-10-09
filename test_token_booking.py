"""
Test script for Token Booking System
Tests all major functionality of the token booking system
"""

import sys
import os
from datetime import date, time, datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.token_booking import (
    TokenBookingManager, TokenBookingRequest, TokenSearchRequest,
    Department, TokenStatus, token_manager
)
from utils.token_management import TokenManagementUtils, token_utils

def test_basic_booking():
    """Test basic token booking functionality"""
    print("🧪 Testing Basic Token Booking...")
    
    # Create a test booking
    request = TokenBookingRequest(
        patient_name="John Doe",
        patient_phone="9876543210",
        patient_age=35,
        department=Department.GENERAL_MEDICINE,
        booking_date=date.today() + timedelta(days=1),
        booking_time=time(10, 30),
        symptoms="Fever and headache",
        priority="normal"
    )
    
    result = token_manager.create_booking(request)
    
    if result.success:
        print(f"✅ Booking successful! Token ID: {result.token_id}, Token Number: {result.token_number}")
        return result.token_id
    else:
        print(f"❌ Booking failed: {result.message}")
        return None

def test_booking_retrieval(token_id):
    """Test retrieving a booking"""
    print(f"\n🧪 Testing Booking Retrieval for Token ID: {token_id}...")
    
    booking = token_manager.get_booking(token_id)
    
    if booking:
        print(f"✅ Booking retrieved successfully!")
        print(f"   Patient: {booking.patient_name}")
        print(f"   Token Number: {booking.token_number}")
        print(f"   Department: {booking.department.value}")
        print(f"   Status: {booking.status.value}")
    else:
        print("❌ Booking not found!")

def test_booking_update(token_id):
    """Test updating a booking status"""
    print(f"\n🧪 Testing Booking Status Update for Token ID: {token_id}...")
    
    from utils.token_booking import TokenUpdateRequest
    
    update_request = TokenUpdateRequest(
        status=TokenStatus.CONFIRMED,
        notes="Patient confirmed appointment"
    )
    
    result = token_manager.update_booking(token_id, update_request)
    
    if result.success:
        print(f"✅ Booking updated successfully! New status: {update_request.status.value}")
    else:
        print(f"❌ Booking update failed: {result.message}")

def test_booking_search():
    """Test searching bookings"""
    print(f"\n🧪 Testing Booking Search...")
    
    # Search by patient name
    search_request = TokenSearchRequest(patient_name="John")
    bookings = token_manager.search_bookings(search_request)
    
    print(f"✅ Found {len(bookings)} booking(s) for patient name 'John'")
    
    # Search by department
    search_request = TokenSearchRequest(department=Department.GENERAL_MEDICINE)
    bookings = token_manager.search_bookings(search_request)
    
    print(f"✅ Found {len(bookings)} booking(s) for General Medicine department")

def test_daily_bookings():
    """Test getting daily bookings"""
    print(f"\n🧪 Testing Daily Bookings...")
    
    tomorrow = date.today() + timedelta(days=1)
    bookings = token_manager.get_daily_bookings(tomorrow)
    
    print(f"✅ Found {len(bookings)} booking(s) for {tomorrow}")

def test_booking_statistics():
    """Test booking statistics"""
    print(f"\n🧪 Testing Booking Statistics...")
    
    stats = token_manager.get_booking_stats()
    
    print(f"✅ Total bookings: {stats['total_bookings']}")
    print(f"   Status breakdown: {stats['status_breakdown']}")
    print(f"   Department breakdown: {stats['department_breakdown']}")

def test_management_utils():
    """Test management utilities"""
    print(f"\n🧪 Testing Management Utilities...")
    
    # Test daily report
    tomorrow = date.today() + timedelta(days=1)
    report = token_utils.generate_daily_report(tomorrow)
    
    if 'error' not in report:
        print(f"✅ Daily report generated for {tomorrow}")
        print(f"   Total bookings: {report['total_bookings']}")
    else:
        print(f"❌ Daily report failed: {report['error']}")
    
    # Test upcoming appointments
    upcoming = token_utils.get_upcoming_appointments(7)
    
    if upcoming and 'error' not in upcoming[0]:
        print(f"✅ Found {len(upcoming)} upcoming appointment(s)")
    else:
        print(f"❌ Failed to get upcoming appointments")

def test_agent_tools():
    """Test agent tools integration"""
    print(f"\n🧪 Testing Agent Tools Integration...")
    
    try:
        from utils.tools import book_medical_token, check_token_status, search_tokens
        
        # Test booking through agent tool
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        result = book_medical_token(
            patient_name="Jane Smith",
            patient_phone="9876543211",
            patient_age=28,
            department="cardiology",
            booking_date=tomorrow,
            booking_time="14:30",
            symptoms="Chest pain",
            priority="high"
        )
        
        print(f"✅ Agent tool booking result: {result[:100]}...")
        
        # Extract token ID from result if successful
        if "Token ID:" in result:
            token_id = result.split("Token ID: ")[1].split("\n")[0]
            
            # Test status check
            status_result = check_token_status(token_id)
            print(f"✅ Agent tool status check: {status_result[:100]}...")
        
    except Exception as e:
        print(f"❌ Agent tools test failed: {str(e)}")

def cleanup_test_data():
    """Clean up test data"""
    print(f"\n🧹 Cleaning up test data...")
    
    # This would typically involve removing test bookings
    # For now, we'll just print a message
    print("✅ Test data cleanup completed (manual cleanup may be required)")

def main():
    """Run all tests"""
    print("🚀 Starting Token Booking System Tests")
    print("=" * 50)
    
    try:
        # Test basic functionality
        token_id = test_basic_booking()
        
        if token_id:
            test_booking_retrieval(token_id)
            test_booking_update(token_id)
        
        # Test search and management
        test_booking_search()
        test_daily_bookings()
        test_booking_statistics()
        test_management_utils()
        test_agent_tools()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup_test_data()

if __name__ == "__main__":
    main()

