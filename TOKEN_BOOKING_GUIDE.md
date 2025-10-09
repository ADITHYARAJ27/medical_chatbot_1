# Token Booking System Guide 🏥

A comprehensive token booking system for the Medical Assistant API at Community Health Center Harichandanpur, Keonjhar, Odisha.

## Overview

The token booking system allows patients to book medical consultation appointments, manage their bookings, and provides administrative tools for hospital staff to manage appointments efficiently.

## Features

### 🎫 Core Booking Features
- **Token Booking**: Book appointments with specific departments
- **Status Management**: Track booking status (pending, confirmed, completed, cancelled, no_show)
- **Department Support**: 9 medical departments available
- **Priority Levels**: Support for different priority levels (low, normal, high, emergency)
- **Patient Information**: Store patient details, symptoms, and notes

### 🔍 Search & Management
- **Token Search**: Search bookings by patient name, phone, department, date, or status
- **Daily Schedules**: View all appointments for a specific date
- **Patient History**: Complete booking history for patients
- **Statistics**: Comprehensive booking analytics and reports

### 🤖 AI Integration
- **Chat Assistant**: Book tokens through natural language conversation
- **Smart Tools**: AI-powered booking management tools
- **Status Updates**: Check token status through chat interface

## API Endpoints

### Token Booking Endpoints

#### 1. Book a Token
```http
POST /tokens/book
Content-Type: application/json

{
    "patient_name": "John Doe",
    "patient_phone": "9876543210",
    "patient_age": 35,
    "department": "general_medicine",
    "booking_date": "2024-01-15",
    "booking_time": "10:30",
    "doctor_name": "Dr. Smith",
    "symptoms": "Fever and headache",
    "priority": "normal",
    "notes": "First time visit"
}
```

#### 2. Get Token Details
```http
GET /tokens/{token_id}
```

#### 3. Update Token Status
```http
PUT /tokens/{token_id}/status
Content-Type: application/json

{
    "status": "confirmed",
    "notes": "Patient confirmed appointment"
}
```

#### 4. Cancel Token
```http
DELETE /tokens/{token_id}
```

#### 5. Search Tokens
```http
GET /tokens/search?patient_name=John&department=general_medicine&status=pending
```

#### 6. Get Daily Bookings
```http
GET /tokens/daily/2024-01-15?department=cardiology
```

#### 7. Get Booking Statistics
```http
GET /tokens/stats
```

#### 8. Get Available Departments
```http
GET /tokens/departments
```

#### 9. Get Available Statuses
```http
GET /tokens/statuses
```

## Departments

The system supports the following medical departments:

- `general_medicine` - General Medicine
- `cardiology` - Cardiology
- `pediatrics` - Pediatrics
- `gynecology` - Gynecology
- `orthopedics` - Orthopedics
- `emergency` - Emergency
- `dental` - Dental
- `dermatology` - Dermatology
- `psychiatry` - Psychiatry

## Token Statuses

- `pending` - ⏳ Newly booked, awaiting confirmation
- `confirmed` - ✅ Confirmed by patient/staff
- `completed` - ✅ Appointment completed
- `cancelled` - ❌ Cancelled by patient/staff
- `no_show` - 🚫 Patient did not show up

## Priority Levels

- `low` - Low priority appointments
- `normal` - Standard priority (default)
- `high` - High priority appointments
- `emergency` - Emergency cases

## Chat Assistant Integration

### Booking Through Chat

You can book tokens through the chat interface using natural language:

**Examples:**
- "I want to book an appointment for tomorrow at 2 PM with the cardiology department"
- "Book a token for John Doe, phone 9876543210, age 35, for general medicine on 2024-01-15 at 10:30"
- "I need to check the status of my token with ID abc123"

### Available Chat Commands

1. **Book Token**: Use the `book_medical_token` tool
2. **Check Status**: Use the `check_token_status` tool
3. **Search Bookings**: Use the `search_tokens` tool
4. **Daily Schedule**: Use the `get_daily_tokens` tool
5. **Statistics**: Use the `get_booking_statistics` tool

## Data Storage

The system uses JSON file-based storage located at:
- **Bookings Data**: `utils/data/token_bookings.json`
- **Export Files**: `utils/data/bookings_export_*.json`

## Management Utilities

### Daily Reports
Generate comprehensive daily reports with department breakdowns, status statistics, and priority analysis.

### Analytics
Get detailed analytics for date ranges including:
- Completion rates
- Cancellation rates
- Department performance
- Daily trends

### Data Export
Export booking data to JSON format for external analysis or backup.

### Cleanup
Automated cleanup of old completed/cancelled bookings to maintain system performance.

## Usage Examples

### Python API Usage

```python
import requests

# Book a token
response = requests.post("http://localhost:8000/tokens/book", json={
    "patient_name": "Jane Smith",
    "patient_phone": "9876543211",
    "patient_age": 28,
    "department": "cardiology",
    "booking_date": "2024-01-15",
    "booking_time": "14:30",
    "symptoms": "Chest pain",
    "priority": "high"
})

result = response.json()
print(f"Token ID: {result['token_id']}")
print(f"Token Number: {result['token_number']}")
```

### JavaScript/Fetch Usage

```javascript
// Book a token
fetch('http://localhost:8000/tokens/book', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        patient_name: "John Doe",
        patient_phone: "9876543210",
        patient_age: 35,
        department: "general_medicine",
        booking_date: "2024-01-15",
        booking_time: "10:30",
        symptoms: "Fever and headache",
        priority: "normal"
    })
})
.then(response => response.json())
.then(data => {
    console.log('Booking successful:', data);
    console.log('Token ID:', data.token_id);
    console.log('Token Number:', data.token_number);
});
```

### Curl Usage

```bash
# Book a token
curl -X POST "http://localhost:8000/tokens/book" \
     -H "Content-Type: application/json" \
     -d '{
         "patient_name": "John Doe",
         "patient_phone": "9876543210",
         "patient_age": 35,
         "department": "general_medicine",
         "booking_date": "2024-01-15",
         "booking_time": "10:30",
         "symptoms": "Fever and headache",
         "priority": "normal"
     }'

# Check token status
curl -X GET "http://localhost:8000/tokens/abc123"

# Get daily bookings
curl -X GET "http://localhost:8000/tokens/daily/2024-01-15"
```

## Error Handling

The system provides comprehensive error handling with meaningful error messages:

- **400 Bad Request**: Invalid input data or business logic violations
- **404 Not Found**: Token booking not found
- **500 Internal Server Error**: System errors

## Testing

Run the test suite to verify system functionality:

```bash
python test_token_booking.py
```

The test suite covers:
- Basic booking functionality
- Booking retrieval and updates
- Search capabilities
- Daily booking management
- Statistics generation
- Management utilities
- Agent tools integration

## Security Considerations

- Input validation for all fields
- Phone number format validation
- Date/time format validation
- Department and status enum validation
- File-based storage with proper error handling

## Performance

- In-memory data management for fast access
- JSON file persistence for data durability
- Efficient search algorithms
- Automatic cleanup of old data

## Future Enhancements

Potential future improvements:
- Database integration (PostgreSQL, MongoDB)
- Email/SMS notifications
- Calendar integration
- Payment processing
- Multi-language support
- Mobile app integration
- Real-time notifications
- Advanced analytics dashboard

## Support

For technical support or questions about the token booking system, please refer to the main project documentation or contact the development team.

---

**Community Health Center Harichandanpur**  
*Keonjhar, Odisha, India*  
*Under the guidance of Dr. Harshin*

