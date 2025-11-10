# Deploy to GitHub Pages - Simple Guide

## How It Works
- **Frontend (HTML)**: Hosted on GitHub Pages (free, static files)
- **Backend (Python/Flask)**: Hosted on Render (free tier available)

## Step 1: Deploy Backend to Render (5 minutes)

1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `angusyang91/recipegen`
4. Configure:
   - **Name**: `recipegen-api` (or any name)
   - **Root Directory**: Leave empty (or `/`)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Add Environment Variable:
   - Key: `WRITER_API_KEY`
   - Value: `1mxu3bKy4P1MOvH0A0V8UfNMIADjCRaW`
6. Click "Create Web Service"
7. Wait 2-3 minutes, then copy your URL (e.g., `https://recipegen-api.onrender.com`)

## Step 2: Update Frontend Config

Update the config.js file with your Render URL:

```bash
cd /Users/angus/Desktop/ghrepo/recipes-project
echo "window.API_BASE_URL = 'https://YOUR-RENDER-URL.onrender.com';" > static/config.js
```

Replace `YOUR-RENDER-URL` with your actual Render service URL.

## Step 3: Enable GitHub Pages

1. Go to https://github.com/angusyang91/recipegen/settings/pages
2. Under "Source":
   - Select branch: `main`
   - Select folder: `/static` (or `/docs` if you use that)
3. Click "Save"
4. Your site will be live at: `https://angusyang91.github.io/recipegen/` (or the path to your index.html)

## Step 4: Push Changes

```bash
cd /Users/angus/Desktop/ghrepo/recipes-project
git add static/config.js
git commit -m "Configure for GitHub Pages"
git push origin main
```

## That's It! 🎉

Your app will be live on GitHub Pages, connecting to your Render backend!

