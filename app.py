"""
Flask API server for RecipeSnap - Recipe Extractor
Provides REST API endpoints for recipe extraction
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from recipe_extractor import RecipeExtractor
from recipe_searcher import RecipeSearcher
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
# Enable CORS for frontend - allow GitHub Pages and localhost
CORS(app, origins=[
    "https://angusyang91.github.io",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:*",
    "http://127.0.0.1:*"
], supports_credentials=True)

# Initialize recipe extractor
try:
    extractor = RecipeExtractor()
except ValueError as e:
    print(f"Warning: {e}")
    extractor = None

# Initialize recipe searcher
try:
    searcher = RecipeSearcher()
except ValueError as e:
    print(f"Warning: {e}")
    searcher = None


@app.route('/')
def index():
    """Serve the main web interface"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'extractor_ready': extractor is not None
    })


@app.route('/api/extract', methods=['POST'])
def extract_recipe():
    """
    Extract recipe from URL
    
    Request body:
    {
        "url": "https://example.com/recipe"
    }
    
    Returns:
    {
        "success": true,
        "recipe": {...},
        "error": null
    }
    """
    if extractor is None:
        return jsonify({
            'success': False,
            'error': 'Recipe extractor not initialized. Please check WRITER_API_KEY environment variable.',
            'recipe': None
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: url',
                'recipe': None
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL cannot be empty',
                'recipe': None
            }), 400
        
        # Extract recipe
        recipe = extractor.extract_recipe(url)
        
        return jsonify({
            'success': True,
            'recipe': recipe,
            'error': None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'recipe': None
        }), 500


@app.route('/api/search', methods=['POST'])
def search_recipes():
    """
    Search for recipes

    Request body:
    {
        "query": "chocolate chip cookies",
        "num_results": 5  (optional, default 5)
    }

    Returns:
    {
        "success": true,
        "results": [
            {
                "title": "Recipe Title",
                "url": "https://...",
                "snippet": "Description...",
                "site": "example.com"
            },
            ...
        ],
        "error": null
    }
    """
    if searcher is None:
        return jsonify({
            'success': False,
            'error': 'Recipe searcher not initialized. Please check GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.',
            'results': []
        }), 500

    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: query',
                'results': []
            }), 400

        query = data['query'].strip()
        num_results = data.get('num_results', 5)

        if not query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty',
                'results': []
            }), 400

        # Search for recipes
        results = searcher.search_recipes(query, num_results=num_results)

        return jsonify({
            'success': True,
            'results': results,
            'error': None
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500


@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with sample data"""
    return jsonify({
        'success': True,
        'message': 'API is working!',
        'extractor_ready': extractor is not None,
        'searcher_ready': searcher is not None
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # For production, use gunicorn or waitress
    # For development, use Flask's built-in server
    if os.environ.get('RENDER') or os.environ.get('PRODUCTION'):
        # Production mode - use waitress for better performance
        try:
            from waitress import serve
            serve(app, host='0.0.0.0', port=port)
        except ImportError:
            # Fallback to Flask server if waitress not available
            app.run(host='0.0.0.0', port=port, debug=False)
    else:
        app.run(host='0.0.0.0', port=port, debug=debug)

