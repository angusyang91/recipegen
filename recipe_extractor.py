"""
RecipeSnap - Recipe Extractor
This script extracts recipes from URLs using AI, matching the output format from the Recipes repo.
Uses Writer's Palmyra X5 API.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RecipeExtractor:
    """Extracts and formats recipes from URLs using AI."""
    
    def __init__(self, api_key=None):
        """
        Initialize the recipe extractor.
        
        Args:
            api_key (str): Writer API key. If not provided, reads from WRITER_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('WRITER_API_KEY')
        if not self.api_key:
            raise ValueError("Writer API key is required. Set WRITER_API_KEY environment variable.")
        
        # Writer API endpoint
        self.api_url = "https://api.writer.com/v1/chat"
        self.model = "palmyra-x5"
    
    def extract_recipe(self, url):
        """
        Extract recipe from URL using AI.
        Matches the output format from the Recipes repo.
        
        Args:
            url (str): The recipe URL to extract
            
        Returns:
            dict: Structured recipe data with format:
            {
                "recipeName": str,
                "ingredients": [str, ...],
                "instructions": [str, ...],
                "applianceInstructions": [
                    {
                        "applianceName": str,
                        "instructions": [str, ...]
                    }
                ]
            }
        """
        print(f"Extracting recipe from: {url}")
        
        # Prompt matching the Recipes repo approach
        appliance_prompt_section = """
After extracting the main instructions, please analyze them.
1. If the recipe involves using a pressure cooker, add a set of specific, alternative instructions under the appliance name "Instant Pot" in the "applianceInstructions" field.
2. If the recipe involves baking or air frying, add a set of specific, alternative instructions under the appliance name "Breville Smart Oven Toaster Pro" in the "applianceInstructions" field.

If neither of these conditions are met, the "applianceInstructions" field MUST be an empty array [].
"""

        prompt = f"""From the URL: {url}, extract the recipe name, the ingredients, and the primary cooking instructions.
{appliance_prompt_section}
Ignore all non-recipe content like stories, ads, and comments.

Return ONLY a valid JSON object with this exact structure:
{{
  "recipeName": "Recipe Name",
  "ingredients": [
    "1 cup flour",
    "2 eggs",
    ...
  ],
  "instructions": [
    "Step 1: ...",
    "Step 2: ...",
    ...
  ],
  "applianceInstructions": [
    {{
      "applianceName": "Instant Pot",
      "instructions": ["Step 1: ...", "Step 2: ..."]
    }}
  ]
}}

Important:
- Clean up and standardize ingredient measurements
- Make instructions clear and actionable
- Number the instructions if they aren't already numbered
- Only include applianceInstructions if the recipe can be adapted for Instant Pot or Breville Smart Oven
- Return ONLY valid JSON, no other text"""

        try:
            # Make API request to Writer's Palmyra X5
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"content": prompt, "role": "user"}
                ]
            }
            
            print(f"Using model: {self.model}")
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            # Handle API errors
            if response.status_code != 200:
                error_msg = f"Writer API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']}"
                    elif "message" in error_data:
                        error_msg += f" - {error_data['message']}"
                except:
                    error_msg += f" - {response.text[:200]}"
                raise Exception(error_msg)
            
            response_data = response.json()
            
            # Extract the response text from Writer API response
            # Writer API response structure may vary, so we handle different formats
            response_text = None
            
            # Try different possible response structures
            if "choices" in response_data and len(response_data["choices"]) > 0:
                # OpenAI-style format
                choice = response_data["choices"][0]
                if "message" in choice:
                    response_text = choice["message"].get("content", "").strip()
                elif "text" in choice:
                    response_text = choice["text"].strip()
                elif "content" in choice:
                    response_text = choice["content"].strip()
            elif "message" in response_data:
                # Direct message format
                if isinstance(response_data["message"], dict):
                    response_text = response_data["message"].get("content", "").strip()
                else:
                    response_text = str(response_data["message"]).strip()
            elif "content" in response_data:
                # Direct content format
                response_text = response_data["content"].strip()
            elif "text" in response_data:
                # Direct text format
                response_text = response_data["text"].strip()
            elif "output" in response_data:
                # Output field format
                response_text = response_data["output"].strip()
            
            if not response_text:
                # Last resort: try to find any string field
                for key, value in response_data.items():
                    if isinstance(value, str) and len(value) > 10:
                        response_text = value.strip()
                        break
                
                if not response_text:
                    raise Exception(f"Could not extract response text from Writer API. Response structure: {list(response_data.keys())}")
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                # Find the first ``` and last ```
                parts = response_text.split("```")
                if len(parts) >= 3:
                    response_text = parts[1]  # Get content between first two ```
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                else:
                    response_text = response_text.replace("```json", "").replace("```", "")
                response_text = response_text.strip()
            
            # Try to parse JSON
            try:
                recipe_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If parsing fails, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        recipe_data = json.loads(json_match.group())
                    except:
                        # Last resort: return empty structure
                        print(f"Warning: Could not parse JSON from response. Returning empty structure.")
                        recipe_data = {
                            "recipeName": None,
                            "ingredients": [],
                            "instructions": [],
                            "applianceInstructions": []
                        }
                else:
                    # No JSON found, return empty structure
                    print(f"Warning: No JSON found in AI response. Response: {response_text[:200]}")
                    recipe_data = {
                        "recipeName": None,
                        "ingredients": [],
                        "instructions": [],
                        "applianceInstructions": []
                    }
            
            # Ensure all required fields exist
            if 'recipeName' not in recipe_data:
                recipe_data['recipeName'] = recipe_data.get('title') or None
            if 'ingredients' not in recipe_data:
                recipe_data['ingredients'] = []
            if 'instructions' not in recipe_data:
                recipe_data['instructions'] = recipe_data.get('directions') or []
            if 'applianceInstructions' not in recipe_data:
                recipe_data['applianceInstructions'] = []
            
            # Ensure applianceInstructions is a list
            if not isinstance(recipe_data.get('applianceInstructions'), list):
                recipe_data['applianceInstructions'] = []
            
            print(f"✓ Successfully extracted: {recipe_data.get('recipeName', 'Unknown')}")
            return recipe_data
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error. Response was: {response_text[:500]}")
            # Return empty structure instead of raising
            return {
                "recipeName": None,
                "ingredients": [],
                "instructions": [],
                "applianceInstructions": []
            }
        except Exception as e:
            print(f"AI extraction error: {str(e)}")
            raise Exception(f"AI extraction failed: {str(e)}")


def main():
    """
    Main function for testing the recipe extractor.
    Run this script directly to test recipe extraction.
    """
    # Example usage
    test_urls = [
        "https://www.seriouseats.com/the-best-chili-recipe",
        # Add more test URLs here
    ]
    
    try:
        extractor = RecipeExtractor()
        
        for url in test_urls:
            print("\n" + "="*80)
            recipe = extractor.extract_recipe(url)
            
            # Pretty print the recipe
            print("\nExtracted Recipe:")
            print(json.dumps(recipe, indent=2))
            print("="*80)
            
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your WRITER_API_KEY in a .env file")
        print("Copy .env.example to .env and add your API key")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
