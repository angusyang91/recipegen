# Quick Start Guide - How to Run the Recipe App

## Step 1: Open Terminal
- On Mac: Press `Cmd + Space`, type "Terminal", and press Enter
- Or find Terminal in Applications → Utilities

## Step 2: Navigate to the Project Folder
Copy and paste this command into Terminal:
```bash
cd /Users/angus/Desktop/ghrepo/recipes-project
```

## Step 3: Run the App
Copy and paste this command:
```bash
python3 app.py
```

You should see something like:
```
 * Running on http://127.0.0.1:5000
```

## Step 4: Open in Your Browser
1. Open your web browser (Chrome, Safari, Firefox, etc.)
2. Go to this address: **http://localhost:5000**
3. You should see the RecipeSnap web interface!

## Step 5: Test It Out
1. Try one of the example recipe URLs (click on them)
2. Or paste your own recipe URL
3. Click "Extract Recipe"
4. Wait a few seconds and see your formatted recipe!

## To Stop the App
- Go back to Terminal
- Press `Ctrl + C` to stop the server

## Troubleshooting

**If you get "command not found":**
- Try `python app.py` instead of `python3 app.py`

**If port 5000 is busy:**
- Press `Ctrl + C` to stop
- Run: `PORT=5001 python3 app.py`
- Then go to: http://localhost:5001

**If you see API key errors:**
- Make sure the `.env` file exists in the recipes-project folder
- It should contain: `WRITER_API_KEY=1mxu3bKy4P1MOvH0A0V8UfNMIADjCRaW`

