import requests
import time

class PlacesAgent:
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        self.headers = {
            'User-Agent': 'TourismAI/1.0'
        }
    
    def get_coordinates(self, place_name):
        """
        Get coordinates for a place using Nominatim API with spelling suggestions
        Returns: dict with lat, lon or error with suggestions
        """
        try:
            params = {
                'q': place_name,
                'format': 'json',
                'limit': 5  # Get multiple results for suggestions
            }
            
            response = requests.get(
                self.nominatim_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if not data:
                # Try fuzzy search with common misspellings
                suggestions = self._get_spelling_suggestions(place_name)
                return {
                    'success': False,
                    'error': f"Place '{place_name}' not found",
                    'suggestions': suggestions
                }
            
            return {
                'success': True,
                'lat': float(data[0]['lat']),
                'lon': float(data[0]['lon']),
                'display_name': data[0].get('display_name', place_name)
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Connection timeout. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Network error. Please check your internet connection.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unable to locate the place. Please try again."
            }
    
    def get_attractions(self, lat, lon, radius=15000):
        """
        Get tourist attractions using Overpass API
        Returns: list of up to 5 attractions
        """
        try:
            # Overpass query to find famous tourist attractions (excluding hotels/lodges)
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["tourism"="attraction"](around:{radius},{lat},{lon});
              way["tourism"="attraction"](around:{radius},{lat},{lon});
              node["tourism"="museum"](around:{radius},{lat},{lon});
              way["tourism"="museum"](around:{radius},{lat},{lon});
              node["historic"]["historic"!="wayside_shrine"](around:{radius},{lat},{lon});
              way["historic"]["historic"!="wayside_shrine"](around:{radius},{lat},{lon});
              node["leisure"="park"](around:{radius},{lat},{lon});
              way["leisure"="park"](around:{radius},{lat},{lon});
              node["leisure"="garden"](around:{radius},{lat},{lon});
              way["leisure"="garden"](around:{radius},{lat},{lon});
              node["amenity"="place_of_worship"]["religion"="hindu"](around:{radius},{lat},{lon});
              way["amenity"="place_of_worship"]["religion"="hindu"](around:{radius},{lat},{lon});
              node["amenity"="place_of_worship"]["religion"="buddhist"](around:{radius},{lat},{lon});
              way["amenity"="place_of_worship"]["religion"="buddhist"](around:{radius},{lat},{lon});
              node["natural"="waterfall"](around:{radius},{lat},{lon});
              node["natural"="peak"](around:{radius},{lat},{lon});
              node["tourism"="viewpoint"](around:{radius},{lat},{lon});
              way["tourism"="zoo"](around:{radius},{lat},{lon});
              node["tourism"="zoo"](around:{radius},{lat},{lon});
            );
            out center 30;
            """
            
            response = requests.post(
                self.overpass_url,
                data={'data': overpass_query},
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract and rank attraction names (exclude hotels, lodges)
            attractions_with_scores = []
            seen_names = set()
            
            # Keywords to exclude (hotels, lodges, etc.)
            exclude_keywords = [
                'hotel', 'lodge', 'resort', 'inn', 'guest house', 'guesthouse',
                'homestay', 'hostel', 'motel', 'accommodation', 'stay', 'rooms'
            ]
            
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                name = tags.get('name')
                tourism_type = tags.get('tourism', '')
                
                # Skip if no name or if it's a hotel/accommodation
                if not name:
                    continue
                    
                if tourism_type in ['hotel', 'motel', 'guest_house', 'hostel', 'apartment']:
                    continue
                
                # Check if name contains hotel/lodge keywords
                name_lower = name.lower()
                if any(keyword in name_lower for keyword in exclude_keywords):
                    continue
                
                # Score attractions by importance
                score = 0
                
                # Higher score for important tourism tags
                if tourism_type in ['attraction', 'museum', 'viewpoint', 'zoo']:
                    score += 3
                if tags.get('historic'):
                    score += 2
                if tags.get('wikipedia') or tags.get('wikidata'):
                    score += 3  # Has Wikipedia page = famous
                if tags.get('heritage'):
                    score += 2
                if 'national' in name_lower or 'palace' in name_lower:
                    score += 2
                if tags.get('leisure') in ['park', 'garden']:
                    score += 1
                
                # Add unique attractions with score
                if name not in seen_names:
                    attractions_with_scores.append((name, score))
                    seen_names.add(name)
            
            # Sort by score (highest first) and take top 5
            attractions_with_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Calculate distance from center for each attraction
            from math import radians, cos, sin, asin, sqrt
            
            def haversine(lon1, lat1, lon2, lat2):
                """Calculate distance between two points in km"""
                lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                km = 6371 * c
                return round(km, 1)
            
            attractions_with_distance = []
            for name, score in attractions_with_scores[:5]:
                # Find the element with this name to get its coordinates
                for element in data.get('elements', []):
                    if element.get('tags', {}).get('name') == name:
                        # Get attraction coordinates
                        if 'lat' in element and 'lon' in element:
                            attr_lat = element['lat']
                            attr_lon = element['lon']
                        elif 'center' in element:
                            attr_lat = element['center']['lat']
                            attr_lon = element['center']['lon']
                        else:
                            continue
                        
                        distance = haversine(lon, lat, attr_lon, attr_lat)
                        attractions_with_distance.append({
                            'name': name,
                            'distance': distance
                        })
                        break
            
            return {
                'success': True,
                'attractions': attractions_with_distance
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"Places API error: {str(e)}"
            }
    
    def _get_spelling_suggestions(self, place_name):
        """
        Get spelling suggestions for misspelled places
        """
        # Common Karnataka city corrections
        corrections = {
            'banglore': 'Bangalore',
            'bangaluru': 'Bangalore',
            'bangelore': 'Bangalore',
            'bangeluru': 'Bangalore',
            'mysuru': 'Mysore',
            'mysooru': 'Mysore',
            'mangaluru': 'Mangalore',
            'mangalor': 'Mangalore',
            'huballi': 'Hubli',
        }
        
        place_lower = place_name.lower()
        if place_lower in corrections:
            return [corrections[place_lower]]
        return []
    
    def get_places(self, place_name):
        """
        Main method to get attractions for a place with error handling
        """
        # First get coordinates
        coord_result = self.get_coordinates(place_name)
        
        if not coord_result['success']:
            return coord_result
        
        # Small delay to respect API rate limits
        time.sleep(0.5)
        
        # Then get attractions
        try:
            attractions_result = self.get_attractions(
                coord_result['lat'], 
                coord_result['lon']
            )
            
            if not attractions_result['success']:
                return attractions_result
            
            return {
                'success': True,
                'lat': coord_result['lat'],
                'lon': coord_result['lon'],
                'attractions': attractions_result['attractions']
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Unable to fetch attractions. Please try again.'
            }
