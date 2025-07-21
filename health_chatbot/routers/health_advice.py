from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models import models as db_models, schemas
from services.health_service import HealthService
from services.llm_service import LLMService

router = APIRouter()

@router.post("/health-advice/", response_model=schemas.ChatbotResponse)
async def get_health_advice(
    request: schemas.ChatbotRequest,
    db: Session = Depends(get_db)
):
    """
    Get personalized health advice based on user input
    """
    try:
        # Initialize services
        health_service = HealthService()
        llm_service = LLMService()
        
        # Calculate BMI and other metrics
        bmi = health_service.calculate_bmi(request.weight, request.height)
        bmi_category = health_service.get_bmi_category(bmi)
        calories_needed = health_service.calculate_calories(
            request.weight, request.height, request.age, 
            request.gender, request.activity_level
        )
        
        # Generate personalized advice using LLM
        advice = await llm_service.generate_health_advice(
            weight=request.weight,
            height=request.height,
            age=request.age,
            gender=request.gender,
            activity_level=request.activity_level,
            daily_routine=request.daily_routine,
            goals=request.goals,
            medical_conditions=request.medical_conditions,
            bmi=bmi,
            calories_needed=calories_needed
        )
        
        # Prepare recommendations
        recommendations = {
            "diet": health_service.get_diet_recommendations(bmi_category, request.goals),
            "exercise": health_service.get_exercise_recommendations(bmi_category, request.activity_level),
            "lifestyle": health_service.get_lifestyle_recommendations(bmi_category)
        }
        
        return schemas.ChatbotResponse(
            advice=advice,
            bmi=bmi,
            bmi_category=bmi_category,
            calories_needed=calories_needed,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating health advice: {str(e)}")

@router.get("/health-advice/history/{user_id}", response_model=List[schemas.HealthAdviceResponse])
def get_advice_history(user_id: int, db: Session = Depends(get_db)):
    """
    Get health advice history for a user
    """
    advice_history = db.query(db_models.HealthAdvice).filter(
        db_models.HealthAdvice.user_profile_id == user_id
    ).order_by(db_models.HealthAdvice.created_at.desc()).all()
    
    return advice_history

@router.post("/health-advice/save/", response_model=schemas.HealthAdviceResponse)
def save_advice(
    advice_request: schemas.HealthAdviceRequest,
    db: Session = Depends(get_db)
):
    """
    Save health advice to database
    """
    db_advice = db_models.HealthAdvice(**advice_request.dict())
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice 