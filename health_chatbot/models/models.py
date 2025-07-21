from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=False)  # in kg
    height = Column(Float, nullable=False)  # in cm
    gender = Column(String(10), nullable=True)
    activity_level = Column(String(20), nullable=True)  # sedentary, light, moderate, active, very_active
    daily_routine = Column(Text, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    goals = Column(String(100), nullable=True)  # weight_loss, muscle_gain, maintenance, general_health
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class HealthAdvice(Base):
    __tablename__ = "health_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, nullable=False)
    advice_type = Column(String(50), nullable=False)  # diet, exercise, general
    advice_content = Column(Text, nullable=False)
    bmi = Column(Float, nullable=True)
    calories_needed = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now()) 