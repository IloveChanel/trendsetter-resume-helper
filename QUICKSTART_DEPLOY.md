# 🚀 Beginner's Deployment Guide

This guide will walk you through deploying your Trendsetter Resume Helper step-by-step. **No prior deployment experience needed!**

## What You'll Need

- A GitHub account (free)
- Your code pushed to GitHub
- A Vercel account (free) - for the frontend
- A Render account (free) - for the backend

**Total time: ~15-20 minutes**  
**Total cost: $0 (using free tiers)**

---

## Part 1: Push Your Code to GitHub (If Not Already Done)

### Step 1: Make sure your code is on GitHub

1. Go to [github.com](https://github.com)
2. Log in to your account
3. Make sure you can see your `trendsetter-resume-helper` repository
4. Click on it to open it

✅ **You should see all your files including `backend/` and `frontend/` folders**

---

## Part 2: Deploy the Backend (API) to Render

The backend is the part that does all the analysis. We'll deploy it first.

### Step 1: Create a Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"** in the top right
3. Sign up using your **GitHub account** (click "Sign up with GitHub")
4. Authorize Render to access your GitHub repositories

### Step 2: Create a New Web Service

1. Once logged in, click **"New +"** button in the top right
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Find `trendsetter-resume-helper` and click **"Connect"**

### Step 3: Configure the Backend Service

Now fill in these exact settings:

**Name:**
```
trendsetter-backend
```
(or any name you like)

**Region:**
- Choose the one closest to you (e.g., "Oregon (US West)" if you're in the US)

**Branch:**
```
copilot/clean-up-directory-structure
```
(or `main` if your code is on the main branch)

**Root Directory:**
```
backend
```
⚠️ **Important: This tells Render to look in the backend folder**

**Runtime:**
- Select **"Python 3"** from the dropdown

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn app:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
- Select **"Free"** (it will say "$0/month")

### Step 4: Add Environment Variables (Optional but Recommended)

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Add this:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.10`

### Step 5: Deploy!

1. Click **"Create Web Service"** at the bottom
2. Wait 3-5 minutes while Render builds your backend
3. You'll see logs scrolling - this is normal!
4. Wait until you see **"Your service is live"** at the top

### Step 6: Save Your Backend URL

1. At the top of the page, you'll see a URL like: `https://trendsetter-backend-xxxx.onrender.com`
2. **Copy this URL** - you'll need it in the next part!
3. Test it by visiting: `https://your-backend-url.onrender.com/api/health`
   - You should see: `{"status":"healthy"}`

✅ **Backend is deployed!**

---

## Part 3: Deploy the Frontend to Vercel

The frontend is the website that users see. Now we'll deploy it.

### Step 1: Create a Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"** in the top right
3. Sign up using your **GitHub account** (click "Continue with GitHub")
4. Authorize Vercel to access your GitHub repositories

### Step 2: Import Your Project

1. Once logged in, click **"Add New..."** → **"Project"**
2. You'll see a list of your GitHub repositories
3. Find `trendsetter-resume-helper` and click **"Import"**

### Step 3: Configure the Frontend

**Root Directory:**
1. Vercel should ask about the root directory
2. Click **"Edit"** next to Root Directory
3. Type: `frontend`
4. Click **"Continue"**

**Framework Preset:**
- Vercel should automatically detect **"Next.js"** - this is correct!

**Build Settings:**
- Leave these as default:
  - Build Command: `npm run build` or `next build`
  - Output Directory: `.next`

### Step 4: Add Environment Variable

This is **critical** - it tells your frontend where to find the backend!

1. Scroll down to **"Environment Variables"**
2. Click to expand the section
3. Add this variable:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** Your backend URL from Part 2 (e.g., `https://trendsetter-backend-xxxx.onrender.com`)
   - ⚠️ **Do NOT include a trailing slash!**
4. Click **"Add"**

### Step 5: Deploy!

1. Click **"Deploy"** button at the bottom
2. Wait 2-3 minutes while Vercel builds your frontend
3. You'll see a progress indicator
4. When done, you'll see **"Congratulations!"** with confetti 🎉

### Step 6: Visit Your Live Site!

1. Vercel will show you a URL like: `https://trendsetter-resume-helper-xxxx.vercel.app`
2. Click **"Visit"** or copy the URL and open it in a new tab
3. **Your app is now live!** 🎉

---

## Part 4: Update Backend CORS (Important!)

Now we need to tell the backend to accept requests from your frontend.

### Step 1: Add Frontend URL to Backend

1. Go back to [render.com](https://dashboard.render.com)
2. Click on your **"trendsetter-backend"** service
3. Click **"Environment"** in the left sidebar
4. Click **"Add Environment Variable"**
5. Add:
   - **Key:** `FRONTEND_URL`
   - **Value:** Your Vercel URL (e.g., `https://trendsetter-resume-helper-xxxx.vercel.app`)
   - ⚠️ **Do NOT include a trailing slash!**
6. Click **"Save Changes"**

### Step 2: Wait for Backend to Redeploy

1. Render will automatically redeploy your backend (takes 1-2 minutes)
2. Wait until you see **"Live"** status again

✅ **Done! Your app is fully deployed and working!**

---

## Testing Your Deployment

### Test the Backend
1. Visit: `https://your-backend-url.onrender.com/docs`
2. You should see the FastAPI documentation page
3. This means your API is working!

### Test the Frontend
1. Visit your Vercel URL: `https://your-frontend-url.vercel.app`
2. You should see the resume upload page
3. Try uploading a resume and analyzing it!

---

## What URLs Do I Have?

After deployment, you'll have:

1. **Frontend (Your Website):**
   - `https://trendsetter-resume-helper-xxxx.vercel.app`
   - This is what you share with users

2. **Backend (API):**
   - `https://trendsetter-backend-xxxx.onrender.com`
   - This is for the frontend to communicate with

---

## Troubleshooting Common Issues

### Issue: "Failed to fetch" error on frontend

**Solution:** Check that:
1. Your `NEXT_PUBLIC_API_URL` in Vercel is correct (no trailing slash)
2. Your `FRONTEND_URL` in Render is correct (no trailing slash)
3. Both services show "Live" status

### Issue: Backend takes a long time to load first time

**Solution:** 
- This is normal on Render's free tier
- The backend "sleeps" after 15 minutes of inactivity
- First request wakes it up (takes 30-60 seconds)
- Subsequent requests are fast

### Issue: Changes not showing up

**Solution:**
- **Backend:** Render auto-deploys when you push to GitHub
- **Frontend:** Vercel auto-deploys when you push to GitHub
- Or manually redeploy from the dashboard

---

## Making Updates Later

### To Update Backend Code:
1. Push changes to GitHub
2. Render automatically detects changes and redeploys
3. Wait 2-3 minutes

### To Update Frontend Code:
1. Push changes to GitHub
2. Vercel automatically detects changes and redeploys
3. Wait 1-2 minutes

### To See Deployment Logs:
- **Render:** Click your service → "Logs" tab
- **Vercel:** Click your project → "Deployments" → Click a deployment → "View Function Logs"

---

## Free Tier Limitations

### Render Free Tier:
- ✅ Unlimited deploys
- ✅ Free SSL (https)
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 750 hours/month free (enough for personal use)

### Vercel Free Tier:
- ✅ Unlimited deploys
- ✅ Free SSL (https)
- ✅ 100 GB bandwidth/month
- ✅ No sleep mode

---

## Need Help?

### Check Status:
1. **Render:** Dashboard shows "Live" or "Failed"
2. **Vercel:** Dashboard shows "Ready" or "Error"

### View Logs:
1. **Render:** Service page → "Logs" tab
2. **Vercel:** Project page → "Deployments" → Click deployment → Logs

### Test Endpoints:
1. Backend health: `https://your-backend.onrender.com/api/health`
2. Backend docs: `https://your-backend.onrender.com/docs`
3. Frontend: `https://your-frontend.vercel.app`

---

## Summary Checklist

- [ ] Backend deployed to Render ✅
- [ ] Backend URL saved and tested ✅
- [ ] Frontend deployed to Vercel ✅
- [ ] Frontend URL saved and tested ✅
- [ ] Environment variables set correctly ✅
- [ ] CORS configured (FRONTEND_URL in backend) ✅
- [ ] App tested and working ✅

**Congratulations! Your app is now live on the internet!** 🎉

Share your Vercel URL with anyone, and they can use your resume analyzer!
