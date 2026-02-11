"""
Flask Backend for Job Scraper Web App
Handles API endpoints, database operations, and job scraping orchestration
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager
import json

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'jobs.db')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Database context manager
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
def init_db():
    """Create database tables if they don't exist"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT,
                url TEXT NOT NULL,
                source_category TEXT NOT NULL,
                description TEXT,
                requirements TEXT,
                posted_date TEXT,
                scraped_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                match_score INTEGER,
                gemini_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_category ON jobs(source_category)
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_company ON jobs(company)
        ''')
        
        conn.commit()

# API Routes

@app.route('/')
def index():
    """Serve the main single-page application"""
    return render_template('index.html')

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Get filtered jobs with pagination
    Query params: search, source, status, page, per_page
    """
    try:
        # Get query parameters
        search = request.args.get('search', '')
        source = request.args.get('source', 'all')
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        offset = (page - 1) * per_page
        
        with get_db() as conn:
            # Build query
            query = 'SELECT * FROM jobs WHERE 1=1'
            params = []
            
            # Search filter
            if search:
                query += ' AND (title LIKE ? OR company LIKE ? OR location LIKE ?)'
                search_term = f'%{search}%'
                params.extend([search_term, search_term, search_term])
            
            # Source category filter
            if source != 'all':
                query += ' AND source_category = ?'
                params.append(source)
            
            # Status filter
            if status != 'all':
                query += ' AND status = ?'
                params.append(status)
            
            # Order by scraped date (newest first)
            query += ' ORDER BY scraped_date DESC LIMIT ? OFFSET ?'
            params.extend([per_page, offset])
            
            # Execute query
            cursor = conn.execute(query, params)
            jobs = [dict(row) for row in cursor.fetchall()]
            
            # Get total count for pagination
            count_query = query.split('ORDER BY')[0].replace('SELECT *', 'SELECT COUNT(*)')
            count_params = params[:-2]  # Exclude LIMIT and OFFSET
            total = conn.execute(count_query, count_params).fetchone()[0]
            
            # Check if job is new (posted today)
            today = datetime.now().date()
            for job in jobs:
                scraped = datetime.fromisoformat(job['scraped_date']).date()
                job['is_new'] = (today - scraped).days == 0
            
            return jsonify({
                'success': True,
                'jobs': jobs,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get job statistics"""
    try:
        with get_db() as conn:
            total_jobs = conn.execute('SELECT COUNT(*) FROM jobs').fetchone()[0]
            applied_jobs = conn.execute('SELECT COUNT(*) FROM jobs WHERE status = "applied"').fetchone()[0]
            pending_jobs = conn.execute('SELECT COUNT(*) FROM jobs WHERE status = "pending"').fetchone()[0]
            failed_jobs = conn.execute('SELECT COUNT(*) FROM jobs WHERE status = "failed"').fetchone()[0]
            
            return jsonify({
                'success': True,
                'stats': {
                    'total': total_jobs,
                    'applied': applied_jobs,
                    'pending': pending_jobs,
                    'failed': failed_jobs
                }
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get all unique source categories"""
    try:
        with get_db() as conn:
            cursor = conn.execute('SELECT DISTINCT source_category FROM jobs')
            sources = [row[0] for row in cursor.fetchall()]
            
            return jsonify({
                'success': True,
                'sources': sources
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    """Update job application status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'applied', 'failed', 'rejected']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        with get_db() as conn:
            conn.execute('UPDATE jobs SET status = ? WHERE id = ?', (new_status, job_id))
            conn.commit()
            
            return jsonify({'success': True, 'message': 'Status updated'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """Manually trigger job scraping (for testing)"""
    try:
        # This will be called by the scheduled job scraper
        # For now, return success
        return jsonify({
            'success': True,
            'message': 'Scraping triggered (will be implemented by scraper service)'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Initialize database on startup
init_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
