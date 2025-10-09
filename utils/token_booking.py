"""
Token Booking System for Medical Assistant
Handles appointment token booking, management, and tracking
"""

from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import json
import os
from uuid import uuid4

class TokenStatus(str, Enum):
    """Token status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class Department(str, Enum):
    """Hospital departments"""
    GENERAL_MEDICINE = "general_medicine"
    CARDIOLOGY = "cardiology"
    PEDIATRICS = "pediatrics"
    GYNECOLOGY = "gynecology"
    ORTHOPEDICS = "orthopedics"
    EMERGENCY = "emergency"
    DENTAL = "dental"
    DERMATOLOGY = "dermatology"
    PSYCHIATRY = "psychiatry"

class TokenBooking(BaseModel):
    """Token booking model"""
    token_id: str = Field(default_factory=lambda: str(uuid4()))
    patient_name: str = Field(..., min_length=2, max_length=100)
    patient_phone: str = Field(..., min_length=10, max_length=15)
    patient_age: int = Field(..., ge=0, le=150)
    department: Department
    doctor_name: Optional[str] = None
    booking_date: date
    booking_time: time
    token_number: int
    status: TokenStatus = TokenStatus.PENDING
    symptoms: Optional[str] = None
    priority: str = Field(default="normal", pattern="^(low|normal|high|emergency)$")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

class TokenBookingRequest(BaseModel):
    """Request model for creating a token booking"""
    patient_name: str = Field(..., min_length=2, max_length=100)
    patient_phone: str = Field(..., min_length=10, max_length=15)
    patient_age: int = Field(..., ge=0, le=150)
    department: Department
    doctor_name: Optional[str] = None
    booking_date: date
    booking_time: time
    symptoms: Optional[str] = None
    priority: str = Field(default="normal", pattern="^(low|normal|high|emergency)$")
    notes: Optional[str] = None

class TokenBookingResponse(BaseModel):
    """Response model for token booking operations"""
    success: bool
    message: str
    token_id: Optional[str] = None
    token_number: Optional[int] = None
    booking_details: Optional[TokenBooking] = None

class TokenUpdateRequest(BaseModel):
    """Request model for updating token status"""
    status: TokenStatus
    notes: Optional[str] = None

class TokenSearchRequest(BaseModel):
    """Request model for searching tokens"""
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    department: Optional[Department] = None
    booking_date: Optional[date] = None
    status: Optional[TokenStatus] = None
    token_number: Optional[int] = None

class TokenBookingManager:
    """Manages token bookings with file-based storage"""
    
    def __init__(self, data_file: str = "utils/data/token_bookings.json"):
        self.data_file = data_file
        self.current_tokens_file = "utils/data/current_tokens.json"  # NEW: file to store current tokens
        self.bookings: Dict[str, TokenBooking] = {}
        self.current_tokens: Dict[str, Dict] = {}  # NEW: store current tokens in memory
        self._load_bookings()
        self._load_current_tokens()  # NEW: load current tokens when starting
    
    def _load_bookings(self):
        """Load bookings from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for token_id, booking_data in data.items():
                        # Convert datetime strings back to datetime objects
                        booking_data['created_at'] = datetime.fromisoformat(booking_data['created_at'])
                        booking_data['updated_at'] = datetime.fromisoformat(booking_data['updated_at'])
                        booking_data['booking_date'] = date.fromisoformat(booking_data['booking_date'])
                        booking_data['booking_time'] = time.fromisoformat(booking_data['booking_time'])
                        self.bookings[token_id] = TokenBooking(**booking_data)
        except Exception as e:
            print(f"Error loading bookings: {e}")
            self.bookings = {}
    
    def _save_bookings(self):
        """Save bookings to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Convert to serializable format
            data = {}
            for token_id, booking in self.bookings.items():
                booking_dict = booking.dict()
                booking_dict['created_at'] = booking.created_at.isoformat()
                booking_dict['updated_at'] = booking.updated_at.isoformat()
                booking_dict['booking_date'] = booking.booking_date.isoformat()
                booking_dict['booking_time'] = booking.booking_time.isoformat()
                data[token_id] = booking_dict
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving bookings: {e}")
    
    def get_next_token_number(self, department: Department, booking_date: date) -> int:
        """Get the next available token number for a department on a specific date"""
        same_day_bookings = [
            booking for booking in self.bookings.values()
            if booking.department == department and booking.booking_date == booking_date
        ]
        
        if not same_day_bookings:
            return 1
        
        max_token = max(booking.token_number for booking in same_day_bookings)
        return max_token + 1
    
    def create_booking(self, request: TokenBookingRequest) -> TokenBookingResponse:
        """Create a new token booking"""
        try:
            # Check for conflicts
            conflicting_bookings = [
                booking for booking in self.bookings.values()
                if (booking.patient_phone == request.patient_phone and 
                    booking.booking_date == request.booking_date and
                    booking.status in [TokenStatus.PENDING, TokenStatus.CONFIRMED])
            ]
            
            if conflicting_bookings:
                return TokenBookingResponse(
                    success=False,
                    message=f"Patient already has a booking for {request.booking_date}. Please choose a different date or cancel existing booking."
                )
            
            # Get next token number
            token_number = self.get_next_token_number(request.department, request.booking_date)
            
            # Create booking
            booking = TokenBooking(
                patient_name=request.patient_name,
                patient_phone=request.patient_phone,
                patient_age=request.patient_age,
                department=request.department,
                doctor_name=request.doctor_name,
                booking_date=request.booking_date,
                booking_time=request.booking_time,
                token_number=token_number,
                symptoms=request.symptoms,
                priority=request.priority,
                notes=request.notes
            )
            
            self.bookings[booking.token_id] = booking
            self._save_bookings()
            
            return TokenBookingResponse(
                success=True,
                message=f"Token booking successful! Your token number is {token_number}",
                token_id=booking.token_id,
                token_number=token_number,
                booking_details=booking
            )
            
        except Exception as e:
            return TokenBookingResponse(
                success=False,
                message=f"Error creating booking: {str(e)}"
            )
    
    def get_booking(self, token_id: str) -> Optional[TokenBooking]:
        """Get a specific booking by token ID"""
        return self.bookings.get(token_id)
    
    def update_booking(self, token_id: str, request: TokenUpdateRequest) -> TokenBookingResponse:
        """Update a booking status"""
        try:
            if token_id not in self.bookings:
                return TokenBookingResponse(
                    success=False,
                    message="Token booking not found"
                )
            
            booking = self.bookings[token_id]
            booking.status = request.status
            booking.updated_at = datetime.now()
            if request.notes:
                booking.notes = request.notes
            
            self._save_bookings()
            
            return TokenBookingResponse(
                success=True,
                message=f"Token status updated to {request.status}",
                token_id=token_id,
                booking_details=booking
            )
            
        except Exception as e:
            return TokenBookingResponse(
                success=False,
                message=f"Error updating booking: {str(e)}"
            )
    
    def search_bookings(self, request: TokenSearchRequest) -> List[TokenBooking]:
        """Search bookings based on criteria"""
        results = list(self.bookings.values())
        
        if request.patient_name:
            results = [b for b in results if request.patient_name.lower() in b.patient_name.lower()]
        
        if request.patient_phone:
            results = [b for b in results if request.patient_phone in b.patient_phone]
        
        if request.department:
            results = [b for b in results if b.department == request.department]
        
        if request.booking_date:
            results = [b for b in results if b.booking_date == request.booking_date]
        
        if request.status:
            results = [b for b in results if b.status == request.status]
        
        if request.token_number:
            results = [b for b in results if b.token_number == request.token_number]
        
        return sorted(results, key=lambda x: (x.booking_date, x.booking_time))
    
    def get_daily_bookings(self, date: date, department: Optional[Department] = None) -> List[TokenBooking]:
        """Get all bookings for a specific date"""
        results = [booking for booking in self.bookings.values() if booking.booking_date == date]
        
        if department:
            results = [booking for booking in results if booking.department == department]
        
        return sorted(results, key=lambda x: (x.booking_time, x.token_number))
    
    def cancel_booking(self, token_id: str) -> TokenBookingResponse:
        """Cancel a booking"""
        return self.update_booking(token_id, TokenUpdateRequest(status=TokenStatus.CANCELLED))
    
    def get_booking_stats(self) -> Dict[str, Any]:
        """Get booking statistics"""
        total_bookings = len(self.bookings)
        status_counts = {}
        department_counts = {}
        
        for booking in self.bookings.values():
            # Count by status
            status_counts[booking.status] = status_counts.get(booking.status, 0) + 1
            
            # Count by department
            department_counts[booking.department] = department_counts.get(booking.department, 0) + 1
        
        return {
            "total_bookings": total_bookings,
            "status_breakdown": status_counts,
            "department_breakdown": department_counts
        }



    def _load_current_tokens(self):
        """Load which tokens are currently being served"""
        try:
            if os.path.exists(self.current_tokens_file):
                with open(self.current_tokens_file, 'r', encoding='utf-8') as f:
                    self.current_tokens = json.load(f)
                print(f"✅ Loaded current tokens from file")
            else:
                self.current_tokens = {}
                print("📝 No current tokens file found, starting fresh")
        except Exception as e:
            print(f"⚠️ Error loading current tokens: {e}")
            self.current_tokens = {}
    
    def _save_current_tokens(self):
        """Save which tokens are currently being served"""
        try:
            os.makedirs(os.path.dirname(self.current_tokens_file), exist_ok=True)
            with open(self.current_tokens_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_tokens, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved current tokens to file")
        except Exception as e:
            print(f"⚠️ Error saving current tokens: {e}")


    def set_current_token(self, department: str, doctor_name: str, token_id: str):
        """
        Mark a token as currently being served by a doctor
        
        Example: set_current_token("cardiology", "Dr. Sharma", "abc-123")
        """
        try:
            # Check if this token exists
            booking = self.get_booking(token_id)
            if not booking:
                return {
                    "success": False, 
                    "message": f"Token {token_id} not found"
                }
            
            # Check if department matches
            if booking.department.value != department.lower():
                return {
                    "success": False,
                    "message": f"This token is for {booking.department.value}, not {department}"
                }
            
            # Create a unique key for this doctor
            # Example: "cardiology_dr. sharma"
            key = f"{department.lower()}_{doctor_name.lower()}"
            
            # Store the current token
            self.current_tokens[key] = {
                "department": department,
                "doctor_name": doctor_name,
                "current_token_id": token_id,
                "current_token_number": booking.token_number,
                "patient_name": booking.patient_name,
                "updated_at": datetime.now().isoformat()
            }
            
            # Save to file
            self._save_current_tokens()
            
            print(f"✅ Set current token: Dr. {doctor_name} is now on Token #{booking.token_number}")
            
            return {
                "success": True,
                "message": f"Dr. {doctor_name} is now serving Token #{booking.token_number}",
                "token_number": booking.token_number
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    def get_current_token(self, doctor_name: str):
        """
        Get which token a doctor is currently serving
        
        Example: get_current_token("Dr. Sharma")
        Returns: {"token_number": 5, "patient_name": "John Doe", ...}
        """
        try:
            # Search through all current tokens for this doctor
            for key, info in self.current_tokens.items():
                if info['doctor_name'].lower() == doctor_name.lower():
                    # Found it! Return the info
                    return info
            
            # Not found
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting current token: {e}")
            return None

# Global instance
token_manager = TokenBookingManager()
