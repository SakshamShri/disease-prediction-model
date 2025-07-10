# 🚀 Deployment Guide for Render

## Prerequisites

1. **GitHub Account** - Your code should be on GitHub
2. **Render Account** - Sign up at [render.com](https://render.com)

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Your repository should contain these files:
- ✅ `main.py` - Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `gunicorn_config.py` - Production server config
- ✅ `templates/` - All HTML templates
- ✅ `recommender systems/` - Models and datasets
- ✅ `.gitignore` - Exclude unnecessary files
- ✅ `README.md` - Project documentation

### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for deployment"

# Add remote repository
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy on Render

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign in with your GitHub account

2. **Create New Web Service**
   - Click **"New +"** button
   - Select **"Web Service"**

3. **Connect Repository**
   - Choose **"Connect a repository"**
   - Select your GitHub repository
   - Click **"Connect"**

4. **Configure Settings**
   - **Name:** `medical-diagnosis-system` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** Choose closest to your users
   - **Branch:** `main`

5. **Build & Deploy Settings**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`

6. **Advanced Settings (Optional)**
   - **Environment Variables:**
     - `PYTHON_VERSION`: `3.9.18`
   - **Health Check Path:** `/` (optional)

7. **Deploy**
   - Click **"Create Web Service"**
   - Wait for build to complete (5-10 minutes)

### Step 4: Access Your App

Your app will be live at:
```
https://your-app-name.onrender.com
```

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` has correct versions
   - Ensure all files are committed to GitHub
   - Check Render logs for specific errors

2. **App Crashes**
   - Verify `main.py` has correct Flask structure
   - Check if all model files are included
   - Review Render logs for errors

3. **Model Files Not Found**
   - Ensure all `.pkl` files are in repository
   - Check file paths in your code
   - Verify file sizes aren't too large

4. **Import Errors**
   - Check all dependencies in `requirements.txt`
   - Ensure compatible Python version
   - Verify all imports in `main.py`

### Checking Logs:

1. Go to your service dashboard on Render
2. Click **"Logs"** tab
3. Check for error messages
4. Look for successful build messages

## Post-Deployment

### Test Your App:
1. ✅ Home page loads
2. ✅ All navigation works
3. ✅ Disease prediction works
4. ✅ All pages display correctly
5. ✅ Contact forms work (if any)

### Monitor Performance:
- Check Render dashboard for performance metrics
- Monitor error logs regularly
- Test functionality periodically

## Custom Domain (Optional)

1. Go to your service dashboard
2. Click **"Settings"**
3. Scroll to **"Custom Domains"**
4. Add your domain and configure DNS

## Environment Variables (If Needed)

Add these in Render dashboard under **"Environment"**:
- `FLASK_ENV`: `production`
- `DEBUG`: `False`
- Any API keys or sensitive data

## Success! 🎉

Your medical diagnosis system is now live and accessible worldwide!

**Remember:** This is for educational purposes. Always include the medical disclaimer on your site.

---

**Need Help?** Check Render's documentation or contact their support team. 