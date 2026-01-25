# Deployment Guide

This guide covers multiple deployment options for the Trendsetter Resume Helper application.

## Table of Contents
1. [Quick Deploy (Recommended)](#quick-deploy-recommended)
2. [Deploy Frontend to Vercel](#deploy-frontend-to-vercel)
3. [Deploy Backend Options](#deploy-backend-options)
4. [Docker Deployment](#docker-deployment)
5. [VPS/Cloud Server Deployment](#vpscloud-server-deployment)

---

## Quick Deploy (Recommended)

### Option 1: Frontend on Vercel + Backend on Render

**Best for:** Quick deployment with free tier options

#### Step 1: Deploy Backend to Render

1. Push your code to GitHub
2. Go to [Render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Name**: trendsetter-backend
   - **Region**: Choose closest to your users
   - **Branch**: main (or your branch)
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `PYTHON_VERSION`: `3.10`
7. Click "Create Web Service"
8. Copy your backend URL (e.g., `https://trendsetter-backend.onrender.com`)

#### Step 2: Deploy Frontend to Vercel

1. Go to [Vercel.com](https://vercel.com) and sign up
2. Click "Add New..." → "Project"
3. Import your GitHub repo
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://trendsetter-backend.onrender.com`)
6. Click "Deploy"
7. Your app will be live at `https://your-project.vercel.app`

---

## Deploy Frontend to Vercel

### Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy: Y
# - Which scope: Select your account
# - Link to existing project: N
# - Project name: trendsetter-resume-helper
# - Directory: ./
# - Override settings: N

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL

# Enter your backend URL when prompted
# Then redeploy
vercel --prod
```

### Environment Variables for Vercel

Add these in Vercel dashboard (Settings → Environment Variables):

```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Deploy Backend Options

### Option A: Render.com (Free Tier Available)

See Quick Deploy section above.

**Pros**: Free tier, automatic deployments, SSL included  
**Cons**: Cold starts on free tier (app sleeps after 15min inactivity)

### Option B: Railway.app

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Configure:
   - **Root Directory**: `backend`
   - Railway auto-detects Python
5. Add Environment Variables (optional):
   - `PORT`: Railway sets this automatically
6. Deploy
7. Get your backend URL from Railway dashboard

**Pros**: Fast deployments, good free tier  
**Cons**: Credit card required for free tier

### Option C: Fly.io

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login:
```bash
fly auth login
```

3. Navigate to backend and create `fly.toml`:
```bash
cd backend
fly launch
```

4. Follow prompts and deploy:
```bash
fly deploy
```

**Pros**: Excellent performance, multiple regions  
**Cons**: More complex setup

### Option D: Heroku

1. Install Heroku CLI
2. Create `Procfile` in backend directory:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

3. Deploy:
```bash
cd backend
heroku create trendsetter-backend
git subtree push --prefix backend heroku main
```

**Pros**: Easy to use, well-documented  
**Cons**: No free tier anymore

---

## Docker Deployment

### Option 1: Docker Compose (Full Stack)

Create `docker-compose.yml` in root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./resume_helper.db
    volumes:
      - ./backend:/app
      - backend-data:/app/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

volumes:
  backend-data:
```

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

Deploy with:
```bash
docker-compose up -d
```

### Option 2: Deploy to AWS ECS/DigitalOcean/GCP

1. Build and push images to registry:
```bash
docker build -t trendsetter-backend ./backend
docker build -t trendsetter-frontend ./frontend

# Tag and push to your registry (ECR, DockerHub, etc.)
```

2. Deploy using platform-specific methods

---

## VPS/Cloud Server Deployment

### Using Ubuntu Server (DigitalOcean, Linode, AWS EC2, etc.)

#### 1. Initial Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3.10 python3-pip nginx nodejs npm git

# Install PM2 for process management
npm install -g pm2
```

#### 2. Clone and Setup Backend

```bash
# Clone repo
cd /var/www
git clone https://github.com/yourusername/trendsetter-resume-helper.git
cd trendsetter-resume-helper/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start with PM2
pm2 start "uvicorn app:app --host 0.0.0.0 --port 8000" --name trendsetter-backend
pm2 save
pm2 startup
```

#### 3. Setup Frontend

```bash
cd /var/www/trendsetter-resume-helper/frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=https://api.yourdomain.com" > .env.local

# Build
npm run build

# Start with PM2
pm2 start "npm start" --name trendsetter-frontend
pm2 save
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/trendsetter`:

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/trendsetter /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 5. Setup SSL with Let's Encrypt

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

#### 6. Update Backend CORS

Edit `backend/app.py` to allow your domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)
```

Restart backend:
```bash
pm2 restart trendsetter-backend
```

---

## Environment Variables

### Backend Environment Variables

Create `backend/.env`:
```bash
DATABASE_URL=sqlite:///./resume_helper.db
# Add other environment variables as needed
```

### Frontend Environment Variables

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Database Considerations

### For Production

**Option 1: Keep SQLite (Simple)**
- Good for: Small to medium traffic
- Backup regularly: `cp resume_helper.db resume_helper.db.backup`

**Option 2: Upgrade to PostgreSQL**
1. Install PostgreSQL on your backend server
2. Update `backend/database.py`:
```python
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/resumedb')
```
3. Update requirements.txt:
```
psycopg2-binary==2.9.9
```

---

## Monitoring & Maintenance

### Health Checks

Add to your deployment:
- Backend health: `https://your-backend-url.com/api/health`
- Frontend health: Check homepage loads

### Logs

**Render/Railway/Vercel**: Built-in log viewers in dashboard

**VPS with PM2**:
```bash
pm2 logs trendsetter-backend
pm2 logs trendsetter-frontend
```

**Docker**:
```bash
docker-compose logs -f
```

### Backup Database

```bash
# Automated daily backup (add to crontab)
0 2 * * * cp /var/www/trendsetter-resume-helper/backend/resume_helper.db /backups/resume_helper_$(date +\%Y\%m\%d).db
```

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Vercel (Frontend) | ✅ Yes | $20/mo | Static/SSR sites |
| Render (Backend) | ✅ Yes* | $7/mo | API services |
| Railway | ✅ $5 credit | $5/mo usage | Full stack |
| Fly.io | ✅ Limited | Pay-as-you-go | Global deployment |
| DigitalOcean Droplet | ❌ No | $6/mo | Full control |

*Free tier sleeps after 15min inactivity

---

## Recommended Setup for Production

### Budget-Friendly (Free/Low Cost)
- **Frontend**: Vercel (Free)
- **Backend**: Render (Free tier)
- **Total**: $0/month (with cold starts)

### Performance-Focused
- **Frontend**: Vercel (Pro $20/mo)
- **Backend**: Railway ($7-15/mo)
- **Total**: ~$30/month

### Professional/Enterprise
- **Frontend**: Vercel Pro or Self-hosted
- **Backend**: DigitalOcean Droplet or AWS
- **Database**: Managed PostgreSQL
- **Total**: $50-100/month

---

## Troubleshooting

### CORS Errors
- Update `allow_origins` in backend `app.py`
- Ensure frontend URL matches exactly (with/without www, http/https)

### Cold Starts (Free Tiers)
- Use cron job to ping backend every 10 minutes
- Upgrade to paid tier for always-on

### Build Failures
- Check Node version (use 18.x)
- Check Python version (use 3.10+)
- Verify all dependencies in requirements.txt/package.json

### Database Issues
- For SQLite: Ensure write permissions
- For PostgreSQL: Verify connection string

---

## Next Steps

1. Choose your deployment platform
2. Set up backend first
3. Configure frontend with backend URL
4. Test thoroughly
5. Set up monitoring
6. Configure backups
7. Set up custom domain (optional)

For questions or issues, refer to platform-specific documentation.
