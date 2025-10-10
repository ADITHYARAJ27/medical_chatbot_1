from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime, date, time
import os
from utils.token_booking import (
    TokenBookingManager, TokenBookingRequest, TokenSearchRequest,
    Department, TokenStatus, token_manager
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_pdf_content(pdf_path: str) -> str:
    """Load and extract text content from PDF file"""
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")
        
        # Load PDF using PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Combine all pages into one text
        full_text = ""
        for doc in documents:
            full_text += doc.page_content + "\n"
        
        return full_text
    
    except Exception as e:
        print(f"Error loading PDF: {str(e)}")
        # Fallback to hardcoded content if PDF loading fails
        return get_fallback_content()

def get_fallback_content() -> str:
    """Fallback content in case PDF loading fails"""
    return """
    HOSPITAL WIDE POLICIES - Community Health Center Harichandanpur, Keonjhar, Odisha
    
    VISITOR'S POLICY:
    Objective: To make sure that our patients get the rest they need and other patients are not disturbed.
    
    Policy:
    1. Visitors must be age of 12 years or above
    2. Siblings will be allowed to visit the maternity units as long as they do not exhibit symptoms of cold or other respiratory infection
    3. Request to visit in compassionate care situation may be approved by the nursing sister
    
    Visiting Hours:
    General Visiting Hours:
    - Before and after the round of doctor
    - Please limit your stay to 15-20 minutes
    - Maximum no. of visitors in the rooms are 02 at a time
    - Children under the age of 12 are not permitted in wards nor may they wait in the waiting area
    - A care giver may interrupt your visit during patients care routine
    - If you are unfit please postpone your visit
    
    For complete hospital policies, please ensure the PDF file is available at utils/hospital.pdf
    """

def setup_vector_store():
    """Setup in-memory vector store with hospital policies from PDF"""
    
    # Define PDF path
    pdf_path = os.path.join("utils/data", "hospital_policies.pdf")
    
    # Load content from PDF
    hospital_policies_content = load_pdf_content(pdf_path)
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    texts = text_splitter.split_text(hospital_policies_content)
    
    # Create in-memory vector store
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_texts(texts)
    
    return vector_store

# Initialize vector store
try:
    vector_store = setup_vector_store()
    print("Vector store initialized successfully with PDF content")
except Exception as e:
    print(f"Warning: Failed to initialize vector store: {str(e)}")
    vector_store = None

@tool
def search_hospital_policies(query: str) -> str:
    """Search hospital policies and procedures for specific information about patient care, visiting hours, admission procedures, consent policies, confidentiality rules, bed management, transfers, complaints, quality standards, and medicine management."""
    try:
        if vector_store is None:
            return "Error: Hospital policies database is not available. Please ensure the PDF file exists at utils/hospital.pdf"
        
        docs = vector_store.similarity_search(query, k=3)
        if not docs:
            return "No relevant hospital policies found for your query."
        
        context = "\n\n".join([doc.page_content for doc in docs])
        return f"Hospital Policies Information:\n{context}"
    except Exception as e:
        return f"Error searching hospital policies: {str(e)}"

@tool
def get_current_datetime() -> str:
    """Get the current date and time information."""
    return f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def get_owner_info() -> str:
    """Get information about the hospital owner Dr. Hari and hospital leadership details."""
    return """Hospital Owner Information:
    Name: Dr. Hari
    Position: Owner and Medical Director
    Hospital: Community Health Center Harichandanpur
    Location: Keonjhar, Odisha, India
    
    Dr. Hari is the owner and medical director of Community Health Center Harichandanpur, 
    overseeing all medical operations, policy implementation, and ensuring quality healthcare 
    delivery at the facility. Under his leadership, the hospital maintains comprehensive 
    policies for patient care, safety, and quality management."""

@tool
def book_medical_token(
    patient_name: str,
    patient_phone: str,
    patient_age: int,
    department: str,
    booking_date: str,
    booking_time: str,
    doctor_name: str = None,
    symptoms: str = None,
    priority: str = "normal",
    notes: str = None
) -> str:
    """
    Book a medical consultation token for a patient.
    
    Args:
        patient_name: Full name of the patient
        patient_phone: Contact phone number (10-15 digits)
        patient_age: Age of the patient (0-150)
        department: Department for consultation (general_medicine, cardiology, pediatrics, gynecology, orthopedics, emergency, dental, dermatology, psychiatry)
        booking_date: Date for appointment (YYYY-MM-DD format)
        booking_time: Time for appointment (HH:MM format)
        doctor_name: Preferred doctor name (optional)
        symptoms: Patient symptoms description (optional)
        priority: Priority level (low, normal, high, emergency) - default: normal
        notes: Additional notes (optional)
    
    Returns:
        Booking confirmation message with token number or error message
    """
    try:
        # Validate department
        try:
            dept_enum = Department(department.lower())
        except ValueError:
            valid_departments = [dept.value for dept in Department]
            return f"Invalid department. Available departments: {', '.join(valid_departments)}"
        
        # Parse date and time
        try:
            parsed_date = date.fromisoformat(booking_date)
            parsed_time = time.fromisoformat(booking_time)
        except ValueError as e:
            return f"Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time. Error: {str(e)}"
        
        # Create booking request
        request = TokenBookingRequest(
            patient_name=patient_name,
            patient_phone=patient_phone,
            patient_age=patient_age,
            department=dept_enum,
            doctor_name=doctor_name,
            booking_date=parsed_date,
            booking_time=parsed_time,
            symptoms=symptoms,
            priority=priority,
            notes=notes
        )
        
        # Create booking
        result = token_manager.create_booking(request)
        
        if result.success:
            return f"✅ Token booking successful!\n\nPatient: {patient_name}\nToken Number: {result.token_number}\nDepartment: {department.replace('_', ' ').title()}\nDate: {booking_date}\nTime: {booking_time}\nStatus: Pending\n\nToken ID: {result.token_id}\n\nPlease arrive 15 minutes before your appointment time."
        else:
            return f"❌ Booking failed: {result.message}"
            
    except Exception as e:
        return f"❌ Error booking token: {str(e)}"

@tool
def check_token_status(token_id: str) -> str:
    """
    Check the status of a token booking using token ID.
    
    Args:
        token_id: Unique token identifier
    
    Returns:
        Token status and booking details or error message
    """
    try:
        booking = token_manager.get_booking(token_id)
        
        if not booking:
            return f"❌ Token booking not found with ID: {token_id}"
        
        status_emoji = {
            "pending": "⏳",
            "confirmed": "✅",
            "cancelled": "❌",
            "completed": "✅",
            "no_show": "🚫"
        }
        
        emoji = status_emoji.get(booking.status, "❓")
        
        return f"""{emoji} Token Status: {booking.status.replace('_', ' ').title()}

Patient: {booking.patient_name}
Token Number: {booking.token_number}
Department: {booking.department.value.replace('_', ' ').title()}
Date: {booking.booking_date}
Time: {booking.booking_time}
Priority: {booking.priority.title()}
Created: {booking.created_at.strftime('%Y-%m-%d %H:%M')}

{f'Symptoms: {booking.symptoms}' if booking.symptoms else ''}
{f'Doctor: {booking.doctor_name}' if booking.doctor_name else ''}
{f'Notes: {booking.notes}' if booking.notes else ''}"""
        
    except Exception as e:
        return f"❌ Error checking token status: {str(e)}"

@tool
def search_tokens(
    patient_name: str = None,
    patient_phone: str = None,
    department: str = None,
    booking_date: str = None,
    status: str = None
) -> str:
    """
    Search for token bookings based on various criteria.
    
    Args:
        patient_name: Search by patient name (partial match)
        patient_phone: Search by phone number
        department: Filter by department
        booking_date: Filter by booking date (YYYY-MM-DD)
        status: Filter by status (pending, confirmed, cancelled, completed, no_show)
    
    Returns:
        List of matching token bookings or error message
    """
    try:
        # Parse date if provided
        parsed_date = None
        if booking_date:
            try:
                parsed_date = date.fromisoformat(booking_date)
            except ValueError:
                return f"Invalid date format. Use YYYY-MM-DD format."
        
        # Parse department if provided
        dept_enum = None
        if department:
            try:
                dept_enum = Department(department.lower())
            except ValueError:
                valid_departments = [dept.value for dept in Department]
                return f"Invalid department. Available departments: {', '.join(valid_departments)}"
        
        # Parse status if provided
        status_enum = None
        if status:
            try:
                status_enum = TokenStatus(status.lower())
            except ValueError:
                valid_statuses = [s.value for s in TokenStatus]
                return f"Invalid status. Available statuses: {', '.join(valid_statuses)}"
        
        # Create search request
        search_request = TokenSearchRequest(
            patient_name=patient_name,
            patient_phone=patient_phone,
            department=dept_enum,
            booking_date=parsed_date,
            status=status_enum
        )
        
        # Search bookings
        bookings = token_manager.search_bookings(search_request)
        
        if not bookings:
            return "No token bookings found matching the search criteria."
        
        # Format results
        result = f"Found {len(bookings)} token booking(s):\n\n"
        
        for i, booking in enumerate(bookings, 1):
            status_emoji = {
                "pending": "⏳",
                "confirmed": "✅",
                "cancelled": "❌",
                "completed": "✅",
                "no_show": "🚫"
            }
            emoji = status_emoji.get(booking.status, "❓")
            
            result += f"""{i}. {emoji} Token #{booking.token_number} - {booking.status.replace('_', ' ').title()}
   Patient: {booking.patient_name}
   Phone: {booking.patient_phone}
   Department: {booking.department.value.replace('_', ' ').title()}
   Date: {booking.booking_date} at {booking.booking_time}
   Priority: {booking.priority.title()}
   Token ID: {booking.token_id}
   
"""
        
        return result
        
    except Exception as e:
        return f"❌ Error searching tokens: {str(e)}"

@tool
def get_daily_tokens(booking_date: str, department: str = None) -> str:
    """
    Get all token bookings for a specific date.
    
    Args:
        booking_date: Date to get bookings for (YYYY-MM-DD format)
        department: Optional department filter
    
    Returns:
        List of token bookings for the specified date or error message
    """
    try:
        # Parse date
        try:
            parsed_date = date.fromisoformat(booking_date)
        except ValueError:
            return f"Invalid date format. Use YYYY-MM-DD format."
        
        # Parse department if provided
        dept_enum = None
        if department:
            try:
                dept_enum = Department(department.lower())
            except ValueError:
                valid_departments = [dept.value for dept in Department]
                return f"Invalid department. Available departments: {', '.join(valid_departments)}"
        
        # Get daily bookings
        bookings = token_manager.get_daily_bookings(parsed_date, dept_enum)
        
        if not bookings:
            dept_text = f" for {department.replace('_', ' ').title()}" if department else ""
            return f"No token bookings found for {booking_date}{dept_text}."
        
        # Format results
        dept_text = f" for {department.replace('_', ' ').title()}" if department else ""
        result = f"Token bookings for {booking_date}{dept_text}:\n\n"
        
        # Group by department if no specific department requested
        if not department:
            dept_groups = {}
            for booking in bookings:
                dept = booking.department.value
                if dept not in dept_groups:
                    dept_groups[dept] = []
                dept_groups[dept].append(booking)
            
            for dept, dept_bookings in dept_groups.items():
                result += f"📋 {dept.replace('_', ' ').title()} Department:\n"
                for booking in dept_bookings:
                    status_emoji = {
                        "pending": "⏳",
                        "confirmed": "✅",
                        "cancelled": "❌",
                        "completed": "✅",
                        "no_show": "🚫"
                    }
                    emoji = status_emoji.get(booking.status, "❓")
                    
                    result += f"  {emoji} Token #{booking.token_number} - {booking.patient_name} ({booking.booking_time}) - {booking.status.replace('_', ' ').title()}\n"
                result += "\n"
        else:
            for booking in bookings:
                status_emoji = {
                    "pending": "⏳",
                    "confirmed": "✅",
                    "cancelled": "❌",
                    "completed": "✅",
                    "no_show": "🚫"
                }
                emoji = status_emoji.get(booking.status, "❓")
                
                result += f"{emoji} Token #{booking.token_number} - {booking.patient_name} ({booking.booking_time}) - {booking.status.replace('_', ' ').title()}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting daily tokens: {str(e)}"

@tool
def get_booking_statistics() -> str:
    """
    Get token booking statistics including counts by status and department.
    
    Returns:
        Formatted statistics about token bookings
    """
    try:
        stats = token_manager.get_booking_stats()
        
        result = f"📊 Token Booking Statistics\n\n"
        result += f"Total Bookings: {stats['total_bookings']}\n\n"
        
        result += "📈 Status Breakdown:\n"
        for status, count in stats['status_breakdown'].items():
            status_emoji = {
                "pending": "⏳",
                "confirmed": "✅",
                "cancelled": "❌",
                "completed": "✅",
                "no_show": "🚫"
            }
            emoji = status_emoji.get(status, "❓")
            result += f"  {emoji} {status.replace('_', ' ').title()}: {count}\n"
        
        result += "\n🏥 Department Breakdown:\n"
        for department, count in stats['department_breakdown'].items():
            result += f"  📋 {department.replace('_', ' ').title()}: {count}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting booking statistics: {str(e)}"



@tool
def get_current_serving_token(doctor_name: str) -> str:
    """
    Find out which token number a doctor is currently serving.
    Use this when someone asks "What token is Dr. X on?" or "Which number is being served?"
    
    Args:
        doctor_name: The doctor's name (e.g., "Dr. Sharma", "Dr. Patel")
    
    Returns:
        Current token information or message if no token is being served
    """
    try:
        # Ask the token manager for current token
        current_info = token_manager.get_current_token(doctor_name)
        
        # If no current token found
        if not current_info:
            return f"❓ Dr. {doctor_name} is not currently marked as seeing any patient. No current token information available."
        
        # Calculate how long ago it was updated
        from datetime import datetime
        updated_time = datetime.fromisoformat(current_info['updated_at'])
        time_ago = datetime.now() - updated_time
        minutes_ago = int(time_ago.total_seconds() / 60)
        
        # Format nice response
        response = f"""🎫 **Current Token Being Served**

👨‍⚕️ **Doctor:** Dr. {current_info['doctor_name']}
🏥 **Department:** {current_info['department'].replace('_', ' ').title()}
🔢 **Token Number:** #{current_info['current_token_number']}
👤 **Patient:** {current_info['patient_name']}
🕐 **Last Updated:** {minutes_ago} minute(s) ago

✅ Dr. {current_info['doctor_name']} is currently serving **Token #{current_info['current_token_number']}**."""
        
        return response
        
    except Exception as e:
        return f"❌ Sorry, I couldn't check the current token. Error: {str(e)}"


# List of all tools
TOOLS = [
    search_hospital_policies, 
    get_current_datetime, 
    get_owner_info,
    book_medical_token,
    check_token_status,
    search_tokens,
    get_daily_tokens,
    get_booking_statistics,
    get_current_serving_token  # ← ADD THIS LINE
]