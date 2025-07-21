from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# User Profile Schemas
class UserProfileBase(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=1, le=120)
    weight: float = Field(..., gt=0, le=500)  # kg
    height: float = Field(..., gt=0, le=300)  # cm
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    daily_routine: Optional[str] = None
    medical_conditions: Optional[str] = None
    goals: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Health Advice Schemas
class HealthAdviceRequest(BaseModel):
    user_profile_id: int
    advice_type: str = Field(..., pattern="^(diet|exercise|general)$")

class HealthAdviceResponse(BaseModel):
    id: int
    user_profile_id: int
    advice_type: str
    advice_content: str
    bmi: Optional[float] = None
    calories_needed: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chatbot Request/Response
class ChatbotRequest(BaseModel):
    weight: float = Field(..., gt=0, le=500)
    height: float = Field(..., gt=0, le=300)
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    daily_routine: Optional[str] = None
    goals: Optional[str] = Field(None, pattern="^(weight_loss|muscle_gain|maintenance|general_health)$")
    medical_conditions: Optional[str] = None

class ChatbotResponse(BaseModel):
    advice: str
    bmi: float
    bmi_category: str
    calories_needed: int
    recommendations: dict 