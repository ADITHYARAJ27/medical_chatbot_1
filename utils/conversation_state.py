from typing import Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class CollectionStep(str, Enum):
    """Steps in the information collection process"""
    GREETING = "greeting"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_AGE = "collecting_age"
    COLLECTING_PHONE = "collecting_phone"
    COLLECTING_DETAILS = "collecting_details"
    CONFIRMING_INFO = "confirming_info"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserInfo(BaseModel):
    """Model for storing collected user information"""
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    details: Optional[str] = None
    collected_at: Optional[datetime] = None

class ConversationState(BaseModel):
    """State management for sequential information collection"""
    current_step: CollectionStep = CollectionStep.GREETING
    user_info: UserInfo = Field(default_factory=UserInfo)
    thread_id: str
    started_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def update_step(self, new_step: CollectionStep):
        """Update the current step and timestamp"""
        self.current_step = new_step
        self.last_updated = datetime.now()
    
    def set_user_info(self, **kwargs):
        """Set user information fields"""
        for key, value in kwargs.items():
            if hasattr(self.user_info, key):
                setattr(self.user_info, key, value)
        self.user_info.collected_at = datetime.now()
        self.last_updated = datetime.now()
    
    def is_info_complete(self) -> bool:
        """Check if all required information is collected"""
        return all([
            self.user_info.name,
            self.user_info.age is not None,
            self.user_info.phone,
            self.user_info.details
        ])
    
    def get_missing_fields(self) -> list:
        """Get list of missing required fields"""
        missing = []
        if not self.user_info.name:
            missing.append("name")
        if self.user_info.age is None:
            missing.append("age")
        if not self.user_info.phone:
            missing.append("phone")
        if not self.user_info.details:
            missing.append("details")
        return missing

class ConversationStateManager:
    """Manages conversation states for different threads"""
    
    def __init__(self):
        self.states: Dict[str, ConversationState] = {}
    
    def get_state(self, thread_id: str) -> ConversationState:
        """Get or create conversation state for a thread"""
        if thread_id not in self.states:
            self.states[thread_id] = ConversationState(thread_id=thread_id)
        return self.states[thread_id]
    
    def update_state(self, thread_id: str, **kwargs) -> ConversationState:
        """Update conversation state"""
        state = self.get_state(thread_id)
        
        # Update step if provided
        if 'current_step' in kwargs:
            state.update_step(kwargs['current_step'])
        
        # Update user info if provided
        user_info_updates = {k: v for k, v in kwargs.items() if k in ['name', 'age', 'phone', 'details']}
        if user_info_updates:
            state.set_user_info(**user_info_updates)
        
        return state
    
    def reset_state(self, thread_id: str):
        """Reset conversation state for a thread"""
        self.states[thread_id] = ConversationState(thread_id=thread_id)
    
    def cleanup_old_states(self, max_age_hours: int = 24):
        """Clean up old conversation states"""
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        to_remove = []
        
        for thread_id, state in self.states.items():
            if state.started_at.timestamp() < cutoff_time:
                to_remove.append(thread_id)
        
        for thread_id in to_remove:
            del self.states[thread_id]

# Global conversation state manager
conversation_manager = ConversationStateManager()


