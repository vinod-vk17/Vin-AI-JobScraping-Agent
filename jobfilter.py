"""
Comprehensive Job Filter
Filters jobs based on:
1. USA Locations ONLY (all 50 states + major cities)
2. Tech Roles ONLY (Software, Data, ML, Analyst, Associate)
3. Experience: 0-5 years or entry-level ONLY
"""


class JobFilter:
    def should_keep(self, job):
        """
        Determine if a job should be kept based on strict criteria.
        
        Returns:
            bool: True if job meets ALL requirements, False otherwise
        """
        title = job.get("title", "").lower()
        location = job.get("location", "").lower()
        description = job.get("description", "").lower()
        
        # Add space padding for better matching
        title = f" {title} "
        location = f" {location} "
        description = f" {description} "
        
        # ============================================================
        # REQUIREMENT 1: LOCATION - ALL 50 US STATES
        # ============================================================

        usa_keywords = [
            # Remote/Flexible
            'remote', 'anywhere', 'work from home', 'wfh', 'nationwide',
            'virtual', 'distributed',

            # USA general
            'usa', 'united states', 'u.s.', 'u.s.a', 'america', 'us only',

            # ALL 50 STATES - Full Names
            'alabama', 'alaska', 'arizona', 'arkansas', 'california',
            'colorado', 'connecticut', 'delaware', 'florida', 'georgia',
            'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
            'kansas', 'kentucky', 'louisiana', 'maine', 'maryland',
            'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri',
            'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey',
            'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio',
            'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina',
            'south dakota', 'tennessee', 'texas', 'utah', 'vermont',
            'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming',

            # ALL 50 STATE ABBREVIATIONS (with space)
            ' al ', ' ak ', ' az ', ' ar ', ' ca ',
            ' co ', ' ct ', ' de ', ' fl ', ' ga ',
            ' hi ', ' id ', ' il ', ' in ', ' ia ',
            ' ks ', ' ky ', ' la ', ' me ', ' md ',
            ' ma ', ' mi ', ' mn ', ' ms ', ' mo ',
            ' mt ', ' ne ', ' nv ', ' nh ', ' nj ',
            ' nm ', ' ny ', ' nc ', ' nd ', ' oh ',
            ' ok ', ' or ', ' pa ', ' ri ', ' sc ',
            ' sd ', ' tn ', ' tx ', ' ut ', ' vt ',
            ' va ', ' wa ', ' wv ', ' wi ', ' wy ',

            # State abbreviations at end (e.g., "Austin, TX")
            ', al', ', ak', ', az', ', ar', ', ca',
            ', co', ', ct', ', de', ', fl', ', ga',
            ', hi', ', id', ', il', ', in', ', ia',
            ', ks', ', ky', ', la', ', me', ', md',
            ', ma', ', mi', ', mn', ', ms', ', mo',
            ', mt', ', ne', ', nv', ', nh', ', nj',
            ', nm', ', ny', ', nc', ', nd', ', oh',
            ', ok', ', or', ', pa', ', ri', ', sc',
            ', sd', ', tn', ', tx', ', ut', ', vt',
            ', va', ', wa', ', wv', ', wi', ', wy',

            # Major US Cities
            'san francisco', 'los angeles', 'san diego', 'san jose', 'sacramento',
            'oakland', 'fresno', 'long beach', 'santa clara', 'palo alto',
            'mountain view', 'sunnyvale', 'irvine', 'anaheim', 'santa monica',
            'new york city', 'nyc', 'brooklyn', 'manhattan', 'queens',
            'bronx', 'staten island', 'buffalo', 'rochester', 'albany',
            'austin', 'dallas', 'houston', 'san antonio', 'fort worth',
            'el paso', 'arlington', 'plano', 'irving',
            'seattle', 'tacoma', 'spokane', 'bellevue', 'redmond',
            'boston', 'cambridge', 'worcester', 'springfield', 'lowell',
            'miami', 'tampa', 'orlando', 'jacksonville', 'fort lauderdale',
            'tallahassee', 'st petersburg', 'naples',
            'chicago', 'naperville', 'aurora', 'rockford',
            'philadelphia', 'pittsburgh', 'harrisburg',
            'atlanta', 'savannah', 'augusta',
            'charlotte', 'raleigh', 'durham', 'greensboro', 'research triangle',
            'denver', 'boulder', 'colorado springs', 'fort collins',
            'phoenix', 'tucson', 'scottsdale', 'mesa', 'tempe',
            'portland', 'eugene', 'salem',
            'las vegas', 'reno', 'henderson',
            'nashville', 'memphis', 'knoxville', 'chattanooga',
            'detroit', 'ann arbor', 'grand rapids',
            'minneapolis', 'st paul', 'rochester',
            'washington dc', 'dc', 'd.c.', 'arlington', 'alexandria', 'bethesda',
            'richmond', 'virginia beach', 'norfolk',
            'columbus', 'cleveland', 'cincinnati',
            'baltimore',
            'milwaukee', 'madison',
            'kansas city', 'st louis',
            'indianapolis',
            'salt lake city', 'provo',
            'albuquerque', 'santa fe',
            'oklahoma city', 'tulsa',
            'new orleans', 'baton rouge',
            'louisville',
            'omaha', 'des moines', 'providence', 'hartford', 'new haven',
        ]

        if location:
            has_usa_location = any(kw in location for kw in usa_keywords)
            if not has_usa_location:
                return False

        # ============================================================
        # REQUIREMENT 2: TECH KEYWORDS + ANALYST/ASSOCIATE
        # ============================================================

        tech_title_keywords = [
            # ===== SOFTWARE ENGINEERING =====
            'software engineer', 'software developer', 'software dev',
            'developer', 'engineer', 'programmer', 'coder',
            'sde', 'sde1', 'sde2', 'sde3', 'sde i', 'sde ii', 'sde iii',

            # Stack specializations
            'backend', 'back-end', 'back end',
            'frontend', 'front-end', 'front end',
            'full stack', 'full-stack', 'fullstack',
            'web developer', 'mobile developer', 'app developer',

            # Specific engineering roles
            'platform engineer', 'infrastructure engineer', 'systems engineer',
            'site reliability', 'sre', 'devops', 'dev ops',
            'cloud engineer', 'solutions architect', 'software architect',
            'security engineer', 'application security', 'appsec',
            'network engineer', 'embedded engineer',

            # ===== DATA ROLES =====
            'data scientist', 'data science',
            'data engineer', 'data engineering',
            'data analyst', 'data analysis',
            'analytics engineer', 'analytical engineer',
            'business intelligence', 'bi engineer', 'bi analyst',
            'data platform engineer', 'data infrastructure',
            'dataops', 'data ops',

            # ===== AI & MACHINE LEARNING =====
            # Core ML
            'machine learning', 'ml engineer', 'machine learning engineer',
            'ai engineer', 'artificial intelligence',
            'deep learning', 'deep learning engineer',

            # Modern AI (2023-2025)
            'llm engineer', 'large language model',
            'generative ai', 'gen ai', 'genai',
            'prompt engineer', 'prompt engineering',
            'foundation model', 'foundation models',
            'ai research', 'ai researcher',

            # ML specializations
            'computer vision', 'cv engineer',
            'nlp engineer', 'natural language processing',
            'mlops', 'ml ops', 'machine learning operations',
            'ml platform', 'ml infrastructure',

            # Research roles
            'research scientist', 'research engineer',
            'applied scientist', 'applied research',
            'ai scientist',

            # ===== ANALYST ROLES (TECH-RELATED) =====
            # Data & Analytics
            'data analyst', 'analytics analyst', 'business analyst',
            'business intelligence analyst', 'bi analyst',
            'reporting analyst', 'insights analyst',
            'data visualization analyst', 'analytics specialist',

            # Quantitative & Research
            'quantitative analyst', 'quant analyst', 'quant',
            'research analyst', 'market research analyst',
            'statistical analyst', 'modeling analyst',

            # Technical Analysts
            'technical analyst', 'systems analyst', 'it analyst',
            'technology analyst', 'software analyst',
            'application analyst', 'solutions analyst',

            # Operations & Performance
            'operations analyst', 'performance analyst',
            'product analyst', 'strategy analyst',
            'risk analyst', 'compliance analyst',

            # Finance Tech Analysts
            'financial analyst', 'investment analyst',
            'credit analyst', 'trading analyst',
            'portfolio analyst', 'risk management analyst',

            # ===== ASSOCIATE ROLES (TECH-RELATED) =====
            # Engineering Associates
            'software engineer associate', 'associate software engineer',
            'engineer associate', 'associate engineer',
            'developer associate', 'associate developer',
            'technical associate', 'associate technical',

            # Data Associates
            'data scientist associate', 'associate data scientist',
            'data engineer associate', 'associate data engineer',
            'data analyst associate', 'associate data analyst',
            'analytics associate', 'associate analytics',

            # ML/AI Associates
            'ml engineer associate', 'associate ml engineer',
            'ai engineer associate', 'associate ai engineer',
            'research associate', 'associate researcher',

            # Tech Program Associates
            'program associate', 'associate program',
            'solutions associate', 'associate solutions',
            'technology associate', 'associate technology',

            # Consulting Tech Associates
            'technology consulting associate', 'tech consulting associate',
            'it consulting associate', 'digital associate',
            'strategy associate', 'innovation associate',

            # ===== QUANTITATIVE & FINANCE TECH =====
            'quantitative analyst', 'quant', 'quantitative developer',
            'quantitative researcher', 'quantitative engineer',
            'algorithmic trading', 'trading systems',
            'financial engineer', 'quantitative trader',
            'derivatives analyst', 'structured products',

            # ===== EMERGING/SPECIALIZED =====
            'blockchain', 'web3', 'crypto',
            'robotics', 'autonomous systems',
            'distributed systems',
            'performance engineer',
            'release engineer', 'build engineer',

            # ===== GENERAL TECH =====
            'technical', 'technology', 'tech',
            'computing', 'computational',
        ]

        has_tech_title = any(kw in title for kw in tech_title_keywords)
        if not has_tech_title:
            return False

        # ============================================================
        # REQUIREMENT 3: EXPERIENCE (0-5 years)
        # ============================================================

        combined_text = title + ' ' + description

        acceptable_exp_keywords = [
            # Explicit 0-5 year ranges
            '0-1', '0-2', '0-3', '0-4', '0-5',
            '1-2', '1-3', '1-4', '1-5',
            '2-3', '2-4', '2-5',
            '3-4', '3-5', '4-5',
            '0 to 1', '0 to 2', '0 to 3', '0 to 4', '0 to 5',
            '1 to 2', '1 to 3', '1 to 4', '1 to 5',
            '2 to 3', '2 to 4', '2 to 5',
            '3 to 4', '3 to 5', '4 to 5',

            # Single years (0-5)
            '0 year', '1 year', '2 years', '3 years', '4 years', '5 years',
            'zero years', 'one year', 'two years', 'three years', 'four years', 'five years',

            # Entry level terms
            'entry level', 'entry-level', 'early career', 'early-career',
            'new grad', 'new graduate', 'recent grad', 'recent graduate',
            'college grad', 'university graduate',
            'junior', 'associate', 'trainee',
            'intern', 'internship', 'co-op', 'coop',

            # Levels (I, II, III)
            'level 1', 'level i', 'level one',
            'level 2', 'level ii', 'level two',
            'level 3', 'level iii', 'level three',
            'l1', 'l2', 'l3',
            ' i ', ' ii ', ' iii ',
            'sde i', 'sde ii', 'sde iii',
            'sde 1', 'sde 2', 'sde 3',
            'analyst 1', 'analyst 2', 'analyst i', 'analyst ii',

            # Flexible/open
            'all levels', 'various levels', 'any level', 'multiple levels',
            'no experience required', 'no experience necessary',
            'open to all levels', 'fresh graduate', 'fresh grad',
        ]

        has_acceptable_exp = any(kw in combined_text for kw in acceptable_exp_keywords)
        mentions_experience = 'experience' in combined_text or 'year' in combined_text

        if has_acceptable_exp:
            return True   # ✅ Has 0-5 years → KEEP
        elif not mentions_experience:
            return True   # ✅ No experience mentioned → KEEP
        else:
            return False  # ❌ Mentions experience but NOT 0-5 years → skip
