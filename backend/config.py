import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Cache settings
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour default
    
    # API URLs
    WEATHER_API = 'https://api.open-meteo.com/v1/forecast'
    NOMINATIM_API = 'https://nominatim.openstreetmap.org/search'
    OVERPASS_API = 'https://overpass-api.de/api/interpreter'
