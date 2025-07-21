from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models import models as db_models, schemas

router = APIRouter()

@router.post("/user-profile/", response_model=schemas.UserProfile)
def create_user_profile(
    profile: schemas.UserProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user profile
    """
    db_profile = db_models.UserProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/user-profile/{profile_id}", response_model=schemas.UserProfile)
def get_user_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user profile by ID
    """
    profile = db.query(db_models.UserProfile).filter(db_models.UserProfile.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.get("/user-profiles/", response_model=List[schemas.UserProfile])
def get_all_user_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all user profiles with pagination
    """
    profiles = db.query(db_models.UserProfile).offset(skip).limit(limit).all()
    return profiles

@router.put("/user-profile/{profile_id}", response_model=schemas.UserProfile)
def update_user_profile(
    profile_id: int,
    profile_update: schemas.UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user profile
    """
    db_profile = db.query(db_models.UserProfile).filter(db_models.UserProfile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    # Update only provided fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.delete("/user-profile/{profile_id}")
def delete_user_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete a user profile
    """
    db_profile = db.query(db_models.UserProfile).filter(db_models.UserProfile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    db.delete(db_profile)
    db.commit()
    return {"message": "User profile deleted successfully"} 