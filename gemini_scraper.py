"""
Gemini-Powered Job Scraper
Uses Google's Gemini API to intelligently extract and analyze job postings
"""

import os
import requests
import sqlite3
from datetime import datetime
import json
import time
from typing import List, Dict, Optional
import google.generativeai as genai

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

DATABASE_PATH = os.getenv('DATABASE_PATH', 'jobs.db')


class GeminiJobScraper:
    """
    Intelligent job scraper using Gemini API to extract structured job data
    from career pages and analyze job descriptions
    """
    
    def __init__(self):
        self.model = model if GEMINI_API_KEY else None
        
    def scrape_jobs_from_url(self, url: str, company: str, source_category: str) -> List[Dict]:
        """
        Scrape jobs from a career page URL using Gemini to extract structured data
        
        Args:
            url: Career page URL
            company: Company name
            source_category: Source category (e.g., MAANG, ENERGY, BFSI)
        
        Returns:
            List of job dictionaries
        """
        try:
            # Fetch the page content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Get the HTML content
            html_content = response.text
            
            # Use Gemini to extract job listings
            jobs = self.extract_jobs_with_gemini(html_content, company, source_category, url)
            
            return jobs
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def extract_jobs_with_gemini(self, html_content: str, company: str, 
                                 source_category: str, base_url: str) -> List[Dict]:
        """
        Use Gemini to intelligently extract job listings from HTML
        """
        if not self.model:
            print("Gemini API not configured")
            return []
        
        try:
            # Truncate HTML if too long (Gemini has token limits)
            max_chars = 30000
            if len(html_content) > max_chars:
                html_content = html_content[:max_chars]
            
            prompt = f"""
Extract all job postings from this career page HTML. For each job, extract:

1. Job Title
2. Location (city, state, or "Remote")
3. Job URL (if available, otherwise use base URL: {base_url})
4. Posted Date (if available)
5. Brief description or key requirements (1-2 sentences)

Return the data as a JSON array. Each job should be an object with keys:
- title (string)
- location (string)
- url (string)
- posted_date (string in YYYY-MM-DD format, or empty string)
- description (string, max 200 chars)

If you cannot find specific jobs, return an empty array [].

HTML Content:
{html_content}

Return ONLY the JSON array, no other text.
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            jobs_data = json.loads(response_text)
            
            # Process and structure jobs
            jobs = []
            for idx, job_data in enumerate(jobs_data):
                job = {
                    'job_id': f"{company.lower().replace(' ', '_')}_{int(time.time())}_{idx}",
                    'company': company,
                    'title': job_data.get('title', 'Unknown Title'),
                    'location': job_data.get('location', 'Not specified'),
                    'url': job_data.get('url', base_url),
                    'source_category': source_category,
                    'description': job_data.get('description', ''),
                    'posted_date': job_data.get('posted_date', ''),
                    'scraped_date': datetime.now().isoformat()
                }
                jobs.append(job)
            
            print(f"Extracted {len(jobs)} jobs from {company}")
            return jobs
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini response as JSON: {e}")
            print(f"Response: {response_text[:500]}")
            return []
        except Exception as e:
            print(f"Error using Gemini to extract jobs: {e}")
            return []
    
    def analyze_job_match(self, job_description: str, user_profile: str) -> Dict:
        """
        Use Gemini to analyze how well a job matches a user's profile
        
        Args:
            job_description: Full job description
            user_profile: User's skills, experience, preferences
        
        Returns:
            Dictionary with match_score (1-10), highlights, concerns
        """
        if not self.model:
            return {'match_score': 5, 'analysis': 'Gemini API not configured'}
        
        try:
            prompt = f"""
Analyze how well this job matches the candidate's profile.

User Profile:
{user_profile}

Job Description:
{job_description}

Provide analysis as JSON with:
- match_score (integer 1-10, where 10 is perfect match)
- highlights (array of strings: top 3 reasons this is a good match)
- concerns (array of strings: top 3 potential issues or missing qualifications)
- recommendation (string: brief recommendation)

Return ONLY the JSON object.
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing job match: {e}")
            return {'match_score': 5, 'analysis': str(e)}


def save_jobs_to_db(jobs: List[Dict]):
    """
    Save scraped jobs to SQLite database
    """
    if not jobs:
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    for job in jobs:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO jobs 
                (job_id, company, title, location, url, source_category, 
                 description, posted_date, scraped_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            ''', (
                job['job_id'],
                job['company'],
                job['title'],
                job['location'],
                job['url'],
                job['source_category'],
                job.get('description', ''),
                job.get('posted_date', ''),
                job['scraped_date']
            ))
            
            if cursor.rowcount > 0:
                inserted += 1
                
        except Exception as e:
            print(f"Error inserting job {job.get('job_id')}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"Saved {inserted} new jobs to database")


def scrape_all_sources(sources_config: Dict):
    """
    Scrape jobs from all configured sources
    
    Args:
        sources_config: Dictionary of sources from sources_config.py
    """
    scraper = GeminiJobScraper()
    total_jobs = []
    
    for source_name, source_data in sources_config.items():
        print(f"\n{'='*60}")
        print(f"Scraping Source: {source_name}")
        print(f"{'='*60}")
        
        companies = source_data.get('companies', {})
        
        for company_name, career_urls in companies.items():
            print(f"\n→ Scraping {company_name}...")
            
            for url in career_urls:
                print(f"  URL: {url}")
                
                try:
                    jobs = scraper.scrape_jobs_from_url(url, company_name, source_name)
                    total_jobs.extend(jobs)
                    
                    # Rate limiting - be respectful
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
    
    # Save all jobs to database
    print(f"\n{'='*60}")
    print(f"Scraping Complete")
    print(f"Total jobs found: {len(total_jobs)}")
    print(f"{'='*60}")
    
    save_jobs_to_db(total_jobs)
    return total_jobs


# Example usage
if __name__ == '__main__':
    # Import sources configuration
    try:
        from sources_config import SOURCES
        scrape_all_sources(SOURCES)
    except ImportError:
        print("sources_config.py not found. Please create it with your company URLs.")
