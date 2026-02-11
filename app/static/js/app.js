/**
 * Job Tracker - Frontend Application Logic
 * Handles API calls, UI updates, and user interactions
 */

// State management
const state = {
    jobs: [],
    currentPage: 1,
    totalPages: 1,
    filters: {
        search: '',
        source: 'all',
        status: 'all'
    }
};

// API base URL
const API_BASE = window.location.origin;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

/**
 * Initialize application
 */
async function initializeApp() {
    showLoading();
    await Promise.all([
        fetchStats(),
        fetchSources(),
        fetchJobs()
    ]);
    hideLoading();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Search input with debounce
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            state.filters.search = e.target.value;
            state.currentPage = 1;
            fetchJobs();
        }, 500);
    });

    // Clear search
    document.getElementById('clearSearch').addEventListener('click', () => {
        searchInput.value = '';
        state.filters.search = '';
        state.currentPage = 1;
        fetchJobs();
    });

    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', () => {
        initializeApp();
    });

    // Source filter chips
    document.getElementById('sourceFilters').addEventListener('click', (e) => {
        if (e.target.classList.contains('chip')) {
            // Remove active from all
            document.querySelectorAll('#sourceFilters .chip').forEach(chip => {
                chip.classList.remove('active');
            });
            // Add active to clicked
            e.target.classList.add('active');
            state.filters.source = e.target.dataset.source;
            state.currentPage = 1;
            fetchJobs();
        }
    });

    // Status filter chips
    document.getElementById('statusFilters').addEventListener('click', (e) => {
        if (e.target.classList.contains('chip')) {
            // Remove active from all
            document.querySelectorAll('#statusFilters .chip').forEach(chip => {
                chip.classList.remove('active');
            });
            // Add active to clicked
            e.target.classList.add('active');
            state.filters.status = e.target.dataset.status;
            state.currentPage = 1;
            fetchJobs();
        }
    });

    // Pagination
    document.getElementById('prevPage').addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            fetchJobs();
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        if (state.currentPage < state.totalPages) {
            state.currentPage++;
            fetchJobs();
        }
    });
}

/**
 * Fetch job statistics
 */
async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        const data = await response.json();
        
        if (data.success) {
            updateStats(data.stats);
        }
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

/**
 * Update statistics display
 */
function updateStats(stats) {
    document.getElementById('totalJobs').textContent = stats.total;
    document.getElementById('appliedJobs').textContent = stats.applied;
    document.getElementById('pendingJobs').textContent = stats.pending;
    document.getElementById('failedJobs').textContent = stats.failed;
    document.getElementById('footerTotal').textContent = stats.total;
}

/**
 * Fetch available source categories
 */
async function fetchSources() {
    try {
        const response = await fetch(`${API_BASE}/api/sources`);
        const data = await response.json();
        
        if (data.success && data.sources.length > 0) {
            renderSourceFilters(data.sources);
        }
    } catch (error) {
        console.error('Error fetching sources:', error);
    }
}

/**
 * Render source filter chips
 */
function renderSourceFilters(sources) {
    const container = document.getElementById('sourceFilters');
    
    // Add source chips after "All"
    sources.forEach(source => {
        const chip = document.createElement('button');
        chip.className = 'chip';
        chip.dataset.source = source;
        chip.textContent = source;
        container.appendChild(chip);
    });
}

/**
 * Fetch jobs with current filters
 */
async function fetchJobs() {
    try {
        showLoading();
        
        const params = new URLSearchParams({
            search: state.filters.search,
            source: state.filters.source,
            status: state.filters.status,
            page: state.currentPage,
            per_page: 50
        });
        
        const response = await fetch(`${API_BASE}/api/jobs?${params}`);
        const data = await response.json();
        
        if (data.success) {
            state.jobs = data.jobs;
            state.totalPages = data.total_pages;
            renderJobs(data.jobs);
            updatePagination(data);
            updateJobsCount(data.total);
        }
    } catch (error) {
        console.error('Error fetching jobs:', error);
        showError('Failed to load jobs. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Render job cards
 */
function renderJobs(jobs) {
    const grid = document.getElementById('jobsGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (jobs.length === 0) {
        grid.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    grid.innerHTML = jobs.map((job, index) => `
        <div class="job-card" style="animation-delay: ${index * 0.05}s">
            <div class="job-card-header">
                <span class="job-label ${job.is_new ? 'new' : 'old'}">
                    ${job.is_new ? '✨ NEW' : 'OLD'}
                </span>
            </div>
            
            <h3 class="job-title">${escapeHtml(job.title)}</h3>
            
            <div class="job-meta">
                <div class="job-meta-item">
                    <span class="job-meta-icon">🏢</span>
                    <span>${escapeHtml(job.company)}</span>
                </div>
                <div class="job-meta-item">
                    <span class="job-meta-icon">📍</span>
                    <span>${escapeHtml(job.location || 'Not specified')}</span>
                </div>
                <div class="job-meta-item">
                    <span class="job-source">${escapeHtml(job.source_category)}</span>
                </div>
            </div>
            
            <div class="job-dates">
                <div class="job-date">
                    <strong>Posted:</strong> ${formatDate(job.posted_date)}
                </div>
                <div class="job-date">
                    <strong>Added:</strong> ${formatDate(job.scraped_date)}
                </div>
            </div>
            
            <div class="job-actions">
                <a href="${escapeHtml(job.url)}" 
                   target="_blank" 
                   class="btn-apply"
                   onclick="markAsApplied(${job.id})">
                    <strong>Apply Now →</strong>
                </a>
            </div>
        </div>
    `).join('');
}

/**
 * Update pagination controls
 */
function updatePagination(data) {
    const pagination = document.getElementById('pagination');
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    
    if (data.total_pages > 1) {
        pagination.style.display = 'flex';
        prevBtn.disabled = data.page === 1;
        nextBtn.disabled = data.page === data.total_pages;
        pageInfo.textContent = `Page ${data.page} of ${data.total_pages}`;
    } else {
        pagination.style.display = 'none';
    }
}

/**
 * Update jobs count display
 */
function updateJobsCount(total) {
    const count = document.getElementById('jobsCount');
    count.textContent = `${total} job${total !== 1 ? 's' : ''}`;
}

/**
 * Mark job as applied
 */
async function markAsApplied(jobId) {
    try {
        const response = await fetch(`${API_BASE}/api/jobs/${jobId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'applied' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Refresh stats
            await fetchStats();
        }
    } catch (error) {
        console.error('Error updating job status:', error);
    }
}

/**
 * Show loading state
 */
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('jobsGrid').style.opacity = '0.5';
}

/**
 * Hide loading state
 */
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('jobsGrid').style.opacity = '1';
}

/**
 * Show error message
 */
function showError(message) {
    // Simple error display - can be enhanced with a toast/notification system
    console.error(message);
    alert(message);
}

/**
 * Utility: Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Utility: Format date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
        
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    } catch (error) {
        return dateString;
    }
}

// Auto-refresh every 5 minutes
setInterval(() => {
    fetchStats();
    fetchJobs();
}, 5 * 60 * 1000);
