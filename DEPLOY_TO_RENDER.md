# Deploy RecipeSnap Backend to Render

## Quick Deploy (5 minutes)

### Step 1: Push to GitHub
Make sure all your changes are pushed to GitHub:
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Deploy on Render

1. **Go to Render**: https://render.com
2. **Sign up/Login** (free account works)
3. **Click "New +"** → **"Web Service"**
4. **Connect GitHub**:
   - Click "Connect GitHub"
   - Authorize Render
   - Select repository: `angusyang91/recipegen`
5. **Configure Service**:
   - **Name**: `recipesnap-api` (or any name you like)
   - **Region**: Choose closest to you (Oregon is default)
   - **Branch**: `main`
   - **Root Directory**: Leave **BLANK** (app is at repository root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variable**:
   - Click "Advanced" → "Add Environment Variable"
   - **Key**: `WRITER_API_KEY`
   - **Value**: `your_writer_api_key_here`
   - Click "Add"
7. **Click "Create Web Service"**
8. **Wait 2-3 minutes** for deployment
9. **Copy your service URL** (e.g., `https://recipesnap-api.onrender.com`)

### Step 3: Update Frontend Config

Once you have your Render URL, create the config file:

```bash
cd /Users/angus/Desktop/ghrepo/recipegen/static
echo "window.API_BASE_URL = 'https://YOUR-RENDER-URL.onrender.com';" > config.js
```

Replace `YOUR-RENDER-URL` with your actual Render service URL.

### Step 4: Push Config and Enable GitHub Pages

```bash
cd /Users/angus/Desktop/ghrepo/recipegen
git add static/config.js
git commit -m "Add API config for GitHub Pages"
git push origin main
```

Then enable GitHub Pages:
1. Go to https://github.com/angusyang91/recipegen/settings/pages
2. Source: Branch `main`, Folder `/docs` (or root `/)
3. Save

Your app will be live at: `https://angusyang91.github.io/recipegen/`

## Troubleshooting

**Service won't start?**
- Check logs in Render dashboard
- Make sure Root Directory is **blank** (app is at repository root)
- Verify `WRITER_API_KEY` is set correctly

**CORS errors?**
- The app already has CORS enabled
- If issues persist, the backend URL might be wrong in config.js

**API returns 404?**
- Check that your Render service is running (green status)
- Test the health endpoint: `https://your-url.onrender.com/api/health`

## Alternative: Use render.yaml (Auto-deploy)

If you pushed the `render.yaml` file, you can:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Render will auto-detect the render.yaml and configure everything
5. Just add the `ANTHROPIC_API_KEY` environment variable

