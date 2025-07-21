class HealthService:
    def __init__(self):
        # Activity level multipliers for BMR calculation
        self.activity_multipliers = {
            "sedentary": 1.2,      # Little or no exercise
            "light": 1.375,        # Light exercise 1-3 days/week
            "moderate": 1.55,      # Moderate exercise 3-5 days/week
            "active": 1.725,       # Hard exercise 6-7 days/week
            "very_active": 1.9     # Very hard exercise, physical job
        }
    
    def calculate_bmi(self, weight: float, height: float) -> float:
        """
        Calculate BMI: weight (kg) / height (m)²
        """
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        return round(bmi, 1)
    
    def get_bmi_category(self, bmi: float) -> str:
        """
        Get BMI category based on BMI value
        """
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"
    
    def calculate_bmr(self, weight: float, height: float, age: int, gender: str) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        """
        if gender and gender.lower() == "female":
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:  # Default to male calculation
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        return bmr
    
    def calculate_calories(self, weight: float, height: float, age: int = None, 
                          gender: str = None, activity_level: str = "moderate") -> int:
        """
        Calculate daily calorie needs
        """
        if age is None:
            age = 30  # Default age if not provided
        
        bmr = self.calculate_bmr(weight, height, age, gender)
        multiplier = self.activity_multipliers.get(activity_level, 1.55)
        calories = bmr * multiplier
        
        return round(calories)
    
    def get_diet_recommendations(self, bmi_category: str, goals: str = None) -> dict:
        """
        Get diet recommendations based on BMI category and goals
        """
        recommendations = {
            "underweight": {
                "calories": "Increase calorie intake by 500-1000 calories per day",
                "protein": "1.2-1.5g protein per kg body weight",
                "carbs": "Focus on complex carbohydrates",
                "fats": "Include healthy fats from nuts, avocados, olive oil",
                "meals": "Eat 5-6 smaller meals throughout the day"
            },
            "normal": {
                "calories": "Maintain current calorie intake",
                "protein": "1.0-1.2g protein per kg body weight",
                "carbs": "45-65% of daily calories from carbohydrates",
                "fats": "20-35% of daily calories from healthy fats",
                "meals": "3 main meals with 1-2 snacks"
            },
            "overweight": {
                "calories": "Create a 500-750 calorie deficit for weight loss",
                "protein": "1.2-1.5g protein per kg body weight",
                "carbs": "Reduce refined carbohydrates",
                "fats": "Focus on healthy fats, limit saturated fats",
                "meals": "3 balanced meals, avoid late-night eating"
            },
            "obese": {
                "calories": "Create a 750-1000 calorie deficit for weight loss",
                "protein": "1.5-2.0g protein per kg body weight",
                "carbs": "Limit to 100-150g per day",
                "fats": "Focus on healthy fats, avoid trans fats",
                "meals": "Structured meal timing, portion control"
            }
        }
        
        base_recommendations = recommendations.get(bmi_category, recommendations["normal"])
        
        # Adjust based on goals
        if goals:
            if goals == "weight_loss":
                base_recommendations["calories"] = "Create a 500-750 calorie deficit"
            elif goals == "muscle_gain":
                base_recommendations["calories"] = "Increase calories by 300-500 per day"
                base_recommendations["protein"] = "1.6-2.2g protein per kg body weight"
        
        return base_recommendations
    
    def get_exercise_recommendations(self, bmi_category: str, activity_level: str) -> dict:
        """
        Get exercise recommendations based on BMI category and current activity level
        """
        recommendations = {
            "underweight": {
                "cardio": "Light to moderate cardio 3-4 times per week",
                "strength": "Focus on strength training 3-4 times per week",
                "duration": "30-45 minutes per session",
                "intensity": "Moderate intensity, avoid overtraining"
            },
            "normal": {
                "cardio": "150 minutes moderate or 75 minutes vigorous cardio per week",
                "strength": "Strength training 2-3 times per week",
                "duration": "30-60 minutes per session",
                "intensity": "Mix of moderate and vigorous intensity"
            },
            "overweight": {
                "cardio": "200-300 minutes moderate cardio per week",
                "strength": "Strength training 2-3 times per week",
                "duration": "45-60 minutes per session",
                "intensity": "Start with low-impact, gradually increase"
            },
            "obese": {
                "cardio": "Start with walking, aim for 150 minutes per week",
                "strength": "Begin with bodyweight exercises",
                "duration": "Start with 10-15 minutes, gradually increase",
                "intensity": "Low-impact activities, focus on consistency"
            }
        }
        
        return recommendations.get(bmi_category, recommendations["normal"])
    
    def get_lifestyle_recommendations(self, bmi_category: str) -> dict:
        """
        Get lifestyle recommendations based on BMI category
        """
        recommendations = {
            "underweight": {
                "sleep": "7-9 hours of quality sleep",
                "stress": "Manage stress through relaxation techniques",
                "hydration": "Stay hydrated, drink 8-10 glasses of water daily",
                "habits": "Avoid smoking, limit alcohol consumption"
            },
            "normal": {
                "sleep": "7-9 hours of quality sleep",
                "stress": "Regular stress management activities",
                "hydration": "Drink 8-10 glasses of water daily",
                "habits": "Maintain healthy lifestyle habits"
            },
            "overweight": {
                "sleep": "7-9 hours of quality sleep",
                "stress": "Practice stress management techniques",
                "hydration": "Drink 10-12 glasses of water daily",
                "habits": "Limit processed foods, practice mindful eating"
            },
            "obese": {
                "sleep": "7-9 hours of quality sleep",
                "stress": "Seek professional help for stress management",
                "hydration": "Drink 12-16 glasses of water daily",
                "habits": "Work with healthcare provider for lifestyle changes"
            }
        }
        
        return recommendations.get(bmi_category, recommendations["normal"]) 