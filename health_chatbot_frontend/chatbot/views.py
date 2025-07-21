import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

def home(request):
    """Home page with the health chatbot interface"""
    return render(request, 'chatbot/home.html')

@csrf_exempt
@require_http_methods(["POST"])
def get_health_advice(request):
    """Get health advice from FastAPI backend"""
    try:
        data = json.loads(request.body)
        
        # Prepare data for FastAPI
        api_data = {
            "weight": float(data.get('weight', 0)),
            "height": float(data.get('height', 0)),
            "age": int(data.get('age', 30)) if data.get('age') else None,
            "gender": data.get('gender'),
            "activity_level": data.get('activity_level', 'moderate'),
            "daily_routine": data.get('daily_routine', ''),
            "goals": data.get('goals', 'general_health'),
            "medical_conditions": data.get('medical_conditions', '')
        }
        
        # Call FastAPI backend
        response = requests.post(
            f"{settings.FASTAPI_BACKEND_URL}/api/health-advice/",
            json=api_data,
            timeout=30
        )
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({
                'error': 'Failed to get health advice',
                'details': response.text
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred',
            'details': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_user_profile(request):
    """Save user profile to FastAPI backend"""
    try:
        data = json.loads(request.body)
        
        # Prepare data for FastAPI
        api_data = {
            "name": data.get('name', ''),
            "age": int(data.get('age', 30)) if data.get('age') else None,
            "weight": float(data.get('weight', 0)),
            "height": float(data.get('height', 0)),
            "gender": data.get('gender'),
            "activity_level": data.get('activity_level', 'moderate'),
            "daily_routine": data.get('daily_routine', ''),
            "goals": data.get('goals', 'general_health'),
            "medical_conditions": data.get('medical_conditions', '')
        }
        
        # Call FastAPI backend
        response = requests.post(
            f"{settings.FASTAPI_BACKEND_URL}/api/user-profile/",
            json=api_data,
            timeout=30
        )
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({
                'error': 'Failed to save user profile',
                'details': response.text
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred',
            'details': str(e)
        }, status=500)

def user_profiles(request):
    """Display user profiles page"""
    try:
        # Get user profiles from FastAPI backend
        response = requests.get(
            f"{settings.FASTAPI_BACKEND_URL}/api/user-profiles/",
            timeout=30
        )
        
        if response.status_code == 200:
            profiles = response.json()
        else:
            profiles = []
            
    except Exception as e:
        profiles = []
    
    return render(request, 'chatbot/profiles.html', {'profiles': profiles}) 