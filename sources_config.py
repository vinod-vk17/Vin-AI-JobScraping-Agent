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
    },
    
    "ENERGY": {
        "companies": {
            "Shell": [
                "https://www.shell.com/careers/about-careers-at-shell/current-opportunities.html",
            ],
            "BP": [
                "https://www.bp.com/en/global/corporate/careers/search-jobs.html",
            ],
            "ExxonMobil": [
                "https://corporate.exxonmobil.com/careers/find-a-job",
            ],
            "Chevron": [
                "https://careers.chevron.com/search",
            ],
            "TotalEnergies": [
                "https://www.totalenergies.com/careers/join-us",
            ],
        }
    },
    
    "BFSI": {
        "companies": {
            "JPMorgan Chase": [
                "https://careers.jpmorgan.com/us/en/students/programs",
                "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001",
            ],
            "Goldman Sachs": [
                "https://www.goldmansachs.com/careers/",
            ],
            "Bank of America": [
                "https://careers.bankofamerica.com/en-us/search-jobs",
            ],
            "Morgan Stanley": [
                "https://www.morganstanley.com/careers/",
            ],
            "Citigroup": [
                "https://jobs.citi.com/",
            ],
        }
    },
    
    # Add your own categories here!
    # "CONSULTING": {
    #     "companies": {
    #         "McKinsey": ["https://www.mckinsey.com/careers"],
    #         "BCG": ["https://careers.bcg.com/"],
    #         "Bain": ["https://www.bain.com/careers/"],
    #     }
    # },
}


# User profile for job matching (optional)
USER_PROFILE = """
Skills: Python, JavaScript, React, Machine Learning, Data Analysis
Experience: 3 years in software engineering
Preferences: Remote or hybrid, focus on AI/ML roles
Education: Bachelor's in Computer Science
"""
