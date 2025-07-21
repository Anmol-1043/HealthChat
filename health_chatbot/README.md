# Health Advice Chatbot API

A FastAPI-based health advice chatbot that provides personalized diet, exercise, and lifestyle recommendations based on user input (weight, height, age, activity level, etc.) using a local LLM (GPT4All).

## Features

- **Personalized Health Advice**: Get customized diet, exercise, and lifestyle recommendations
- **BMI Calculation**: Automatic BMI calculation and categorization
- **Calorie Needs**: Calculate daily calorie requirements based on activity level
- **Local LLM Integration**: Uses GPT4All for generating natural language health advice
- **User Profile Management**: Store and manage user profiles
- **Advice History**: Track and retrieve previous health advice
- **RESTful API**: Clean, documented API endpoints

## Project Structure

```
health_chatbot/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── models/                # Database models and Pydantic schemas
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   └── schemas.py         # Pydantic schemas
├── database/              # Database configuration
│   ├── __init__.py
│   └── database.py        # SQLAlchemy setup
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── health_advice.py   # Health advice endpoints
│   └── user_profile.py    # User profile endpoints
└── services/              # Business logic services
    ├── __init__.py
    ├── health_service.py  # Health calculations and recommendations
    └── llm_service.py     # LLM integration for advice generation
```

## Installation

1. **Clone or create the project directory**
   ```bash
   mkdir health_chatbot
   cd health_chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

   The API will be available at `http://localhost:8001`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8001/docs`
- **ReDoc documentation**: `http://localhost:8001/redoc`

## API Endpoints

### Health Advice
- `POST /api/health-advice/` - Get personalized health advice
- `GET /api/health-advice/history/{user_id}` - Get advice history
- `POST /api/health-advice/save/` - Save advice to database

### User Profiles
- `POST /api/user-profile/` - Create user profile
- `GET /api/user-profile/{profile_id}` - Get user profile
- `GET /api/user-profiles/` - Get all user profiles
- `PUT /api/user-profile/{profile_id}` - Update user profile
- `DELETE /api/user-profile/{profile_id}` - Delete user profile

## Usage Examples

### Get Health Advice

```python
import requests

# Example request
data = {
    "weight": 70.0,
    "height": 175.0,
    "age": 30,
    "gender": "male",
    "activity_level": "moderate",
    "daily_routine": "Office job, some walking",
    "goals": "weight_loss",
    "medical_conditions": "None"
}

response = requests.post("http://localhost:8001/api/health-advice/", json=data)
advice = response.json()
print(advice)
```

### Create User Profile

```python
profile_data = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.0,
    "height": 175.0,
    "gender": "male",
    "activity_level": "moderate",
    "daily_routine": "Office job, some walking",
    "goals": "weight_loss"
}

response = requests.post("http://localhost:8001/api/user-profile/", json=profile_data)
profile = response.json()
print(profile)
```

## LLM Configuration

The application uses GPT4All for generating health advice. The model will be automatically downloaded on first use.

### Available Models
- `ggml-gpt4all-j-v1.3-groovy` (default)
- `ggml-gpt4all-j-v1.2-jazzy`
- `ggml-gpt4all-j-v1.1-breezy`

To change the model, modify the `model_name` parameter in `services/llm_service.py`.

## Health Calculations

The application provides:
- **BMI Calculation**: Weight (kg) / Height (m)²
- **BMR Calculation**: Mifflin-St Jeor Equation
- **Calorie Needs**: BMR × Activity Multiplier
- **BMI Categories**: Underweight, Normal, Overweight, Obese

## Error Handling

The application includes comprehensive error handling:
- Input validation using Pydantic schemas
- Graceful fallback when LLM is unavailable
- Proper HTTP status codes and error messages
- Logging for debugging

## Development

### Adding New Features
1. Create new models in `models/models.py`
2. Add corresponding schemas in `models/schemas.py`
3. Create service methods in appropriate service files
4. Add API endpoints in router files
5. Update documentation

### Testing
```bash
# Run with auto-reload for development
uvicorn main:app --reload

# Run tests (when implemented)
pytest
```

## Dependencies

- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **GPT4All**: Local LLM integration
- **Uvicorn**: ASGI server

## License

This project is for educational purposes. Please consult healthcare professionals for medical advice.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository. 