"""
RecipeSnap - Recipe Searcher
Searches for recipes using Google Custom Search API
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()


class RecipeSearcher:
    """Searches for recipes using Google Custom Search API."""

    def __init__(self, api_key=None, search_engine_id=None):
        """
        Initialize the recipe searcher.

        Args:
            api_key (str): Google Custom Search API key. If not provided, reads from GOOGLE_API_KEY env var.
            search_engine_id (str): Google Custom Search Engine ID. If not provided, reads from GOOGLE_CSE_ID env var.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = search_engine_id or os.getenv('GOOGLE_CSE_ID')

        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        if not self.search_engine_id:
            raise ValueError("Google Custom Search Engine ID is required. Set GOOGLE_CSE_ID environment variable.")

        # Google Custom Search API endpoint
        self.api_url = "https://www.googleapis.com/customsearch/v1"

        # Popular recipe sites to prioritize in search
        self.recipe_sites = [
            "allrecipes.com",
            "foodnetwork.com",
            "seriouseats.com",
            "bonappetit.com",
            "epicurious.com",
            "tasty.co",
            "delish.com",
            "simplyrecipes.com",
            "thekitchn.com",
            "cookieandkate.com"
        ]

        # Simple in-memory cache with timestamps
        # Format: {query: {'results': [...], 'timestamp': time}}
        self._cache = {}
        self._cache_duration = 3600  # Cache for 1 hour (3600 seconds)

    def search_recipes(self, query, num_results=5):
        """
        Search for recipes using Google Custom Search.

        Args:
            query (str): The recipe search query (e.g., "chocolate chip cookies")
            num_results (int): Number of results to return (default 5, max 10)

        Returns:
            list: List of recipe search results with format:
            [
                {
                    "title": str,
                    "url": str,
                    "snippet": str,
                    "site": str
                },
                ...
            ]
        """
        print(f"🔍 Searching for recipes: {query}")

        # Normalize query for cache key
        cache_key = f"{query.lower().strip()}:{num_results}"

        # Check cache first
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            # Check if cache is still valid (within 1 hour)
            if time.time() - cached_data['timestamp'] < self._cache_duration:
                print(f"✅ Returning cached results for '{query}'")
                return cached_data['results']
            else:
                # Cache expired, remove it
                del self._cache[cache_key]

        # Limit results to max 10
        num_results = min(num_results, 10)

        # Build search query to focus on recipes
        search_query = f"{query} recipe"

        try:
            # Make API request to Google Custom Search
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': search_query,
                'num': num_results
            }

            response = requests.get(self.api_url, params=params, timeout=10)

            # Handle API errors
            if response.status_code != 200:
                error_msg = f"Google Search API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error'].get('message', '')}"
                except:
                    error_msg += f" - {response.text[:200]}"
                raise Exception(error_msg)

            data = response.json()

            # Extract search results
            results = []
            if 'items' in data:
                for item in data['items']:
                    # Extract domain from URL
                    url = item.get('link', '')
                    domain = url.split('/')[2] if len(url.split('/')) > 2 else ''

                    result = {
                        'title': item.get('title', 'Untitled Recipe'),
                        'url': url,
                        'snippet': item.get('snippet', ''),
                        'site': domain
                    }
                    results.append(result)

            print(f"✓ Found {len(results)} recipe results")

            # Cache the results
            self._cache[cache_key] = {
                'results': results,
                'timestamp': time.time()
            }
            print(f"💾 Cached results for '{query}'")

            return results

        except Exception as e:
            print(f"Search error: {str(e)}")
            raise Exception(f"Recipe search failed: {str(e)}")


def main():
    """
    Main function for testing the recipe searcher.
    """
    try:
        searcher = RecipeSearcher()

        # Test search
        query = "chocolate chip cookies"
        print(f"\nSearching for: {query}")
        print("="*80)

        results = searcher.search_recipes(query, num_results=5)

        print(f"\nSearch Results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Site: {result['site']}")
            print(f"   Snippet: {result['snippet'][:100]}...")

    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set GOOGLE_API_KEY and GOOGLE_CSE_ID in a .env file")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
