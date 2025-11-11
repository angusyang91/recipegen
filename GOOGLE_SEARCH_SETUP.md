# Setting Up Google Custom Search API

The recipe search feature uses Google Custom Search API to find recipes. Follow these steps to set it up.

## Step 1: Get a Google API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Custom Search API**:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search for "Custom Search API"
   - Click "Enable"
4. Create API credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy your API key (it will look like: `AIzaSy...`)
5. **Optional but recommended**: Restrict your API key:
   - Click on your API key to edit it
   - Under "API restrictions", select "Restrict key"
   - Choose "Custom Search API"
   - Save

## Step 2: Create a Custom Search Engine

1. Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click "Add" or "Create a new search engine"
3. Configure your search engine:
   - **Sites to search**: Enter `*.com` (to search across all .com sites)
   - Or list specific recipe sites like:
     - `allrecipes.com`
     - `foodnetwork.com`
     - `seriouseats.com`
     - `bonappetit.com`
4. Click "Create"
5. On the next page, click "Customize" or "Control Panel"
6. Under "Basic" settings:
   - Find your **Search engine ID** (looks like: `01234567890abcdef`)
   - Copy this ID
7. Enable "Search the entire web":
   - Go to "Setup" tab
   - Turn ON "Search the entire web"
   - Save

## Step 3: Add to Render Environment Variables

1. Go to your Render dashboard: https://dashboard.render.com
2. Select your RecipeSnap service
3. Click **Environment** in the left sidebar
4. Add these two new environment variables:
   - **Key**: `GOOGLE_API_KEY`
     **Value**: Your Google API key from Step 1 (e.g., `AIzaSy...`)
   - **Key**: `GOOGLE_CSE_ID`
     **Value**: Your Search Engine ID from Step 2 (e.g., `01234567890abcdef`)
5. Click **Save Changes**
6. Wait for automatic redeploy (~2 minutes)

## Step 4: Add to Local .env (For Local Testing)

Add these lines to your `.env` file:

```env
GOOGLE_API_KEY=AIzaSy_your_api_key_here
GOOGLE_CSE_ID=your_search_engine_id_here
```

## Usage Limits

**Free Tier:**
- 100 search queries per day (free)
- After that: $5 per 1000 queries (up to 10k queries/day)

**Tips to stay within free tier:**
- Use search sparingly during development
- Consider caching search results
- The search only happens when users click "Search" button

## Testing

Test your setup locally:

```bash
cd /Users/angus/Desktop/ghrepo/recipegen
python3 recipe_searcher.py
```

This will search for "chocolate chip cookies" and display results.

## Troubleshooting

**Error: "Google API key is required"**
- Make sure `GOOGLE_API_KEY` is set in Render environment variables
- Check for typos in the key

**Error: "Google Custom Search Engine ID is required"**
- Make sure `GOOGLE_CSE_ID` is set in Render environment variables
- Check for typos in the ID

**Error: "API returned 403"**
- Your API key restrictions might be too strict
- Make sure Custom Search API is enabled in your Google Cloud project

**No results found:**
- Your Custom Search Engine might be restricted to specific sites
- Enable "Search the entire web" in CSE settings

## Alternative: Disable Search Feature

If you don't want to set up Google Custom Search, the URL extraction feature will still work fine. Users just won't see the "Search Recipes" option.

To disable search temporarily:
1. In Render, remove or leave blank the `GOOGLE_API_KEY` environment variable
2. The app will still work for URL extraction
