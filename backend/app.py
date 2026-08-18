from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.parent_agent import ParentAgent
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS based on environment
if Config.FLASK_ENV == 'production':
    CORS(app, resources={r"/*": {"origins": Config.FRONTEND_URL}})
else:
    CORS(app)

parent_agent = ParentAgent()

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_input = data.get('query', '')
        
        if not user_input:
            logger.warning("Empty query received")
            return jsonify({'error': 'No query provided'}), 400
        
        logger.info(f"Processing query: {user_input}")
        result = parent_agent.process_query(user_input)
        logger.info(f"Query processed successfully")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'environment': Config.FLASK_ENV})

if __name__ == '__main__':
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=Config.PORT
    )
