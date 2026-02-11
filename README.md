# 🚀 AI-Powered Job Scraper Web App

A beautiful, intelligent job tracking application powered by Google's Gemini API. Automatically scrapes, analyzes, and organizes job postings from multiple companies and industries.

## ✨ Features

### 🤖 **Gemini AI Integration**
- Intelligent extraction of job details from career pages
- Automatic parsing of HTML content
- Smart job description analysis
- Match scoring based on your profile

### 💎 **Beautiful Web Interface**
- Modern, responsive single-page application
- Real-time search and filtering
- Source category organization
- Status tracking (Pending, Applied, Failed)
- Stunning UI with smooth animations

### 📊 **Smart Organization**
- Multi-source categorization (MAANG, ENERGY, BFSI, etc.)
- SQLite database for fast queries
- Automatic deduplication
- Date tracking (Posted date & Scraped date)

### ⚡ **Automated Scraping**
- Runs every 4 hours via GitHub Actions
- Or deploy as a service with cron jobs
- Configurable source categories
- Multiple URLs per company support

---

## 🎯 Quick Start

### Prerequisites
- Python 3.11+
- Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized deployment)

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/job-scraper-webapp.git
cd job-scraper-webapp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

### 3. Configure Sources

Edit `sources_config.py` to add your target companies:

```python
SOURCES = {
    "MAANG": {
        "companies": {
            "Meta": ["https://www.metacareers.com/jobs"],
            "Google": ["https://careers.google.com/jobs/results/"],
            # Add more...
        }
    },
    "YOUR_CATEGORY": {
        "companies": {
            "Company1": ["https://careers.company1.com"],
            # Add more...
        }
    }
}
```

### 4. Run Initial Scrape

```bash
# Scrape jobs from all sources
python gemini_scraper.py
```

### 5. Start Web App

```bash
# Development mode
python app.py

# Production mode (recommended)
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
```

### 6. Open Browser

Navigate to: `http://localhost:5000`

🎉 **You're live!**

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Set your Gemini API key in .env
echo "GEMINI_API_KEY=your_key_here" > .env

# Build and run
docker-compose up -d

# Run scraper
docker-compose run scraper
```

### Manual Docker Build

```bash
# Build image
docker build -t job-scraper-webapp .

# Run web app
docker run -d -p 5000:5000 \
  -e GEMINI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  job-scraper-webapp

# Run scraper
docker run --rm \
  -e GEMINI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  job-scraper-webapp python gemini_scraper.py
```

---

## ☁️ Deploy to Production

### Deploy to Render

1. Create account on [Render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app`
   - **Environment Variables:** Add `GEMINI_API_KEY`
5. Deploy!

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-job-scraper

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add environment variables
4. Deploy automatically

---

## ⚙️ Configuration

### Sources Configuration

Add unlimited companies to `sources_config.py`:

```python
SOURCES = {
    "TECH": {
        "companies": {
            "Microsoft": [
                "https://careers.microsoft.com/",
                "https://jobs.careers.microsoft.com/global/en/search"  # Multiple URLs!
            ],
        }
    }
}
```

### User Profile (Optional)

Configure your profile for AI matching in `sources_config.py`:

```python
USER_PROFILE = """
Skills: Python, React, Machine Learning
Experience: 5 years
Preferences: Remote, AI/ML focus
"""
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes |
| `DATABASE_PATH` | SQLite database path | No (default: `jobs.db`) |
| `PORT` | Web app port | No (default: `5000`) |
| `FLASK_ENV` | Flask environment | No (default: `production`) |

---

## 🤖 Automated Scraping

### GitHub Actions (Recommended)

Already configured in `.github/workflows/scrape.yml`!

**Setup:**
1. Go to repository Settings → Secrets
2. Add `GEMINI_API_KEY` secret
3. Workflow runs automatically every 4 hours
4. Database stored as GitHub artifact

**Manual trigger:**
- Go to Actions tab
- Select "Scrape Jobs Every 4 Hours"
- Click "Run workflow"

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs every 4 hours)
0 */4 * * * cd /path/to/job-scraper-webapp && /path/to/venv/bin/python gemini_scraper.py >> scraper.log 2>&1
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 4 hours
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `gemini_scraper.py`
   - Start in: `C:\path\to\job-scraper-webapp`

---

## 📊 API Endpoints

The backend provides RESTful API endpoints:

### Get Jobs
```http
GET /api/jobs?search=engineer&source=MAANG&status=pending&page=1
```

### Get Statistics
```http
GET /api/stats
```

### Get Sources
```http
GET /api/sources
```

### Update Job Status
```http
PUT /api/jobs/:id/status
Content-Type: application/json

{
  "status": "applied"
}
```

---

## 🎨 Customization

### Change UI Theme

Edit `app/static/css/styles.css`:

```css
:root {
    --primary: #6366f1;  /* Change to your color */
    --bg-primary: #0f0f1a;  /* Background color */
    /* ... more variables ... */
}
```

### Add More Filters

Edit `app/templates/index.html` and `app/static/js/app.js` to add custom filters.

### Custom Job Analysis

Edit `gemini_scraper.py` → `analyze_job_match()` to customize AI analysis.

---

## 🔧 Troubleshooting

### Issue: Jobs not appearing

**Solution:**
1. Check if scraper ran successfully: `python gemini_scraper.py`
2. Verify Gemini API key is correct
3. Check database: `sqlite3 jobs.db "SELECT COUNT(*) FROM jobs;"`

### Issue: Gemini API errors

**Solution:**
1. Verify API key: https://makersuite.google.com/app/apikey
2. Check API quota limits
3. Try again after a few minutes (rate limiting)

### Issue: Web app not loading

**Solution:**
1. Check if port 5000 is available
2. Look at console logs for errors
3. Try: `python app.py` in development mode

---

## 📈 Performance Tips

### For 100+ Companies

1. **Batch scraping:** Process sources in batches
2. **Increase delays:** Add `time.sleep(5)` between requests
3. **Use caching:** Cache company pages for 24 hours
4. **Optimize Gemini calls:** Reduce HTML size before sending

### For High Traffic

1. **Use PostgreSQL:** Replace SQLite with PostgreSQL
2. **Add Redis:** Cache API responses
3. **Scale workers:** Increase gunicorn workers
4. **Enable CDN:** Serve static files via CDN

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file

---

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Flask for backend framework
- Modern CSS techniques for beautiful UI

---

## 📞 Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** your-email@example.com

---

**Built with ❤️ and powered by AI**

🚀 Happy Job Hunting!
