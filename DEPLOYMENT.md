# 🚀 Deployment Guide

## Quick Deploy Options

### 1. Railway (Recommended - Easiest)

**Step 1: Prepare Your Code**
- Make sure all files are committed to a GitHub repository
- Your app is now ready for deployment!

**Step 2: Deploy to Railway**
1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python app
6. Wait for deployment (usually 2-3 minutes)
7. Your app will be live at a URL like: `https://your-app-name.railway.app`

**Step 3: Configure Environment (Optional)**
- In Railway dashboard, go to your project
- Add environment variable: `PORT=5000`

---

### 2. Render

**Step 1: Deploy to Render**
1. Go to [Render.com](https://render.com)
2. Sign up and create account
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `rock-paper-scissors`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Click "Create Web Service"
7. Wait for deployment (3-5 minutes)

**Step 2: Get Your URL**
- Your app will be available at: `https://your-app-name.onrender.com`

---

### 3. Heroku

**Step 1: Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Deploy**
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# Open your app
heroku open
```

---

### 4. PythonAnywhere

**Step 1: Sign Up**
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Create a free account

**Step 2: Upload Your Code**
1. Go to "Files" tab
2. Upload your project files
3. Or use Git: `git clone https://github.com/your-username/your-repo.git`

**Step 3: Configure Web App**
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" and Python 3.9
4. Set source code directory to your project folder
5. Set WSGI configuration file to point to your app.py

---

## Local Testing Before Deployment

**Test your app locally:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser to: http://localhost:5000
```

---

## Troubleshooting

### Common Issues:

**1. Port Issues**
- Make sure your app uses `os.environ.get('PORT', 5000)`
- ✅ Already configured in your app.py

**2. Dependencies**
- Make sure `requirements.txt` is up to date
- ✅ Already configured

**3. Static Files**
- Flask automatically serves static files
- ✅ No additional configuration needed

**4. Environment Variables**
- Your app doesn't need any special environment variables
- ✅ Ready to deploy

---

## Post-Deployment

### Test Your Deployed App:
1. **Single Player**: Test the basic game functionality
2. **Multiplayer**: Open two browser windows/tabs to test real-time gameplay
3. **Mobile**: Test on your phone to ensure responsive design works

### Monitor Your App:
- Check the deployment platform's dashboard for logs
- Monitor for any errors or performance issues

---

## Recommended: Railway

**Why Railway is best for your app:**
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Easy setup
- ✅ Good performance
- ✅ WebSocket support (for multiplayer)
- ✅ No credit card required

**Your app is now ready for deployment! 🎉** 