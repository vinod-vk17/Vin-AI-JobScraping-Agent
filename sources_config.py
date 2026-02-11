"""
Sources Configuration
Configure your job sources here - add unlimited companies and categories
"""

SOURCES = {
    "MAANG": {
        "companies": {
            "Meta": [
                "https://www.metacareers.com/jobs",
            ],
            "Apple": [
                "https://jobs.apple.com/en-us/search",
            ],
            "Amazon": [
                "https://www.amazon.jobs/en/search",
            ],
            "Netflix": [
                "https://jobs.netflix.com/search",
            ],
            "Google": [
                "https://careers.google.com/jobs/results/",
            ]
        }
    }
}


# User profile for job matching (optional)
USER_PROFILE = """
Skills: Python, JavaScript, React, Machine Learning, Data Analysis
Experience: 3 years in software engineering
Preferences: Remote or hybrid, focus on AI/ML roles
Education: Bachelor's in Computer Science
"""
