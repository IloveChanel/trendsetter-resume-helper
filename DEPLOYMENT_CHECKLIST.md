# 📋 Quick Deployment Checklist

Copy and paste this checklist to track your progress!

```
DEPLOYMENT CHECKLIST
====================

PREPARATION
□ Code is on GitHub
□ GitHub account created
□ Vercel account created (free)
□ Render account created (free)

BACKEND DEPLOYMENT (Render)
□ Created new Web Service on Render
□ Connected GitHub repository
□ Set Root Directory to: backend
□ Set Build Command to: pip install -r requirements.txt
□ Set Start Command to: uvicorn app:app --host 0.0.0.0 --port $PORT
□ Selected Free tier
□ Clicked "Create Web Service"
□ Waited for deployment (3-5 minutes)
□ Backend shows "Live" status
□ Saved backend URL: _______________________
□ Tested: https://my-backend-url/api/health ✓

FRONTEND DEPLOYMENT (Vercel)
□ Clicked "Add New Project" on Vercel
□ Imported GitHub repository
□ Set Root Directory to: frontend
□ Added Environment Variable:
   Name: NEXT_PUBLIC_API_URL
   Value: (your backend URL from above)
□ Clicked "Deploy"
□ Waited for deployment (2-3 minutes)
□ Frontend shows "Ready" status
□ Saved frontend URL: _______________________
□ Tested: https://my-frontend-url ✓

CONNECT BACKEND TO FRONTEND
□ Went back to Render dashboard
□ Clicked on backend service
□ Clicked "Environment" tab
□ Added Environment Variable:
   Key: FRONTEND_URL
   Value: (your Vercel URL from above)
□ Saved changes
□ Waited for auto-redeploy (1-2 minutes)
□ Backend shows "Live" status again

FINAL TESTING
□ Visited frontend URL
□ Uploaded a test resume (PDF or DOCX)
□ Pasted a job description
□ Clicked "Analyze Resume"
□ Got results with scores ✓

DONE! 🎉
□ Shared my URL with others: _______________________

TROUBLESHOOTING
If something doesn't work:
1. Check both services show "Live" or "Ready" status
2. Check environment variables have no typos
3. Check URLs have no trailing slashes (/)
4. Check logs in Render or Vercel dashboard
5. Wait 1 minute and try again (Render wakes from sleep)
```

## Quick Reference URLs

After deployment, bookmark these:

| Service | URL | Purpose |
|---------|-----|---------|
| **Your Live App** | https://your-project.vercel.app | Share this with users |
| **Backend API** | https://your-backend.onrender.com | API endpoint |
| **API Docs** | https://your-backend.onrender.com/docs | API documentation |
| **Render Dashboard** | https://dashboard.render.com | Manage backend |
| **Vercel Dashboard** | https://vercel.com/dashboard | Manage frontend |

## Common Commands

### To redeploy manually:

**Render (Backend):**
1. Go to dashboard.render.com
2. Click your service
3. Click "Manual Deploy" → "Deploy latest commit"

**Vercel (Frontend):**
1. Go to vercel.com/dashboard
2. Click your project
3. Click "Redeploy" on latest deployment

### To view logs:

**Render:**
```
Dashboard → Your Service → Logs tab
```

**Vercel:**
```
Dashboard → Your Project → Deployments → Click deployment → Function Logs
```

## Time Estimates

| Task | Time |
|------|------|
| Create accounts | 2 minutes |
| Deploy backend | 5 minutes |
| Deploy frontend | 3 minutes |
| Configure CORS | 2 minutes |
| Testing | 3 minutes |
| **TOTAL** | **~15 minutes** |

## Need Help?

1. Check `QUICKSTART_DEPLOY.md` for detailed steps
2. Check `DEPLOYMENT.md` for advanced options
3. Check logs in Render or Vercel dashboard
4. Verify environment variables are correct

---

**Remember:**
- Backend URL: NO trailing slash (/) ❌ `https://backend.com/`
- Backend URL: YES ✅ `https://backend.com`
- Frontend URL: NO trailing slash (/) ❌ `https://frontend.com/`
- Frontend URL: YES ✅ `https://frontend.com`
