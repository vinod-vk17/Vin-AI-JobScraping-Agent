# 🚀 Deployment Guide - Job Scraper Web App

Complete guide for deploying your AI-powered job tracker to production.

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Deploy to Render (Recommended)](#deploy-to-render)
3. [Deploy to Railway](#deploy-to-railway)
4. [Deploy to Heroku](#deploy-to-heroku)
5. [Deploy with Docker](#deploy-with-docker)
6. [Setup Automated Scraping](#setup-automated-scraping)
7. [Environment Variables](#environment-variables)

---

## 🏠 Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/job-scraper-webapp.git
cd job-scraper-webapp

# Run start script
./start.sh
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# Run initial scrape
python gemini_scraper.py

# Start web app
python app.py
```

Visit: `http://localhost:5000`

---

## ☁️ Deploy to Render (Recommended)

**Best for:** Production deployment with automatic HTTPS and free tier

### Step 1: Prepare Repository

1. Push your code to GitHub
2. Make sure `.env` is in `.gitignore` (it is by default)

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

   **Basic Settings:**
   - Name: `job-scraper-webapp`
   - Region: Choose closest to you
   - Branch: `main`
   - Root Directory: (leave empty)

   **Build Settings:**
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`

4. Click **"Advanced"** → Add Environment Variables:
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key

5. Select **Free** plan

6. Click **"Create Web Service"**

### Step 4: Setup Database Persistence

1. In Render dashboard, click your service
2. Go to **"Disk"** tab
3. Add new disk:
   - Name: `jobs-database`
   - Mount Path: `/app/data`
   - Size: 1 GB

4. Update environment variable:
   - Key: `DATABASE_PATH`
   - Value: `/app/data/jobs.db`

### Step 5: Setup Automated Scraping

**Option A: Use Render Cron Jobs (Paid plan)**
1. Create new Cron Job
2. Command: `python gemini_scraper.py`
3. Schedule: `0 */4 * * *` (every 4 hours)

**Option B: Use GitHub Actions (Free)**
See [Setup Automated Scraping](#setup-automated-scraping) section

Your app is live! 🎉

URL: `https://job-scraper-webapp.onrender.com`

---

## 🚂 Deploy to Railway

**Best for:** Quick deployment with excellent developer experience

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub

### Step 2: Deploy

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Click **"Deploy Now"**

### Step 3: Configure Environment

1. Go to **Variables** tab
2. Add variables:
   ```
   GEMINI_API_KEY=your_api_key_here
   DATABASE_PATH=/app/data/jobs.db
   PORT=5000
   ```

### Step 4: Add Volume for Database

1. Go to **Settings** tab
2. Click **"+ Add Volume"**
3. Mount path: `/app/data`
4. Size: 1 GB

### Step 5: Configure Start Command

1. Go to **Settings** tab
2. Find **"Start Command"**
3. Set: `gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app`

Your app is live! 🎉

URL: Click **"Generate Domain"** to get your URL

---

## 🟣 Deploy to Heroku

**Best for:** Established platform with good documentation

### Prerequisites

```bash
# Install Heroku CLI
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 1: Login

```bash
heroku login
```

### Step 2: Create App

```bash
cd job-scraper-webapp
heroku create your-job-scraper-app
```

### Step 3: Add Environment Variables

```bash
heroku config:set GEMINI_API_KEY=your_api_key_here
```

### Step 4: Add PostgreSQL (Optional, for scaling)

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Deploy

```bash
git push heroku main
```

### Step 6: Open App

```bash
heroku open
```

### Step 7: Setup Scraper Scheduler

```bash
# Add Heroku Scheduler addon
heroku addons:create scheduler:standard

# Open scheduler dashboard
heroku addons:open scheduler
```

In the dashboard:
- Click **"Create job"**
- Command: `python gemini_scraper.py`
- Frequency: Every 4 hours
- Click **"Save"**

Your app is live! 🎉

---

## 🐳 Deploy with Docker

**Best for:** Self-hosting on your own server

### Option A: Docker Compose (Recommended)

```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Run scraper manually
docker-compose run scraper
```

### Option B: Docker CLI

```bash
# Build image
docker build -t job-scraper .

# Run web app
docker run -d \
  --name job-scraper-web \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  job-scraper

# Run scraper
docker run --rm \
  -e GEMINI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  job-scraper python gemini_scraper.py
```

### Setup Cron for Scraping

```bash
# Edit crontab
crontab -e

# Add this line
0 */4 * * * docker run --rm -e GEMINI_API_KEY=your_key -v /path/to/data:/app/data job-scraper python gemini_scraper.py
```

---

## 🤖 Setup Automated Scraping

### GitHub Actions (Recommended - Free)

Already configured! Just need to:

1. **Add Secret:**
   - Go to GitHub repo → Settings → Secrets → Actions
   - Click **"New repository secret"**
   - Name: `GEMINI_API_KEY`
   - Value: Your API key
   - Click **"Add secret"**

2. **Workflow runs automatically every 4 hours**

3. **Manual trigger:**
   - Go to Actions tab
   - Click "Scrape Jobs Every 4 Hours"
   - Click "Run workflow"

4. **Database storage:**
   - Database saved as GitHub artifact
   - Automatically downloaded on next run
   - Persists for 90 days

### Cron Job (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Add this line (runs every 4 hours)
0 */4 * * * cd /path/to/job-scraper-webapp && /path/to/venv/bin/python gemini_scraper.py >> /path/to/logs/scraper.log 2>&1
```

### Windows Task Scheduler

1. Open **Task Scheduler**
2. Click **"Create Basic Task"**
3. Name: "Job Scraper"
4. Trigger: **Daily**, repeat every 4 hours
5. Action: **Start a program**
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `gemini_scraper.py`
   - Start in: `C:\path\to\job-scraper-webapp`
6. Click **"Finish"**

---

## 🔐 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Web app port | `5000` |
| `DATABASE_PATH` | SQLite database file | `jobs.db` |
| `FLASK_ENV` | Flask environment | `production` |

### How to Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API key"**
3. Choose or create a project
4. Copy the API key
5. Add to your deployment platform

---

## 🔍 Health Checks

### Check if Web App is Running

```bash
curl https://your-app-url.com/api/stats
```

Should return JSON with job statistics.

### Check Database

```bash
# Local
sqlite3 jobs.db "SELECT COUNT(*) FROM jobs;"

# Docker
docker exec job-scraper-web sqlite3 /app/data/jobs.db "SELECT COUNT(*) FROM jobs;"
```

### View Logs

**Render:**
- Dashboard → Your service → Logs tab

**Railway:**
- Dashboard → Your project → Deployments → Click latest → Logs

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker logs -f job-scraper-web
```

---

## 🎯 Performance Optimization

### For High Traffic

1. **Increase workers:**
   ```bash
   gunicorn --workers 4 --threads 2 app:app
   ```

2. **Add Redis cache:**
   - Install: `pip install redis Flask-Caching`
   - Configure caching for API responses

3. **Use PostgreSQL:**
   - Replace SQLite with PostgreSQL
   - Better for concurrent writes

4. **Enable compression:**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

### For Many Companies (100+)

1. **Batch scraping:**
   - Process 10 companies at a time
   - Add delays between batches

2. **Optimize Gemini calls:**
   - Cache results for 24 hours
   - Reduce HTML size before sending

3. **Database indexes:**
   - Already added in `app.py`
   - Consider full-text search indexes

---

## 🆘 Troubleshooting

### App won't start

1. Check environment variables are set
2. Verify Gemini API key is valid
3. Look at logs for error messages
4. Try running locally first

### Database errors

1. Check DATABASE_PATH is writable
2. Verify disk has space
3. Try deleting and recreating database

### Scraper not finding jobs

1. Verify URLs in `sources_config.py`
2. Check Gemini API quota
3. Look at scraper logs
4. Try running scraper manually

### Slow performance

1. Add database indexes
2. Reduce number of companies
3. Increase server resources
4. Enable caching

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/job-scraper-webapp/issues)
- **Documentation:** [README.md](README.md)
- **Email:** your-email@example.com

---

## ✅ Deployment Checklist

- [ ] Gemini API key obtained
- [ ] Code pushed to GitHub
- [ ] Platform account created (Render/Railway/Heroku)
- [ ] Web service deployed
- [ ] Environment variables configured
- [ ] Database persistence setup
- [ ] Automated scraping configured
- [ ] Health check passing
- [ ] Custom domain configured (optional)
- [ ] Monitoring setup (optional)

---

**Congratulations! Your job tracker is now live! 🎉**

Visit your URL and start tracking opportunities!
