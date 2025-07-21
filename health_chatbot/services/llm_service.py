import os
import openai
import asyncio
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your key in environment variable

    async def generate_health_advice(
        self,
        weight: float,
        height: float,
        age: int = None,
        gender: str = None,
        activity_level: str = None,
        daily_routine: str = None,
        goals: str = None,
        medical_conditions: str = None,
        bmi: float = None,
        calories_needed: int = None
    ) -> str:
        prompt = self._create_health_prompt(
            weight, height, age, gender, activity_level,
            daily_routine, goals, medical_conditions, bmi, calories_needed
        )
        # Call OpenAI's API (use gpt-3.5-turbo or gpt-4)
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a professional health and fitness advisor."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def _create_health_prompt(
        self,
        weight: float,
        height: float,
        age: Optional[int],
        gender: Optional[str],
        activity_level: Optional[str],
        daily_routine: Optional[str],
        goals: Optional[str],
        medical_conditions: Optional[str],
        bmi: Optional[float],
        calories_needed: Optional[int]
    ) -> str:
        """
        Create a comprehensive prompt for health advice generation
        """
        prompt = f"""You are a professional health and fitness advisor. Provide personalized, practical, and safe health advice based on the following information:

Patient Information:
- Weight: {weight} kg
- Height: {height} cm
- Age: {age if age else 'Not specified'}
- Gender: {gender if gender else 'Not specified'}
- Activity Level: {activity_level if activity_level else 'Not specified'}
- Daily Routine: {daily_routine if daily_routine else 'Not specified'}
- Health Goals: {goals if goals else 'General health'}
- Medical Conditions: {medical_conditions if medical_conditions else 'None specified'}
- BMI: {bmi if bmi else 'Not calculated'}
- Daily Calorie Needs: {calories_needed if calories_needed else 'Not calculated'}

Please provide:
1. A brief assessment of their current health status
2. Personalized diet recommendations
3. Exercise suggestions appropriate for their fitness level
4. Lifestyle tips for better health
5. Any precautions or warnings if applicable

Keep the advice practical, encouraging, and easy to follow. Focus on sustainable lifestyle changes rather than quick fixes. Always emphasize consulting with healthcare professionals for medical concerns.

Response:"""

        return prompt
    
    def _get_fallback_advice(self, bmi: Optional[float], calories_needed: Optional[int], goals: Optional[str]) -> str:
        """
        Provide fallback advice when LLM is not available
        """
        advice = "Based on your information, here are some general health recommendations:\n\n"
        
        if bmi:
            if bmi < 18.5:
                advice += "• Your BMI indicates you're underweight. Consider increasing your calorie intake with nutrient-rich foods.\n"
            elif bmi < 25:
                advice += "• Your BMI is in the healthy range. Focus on maintaining a balanced diet and regular exercise.\n"
            elif bmi < 30:
                advice += "• Your BMI indicates you're overweight. Consider a balanced diet with moderate calorie reduction and regular exercise.\n"
            else:
                advice += "• Your BMI indicates obesity. Consider consulting a healthcare provider for a personalized weight management plan.\n"
        
        if calories_needed:
            advice += f"• Your estimated daily calorie needs are approximately {calories_needed} calories.\n"
        
        if goals:
            if goals == "weight_loss":
                advice += "• For weight loss, create a moderate calorie deficit through diet and exercise.\n"
            elif goals == "muscle_gain":
                advice += "• For muscle gain, increase protein intake and focus on strength training.\n"
            elif goals == "maintenance":
                advice += "• For weight maintenance, balance your calorie intake with your activity level.\n"
        
        advice += "\nGeneral recommendations:\n"
        advice += "• Eat a balanced diet with plenty of fruits, vegetables, and lean proteins\n"
        advice += "• Exercise regularly, aiming for at least 150 minutes of moderate activity per week\n"
        advice += "• Stay hydrated by drinking plenty of water\n"
        advice += "• Get 7-9 hours of quality sleep each night\n"
        advice += "• Consult with healthcare professionals for personalized medical advice\n"
        
        return advice 