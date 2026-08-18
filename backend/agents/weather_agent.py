import requests

class WeatherAgent:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, lat, lon):
        """
        Fetch weather data for given coordinates using Open-Meteo API
        Returns: dict with temperature and rain_chance
        """
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,precipitation_probability',
                'temperature_unit': 'celsius'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract current weather data
            current = data.get('current', {})
            temperature = current.get('temperature_2m')
            rain_chance = current.get('precipitation_probability', 0)
            
            if temperature is None:
                return {
                    'success': False,
                    'error': 'Weather data not available for this location.'
                }
            
            return {
                'success': True,
                'temperature': temperature,
                'rain_chance': rain_chance
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Weather service timeout. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Unable to connect to weather service.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Weather information temporarily unavailable.'
            }
