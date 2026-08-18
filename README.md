# Tourist AI - Multi-Agent Tourism Planning System

A smart tourism planning system built with a multi-agent architecture that provides weather information and tourist attraction recommendations using natural language queries.

## 🌟 Features

- **Multi-Agent System**: Parent Agent orchestrates Weather and Places agents
- **Natural Language Processing**: Understands conversational queries
- **Weather Information**: Real-time weather data from Open-Meteo API
- **Tourist Attractions**: Curated attractions with distance calculations
- **Smart Caching**: 56% faster response times for repeated queries
- **Attraction Ranking**: Prioritizes museums, monuments, and popular sites
- **Spelling Correction**: Suggests corrections for misspelled city names
- **Distance Display**: Shows distances from city center for trip planning

## 🏗️ Architecture

### Backend (Flask)
- **Parent Agent**: Intent detection, place extraction, response orchestration
- **Weather Agent**: Fetches weather data from Open-Meteo API
- **Places Agent**: Geocoding (Nominatim) and attraction discovery (Overpass API)

### Frontend (React)
- Clean, responsive UI with example queries
- Real-time loading states and error handling
- Formatted results display with weather and attraction lists

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## 🚀 Local Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from example:
```bash
copy .env.example .env  # Windows
```

5. Start the Flask server:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
copy .env.example .env  # Windows
```

4. Start the development server:
```bash
npm start
```

Frontend will open at `http://localhost:3000`

## 🎯 Usage

Try these example queries:
- "What's the weather in Bangalore?"
- "Show me places to visit in Paris"
- "I'm going to Tokyo, plan my trip"
- "Tell me about Mysore and its weather"

## 📁 Project Structure

```
tourist-ai/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── parent_agent.py
│   │   ├── weather_agent.py
│   │   └── places_agent.py
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env.production
│   └── Procfile
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputBox.jsx
│   │   │   ├── InputBox.css
│   │   │   ├── ResultBox.jsx
│   │   │   └── ResultBox.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env.example
│
└── README.md
```

## 🚢 Deployment

### Backend Deployment (Heroku/Render)

1. Update `.env.production` with your production values
2. Set environment variables in your hosting platform
3. Deploy using Procfile (configured for Gunicorn)

**Environment Variables:**
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `PORT=5000`
- `FRONTEND_URL=https://your-frontend-domain.com`
- `CACHE_TTL=3600`

### Frontend Deployment (Vercel/Netlify)

1. Build the production bundle:
```bash
npm run build
```

2. Set environment variable:
- `REACT_APP_API_URL=https://your-backend-domain.com`

3. Deploy the `build` folder to your hosting platform

## 🔧 Configuration

### Backend (config.py)
- `CACHE_TTL`: Cache duration in seconds (default: 3600)
- `FRONTEND_URL`: CORS allowed origin
- API endpoints are pre-configured for Open-Meteo, Nominatim, and Overpass

### Frontend (.env)
- `REACT_APP_API_URL`: Backend API URL

## 🧪 Testing

Test backend API directly:
```powershell
$body = @{query="Show me places in Bangalore"} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/query -Method POST -Body $body -ContentType "application/json"
```

## 📊 Performance

- **Cache Hit**: ~2 seconds (56% faster)
- **Cache Miss**: ~4.5 seconds
- **Cache Duration**: 1 hour (configurable)

## 🛠️ Technologies

**Backend:**
- Flask 3.0.0
- flask-cors 4.0.0
- requests 2.31.0
- python-dotenv 1.0.0
- gunicorn 21.2.0

**Frontend:**
- React 18.2.0
- axios 1.6.0
- react-scripts 5.0.1

**APIs:**
- Open-Meteo API (Weather)
- Nominatim API (Geocoding)
- Overpass API (POI Data)

## 📝 Features Explained

### Intent Detection
Detects whether user wants:
- Weather information only
- Places information only
- Both weather and places

### Place Extraction
- Regex-based extraction with multiple patterns
- Case-insensitive matching
- Handles "and" as delimiter (e.g., "Tokyo and weather")

### Spelling Corrections
Common misspellings mapped to correct names:
- "Bangeluru" → "Bangalore"
- "Bangaluru" → "Bangalore"
- "Mysuru" → "Mysore"

### Attraction Filtering
Excludes:
- Hotels, lodges, resorts
- Accommodations and hostels

Prioritizes:
- Museums and monuments
- Historic sites
- Tourism attractions
- Places with Wikipedia articles

### Distance Calculation
Uses Haversine formula to calculate distance from city center to each attraction.

## 🤝 Contributing

This is an academic project. For improvements, please follow standard pull request procedures.

## 📄 License

Academic project - All rights reserved.

## 👤 Author

Created for Tourism Planning System assignment.

---

**Note**: Make sure to update API URLs and CORS settings before deploying to production.
