from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.home, name='home'),
    path('get-advice/', views.get_health_advice, name='get_health_advice'),
    path('save-profile/', views.save_user_profile, name='save_user_profile'),
    path('profiles/', views.user_profiles, name='user_profiles'),
] 