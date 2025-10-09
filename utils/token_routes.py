"""
Token Booking API Routes
FastAPI routes for token booking system
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel
from utils.token_booking import (
    TokenBookingManager, TokenBookingRequest, TokenBookingResponse,
    TokenUpdateRequest, TokenSearchRequest, TokenStatus, Department,
    token_manager
)

# Create router
router = APIRouter(prefix="/tokens", tags=["Token Booking"])

class SetCurrentTokenRequest(BaseModel):
    """Model for setting current token"""
    department: str
    doctor_name: str
    token_id: str

@router.post("/book", response_model=TokenBookingResponse)
async def book_token(request: TokenBookingRequest):
    """
    Book a new token for medical consultation
    
    Args:
        request: Token booking details including patient info, department, and timing
    
    Returns:
        TokenBookingResponse with booking confirmation or error message
    """
    try:
        result = token_manager.create_booking(request)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{token_id}", response_model=TokenBookingResponse)
async def get_token(token_id: str):
    """
    Get token booking details by token ID
    
    Args:
        token_id: Unique token identifier
    
    Returns:
        TokenBookingResponse with booking details
    """
    try:
        booking = token_manager.get_booking(token_id)
        
        if not booking:
            raise HTTPException(status_code=404, detail="Token booking not found")
        
        return TokenBookingResponse(
            success=True,
            message="Token booking retrieved successfully",
            token_id=token_id,
            token_number=booking.token_number,
            booking_details=booking
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{token_id}/status", response_model=TokenBookingResponse)
async def update_token_status(token_id: str, request: TokenUpdateRequest):
    """
    Update token booking status
    
    Args:
        token_id: Unique token identifier
        request: Status update request with new status and optional notes
    
    Returns:
        TokenBookingResponse with updated booking details
    """
    try:
        result = token_manager.update_booking(token_id, request)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/{token_id}", response_model=TokenBookingResponse)
async def cancel_token(token_id: str):
    """
    Cancel a token booking
    
    Args:
        token_id: Unique token identifier
    
    Returns:
        TokenBookingResponse confirming cancellation
    """
    try:
        result = token_manager.cancel_booking(token_id)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/search", response_model=List[dict])
async def search_tokens(
    patient_name: Optional[str] = Query(None, description="Patient name to search"),
    patient_phone: Optional[str] = Query(None, description="Patient phone number"),
    department: Optional[Department] = Query(None, description="Department filter"),
    booking_date: Optional[date] = Query(None, description="Booking date filter"),
    status: Optional[TokenStatus] = Query(None, description="Status filter"),
    token_number: Optional[int] = Query(None, description="Token number filter")
):
    """
    Search token bookings based on various criteria
    
    Args:
        patient_name: Filter by patient name (partial match)
        patient_phone: Filter by patient phone number
        department: Filter by department
        booking_date: Filter by booking date
        status: Filter by booking status
        token_number: Filter by token number
    
    Returns:
        List of matching token bookings
    """
    try:
        search_request = TokenSearchRequest(
            patient_name=patient_name,
            patient_phone=patient_phone,
            department=department,
            booking_date=booking_date,
            status=status,
            token_number=token_number
        )
        
        bookings = token_manager.search_bookings(search_request)
        
        # Convert to dict format for JSON response
        result = []
        for booking in bookings:
            booking_dict = booking.dict()
            booking_dict['created_at'] = booking.created_at.isoformat()
            booking_dict['updated_at'] = booking.updated_at.isoformat()
            booking_dict['booking_date'] = booking.booking_date.isoformat()
            booking_dict['booking_time'] = booking.booking_time.isoformat()
            result.append(booking_dict)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/daily/{date}", response_model=List[dict])
async def get_daily_bookings(
    date: date,
    department: Optional[Department] = Query(None, description="Filter by department")
):
    """
    Get all token bookings for a specific date
    
    Args:
        date: Date to get bookings for
        department: Optional department filter
    
    Returns:
        List of token bookings for the specified date
    """
    try:
        bookings = token_manager.get_daily_bookings(date, department)
        
        # Convert to dict format for JSON response
        result = []
        for booking in bookings:
            booking_dict = booking.dict()
            booking_dict['created_at'] = booking.created_at.isoformat()
            booking_dict['updated_at'] = booking.updated_at.isoformat()
            booking_dict['booking_date'] = booking.booking_date.isoformat()
            booking_dict['booking_time'] = booking.booking_time.isoformat()
            result.append(booking_dict)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/stats", response_model=dict)
async def get_booking_stats():
    """
    Get token booking statistics
    
    Returns:
        Dictionary with booking statistics including counts by status and department
    """
    try:
        stats = token_manager.get_booking_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/departments", response_model=List[dict])
async def get_departments():
    """
    Get list of available departments
    
    Returns:
        List of departments with their details
    """
    departments = [
        {"value": dept.value, "name": dept.value.replace("_", " ").title()}
        for dept in Department
    ]
    return departments

@router.get("/statuses", response_model=List[dict])
async def get_statuses():
    """
    Get list of available token statuses
    
    Returns:
        List of statuses with their details
    """
    statuses = [
        {"value": status.value, "name": status.value.replace("_", " ").title()}
        for status in TokenStatus
    ]
    return statuses


@router.post("/current/set")
async def set_current_token_route(request: SetCurrentTokenRequest):
    """
    API endpoint to set which token a doctor is currently serving
    
    Example usage:
    POST /tokens/current/set
    {
        "department": "cardiology",
        "doctor_name": "Dr. Sharma",
        "token_id": "abc-123"
    }
    """
    try:
        result = token_manager.set_current_token(
            request.department, 
            request.doctor_name, 
            request.token_id
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['message'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/current/{doctor_name}")
async def get_current_token_route(doctor_name: str):
    """
    API endpoint to get which token a doctor is currently serving
    
    Example usage:
    GET /tokens/current/Dr.%20Sharma
    (Note: spaces in URL should be encoded as %20)
    """
    try:
        current_info = token_manager.get_current_token(doctor_name)
        
        if not current_info:
            return {
                "success": False,
                "message": f"No current token information for Dr. {doctor_name}",
                "current_token": None
            }
        
        return {
            "success": True,
            "message": "Current token retrieved successfully",
            "current_token": current_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")