import re
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent

class ParentAgent:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        self.cache = {}  # Response cache: {place_name: {data, timestamp}}
        self.cache_duration = 3600  # Cache for 1 hour (3600 seconds)
    
    def extract_place(self, user_input):
        """
        Extract place name from user input (case insensitive)
        """
        # Common patterns for place extraction (case insensitive)
        patterns = [
            r'(?:going to|visit|plan.*trip.*to|travel to|trip to)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s*(?:and|what|let|,|\.|$)',
            r'([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s+(?:weather|temperature)',
            r'(?:weather|temperature)\s+(?:in|at|for)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)',
            r'(?:what\'?s?|what is)\s+(?:in|at)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)',
            r'(?:in|at)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s+(?:and|what|is|are|it|these)',
            r'(?:to)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)\s*(?:,|\?|and|what|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                # Clean up common words
                place = re.sub(r'\b(the|a|an|to|is|are)\b', '', place, flags=re.IGNORECASE).strip()
                # Capitalize first letter of each word
                place = place.title()
                if place and len(place) > 1:
                    return place
        
        # Fallback: look for potential place names
        words = user_input.split()
        skip_words = {'i', "i'm", 'im', 'what', 'and', 'the', 'is', 'are', 'can', 'will', 'there', 'these', 'those', 'my', 'trip', 'plan', 'going', 'to', 'visit', 'lets', 'let'}
        
        for i, word in enumerate(words):
            word_clean = word.strip('.,?!')
            if word_clean and len(word_clean) >= 2 and word_clean.lower() not in skip_words:
                # Try to get 1-2 word place names
                place = word_clean
                if i + 1 < len(words):
                    next_word = words[i + 1].strip('.,?!')
                    if next_word and len(next_word) >= 2 and next_word.lower() not in skip_words:
                        place += ' ' + next_word
                return place.title()
        
        return None
    
    def detect_intent(self, user_input):
        """
        Detect user intent: weather, places, or both
        """
        user_input_lower = user_input.lower()
        
        weather_keywords = ['weather', 'temperature', 'rain', 'forecast', 'climate', 'hot', 'cold']
        places_keywords = ['places', 'visit', 'attractions', 'tourist', 'sightseeing', 'plan', 'trip', 'go to']
        
        has_weather = any(keyword in user_input_lower for keyword in weather_keywords)
        has_places = any(keyword in user_input_lower for keyword in places_keywords)
        
        if has_weather and has_places:
            return 'both'
        elif has_weather:
            return 'weather'
        elif has_places:
            return 'places'
        else:
            # Default to places if planning a trip
            return 'places'
    
    def format_response(self, place, intent, weather_data=None, places_data=None):
        """
        Format the final polished response based on intent and data
        """
        response = ""
        
        # Format weather information with polished descriptions
        if intent in ['weather', 'both'] and weather_data:
            temp = weather_data.get('temperature')
            rain = weather_data.get('rain_chance', 0)
            
            # Polished weather description
            if rain > 70:
                rain_desc = "high chance of rain"
            elif rain > 40:
                rain_desc = "moderate chance of rain"
            elif rain > 0:
                rain_desc = f"{rain}% chance of rain"
            else:
                rain_desc = "clear skies"
            
            response += f"In {place}, it's currently {temp}°C with {rain_desc}."
        
        # Format places information
        if intent in ['places', 'both'] and places_data:
            attractions = places_data.get('attractions', [])
            
            if response:
                response += " And these are the places you can visit:"
            else:
                response += f"In {place}, these are the places you can visit:"
            
            if attractions:
                for attraction in attractions:
                    # Handle both old format (strings) and new format (dicts with distance)
                    if isinstance(attraction, dict):
                        name = attraction['name']
                        distance = attraction['distance']
                        response += f"\n- {name} - {distance} km away"
                    else:
                        response += f"\n- {attraction}"
            else:
                response += f"\n- Unfortunately, I couldn't find popular tourist attractions for {place} in my database. This might be a smaller city or the tourism data isn't available yet."
        
        return response
    
    def _is_cache_valid(self, place):
        """Check if cached data is still valid"""
        import time
        if place not in self.cache:
            return False
        cache_time = self.cache[place].get('timestamp', 0)
        return (time.time() - cache_time) < self.cache_duration
    
    def process_query(self, user_input):
        """
        Main method to process user query with robust error handling and caching
        """
        import time
        try:
            # Extract place
            place = self.extract_place(user_input)
            
            if not place:
                return {
                    'success': False,
                    'message': "Please mention a specific place name. For example: 'I'm going to Bangalore' or 'Weather in Paris'."
                }
            
            # Detect intent
            intent = self.detect_intent(user_input)
            
            # Check cache first
            cache_key = place.lower()
            if self._is_cache_valid(cache_key):
                cached_data = self.cache[cache_key]
                # Re-format response based on current intent
                message = self.format_response(
                    place, intent, 
                    cached_data.get('weather_data'),
                    cached_data.get('places_data')
                )
                return {
                    'success': True,
                    'message': message,
                    'place': place,
                    'intent': intent,
                    'cached': True
                }
            
            # Get coordinates first (needed for both weather and places)
            coord_result = self.places_agent.get_coordinates(place)
            
            if not coord_result['success']:
                # Check for spelling suggestions
                suggestions = coord_result.get('suggestions', [])
                if suggestions:
                    suggestion_text = f" Did you mean '{suggestions[0]}'?"
                else:
                    suggestion_text = " Please check the spelling and try again."
                
                return {
                    'success': False,
                    'message': f"Sorry, I couldn't find '{place}'.{suggestion_text}"
                }
            
            lat = coord_result['lat']
            lon = coord_result['lon']
            
            weather_data = None
            places_data = None
            error_messages = []
            
            # Get weather if needed
            if intent in ['weather', 'both']:
                weather_result = self.weather_agent.get_weather(lat, lon)
                if weather_result['success']:
                    weather_data = weather_result
                else:
                    error_messages.append(weather_result.get('error', 'Weather unavailable'))
            
            # Get places if needed
            if intent in ['places', 'both']:
                attractions_result = self.places_agent.get_attractions(lat, lon)
                if attractions_result['success']:
                    places_data = attractions_result
                else:
                    error_messages.append(attractions_result.get('error', 'Places unavailable'))
            
            # Check if we got any data
            if not weather_data and not places_data:
                return {
                    'success': False,
                    'message': f"Unable to fetch information for {place}. {' '.join(error_messages)}"
                }
            
            # Store in cache for future requests
            self.cache[cache_key] = {
                'weather_data': weather_data,
                'places_data': places_data,
                'timestamp': time.time()
            }
            
            # Format response
            message = self.format_response(place, intent, weather_data, places_data)
            
            return {
                'success': True,
                'message': message,
                'place': place,
                'intent': intent,
                'cached': False
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'An unexpected error occurred. Please try again later.'
            }
