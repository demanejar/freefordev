// Global state
let categoriesData = [];
let currentFilter = 'all';
let searchQuery = '';
let currentModalCategory = null;
let modalSearchQuery = '';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const clearSearch = document.getElementById('clearSearch');
const categoriesGrid = document.getElementById('categoriesGrid');
const noResults = document.getElementById('noResults');
const filterButtons = document.querySelectorAll('.filter-btn');
const totalServices = document.getElementById('totalServices');
const totalCategories = document.getElementById('totalCategories');

// Modal Elements
const modal = document.getElementById('servicesModal');
const modalClose = document.getElementById('modalClose');
const modalTitle = document.getElementById('modalTitle');
const modalSubtitle = document.getElementById('modalSubtitle');
const modalIcon = document.getElementById('modalIcon');
const modalBody = document.getElementById('modalBody');
const modalSearchInput = document.getElementById('modalSearchInput');

// Load data from JSON file
async function loadData() {
    try {
        const response = await fetch('data.json');
        categoriesData = await response.json();
        console.log(`✅ Loaded ${categoriesData.length} categories with ${getTotalServices()} services`);
        init();
    } catch (error) {
        console.error('❌ Error loading data:', error);
        categoriesData = [];
        init();
    }
}

// Get total services count
function getTotalServices() {
    return categoriesData.reduce((sum, cat) => sum + cat.services.length, 0);
}

// Initialize
function init() {
    updateStats();
    renderCategories();
    setupEventListeners();
}

// Update statistics
function updateStats() {
    const totalServicesCount = getTotalServices();
    totalServices.textContent = totalServicesCount > 0 ? `${totalServicesCount}` : '500+';
    totalCategories.textContent = categoriesData.length > 0 ? `${categoriesData.length}` : '40+';
}

// Render categories
function renderCategories() {
    const filteredCategories = getFilteredCategories();

    if (filteredCategories.length === 0) {
        categoriesGrid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }

    categoriesGrid.style.display = 'grid';
    noResults.style.display = 'none';

    categoriesGrid.innerHTML = filteredCategories.map((category, index) => {
        const displayServices = category.services.slice(0, 5);
        const hasMore = category.services.length > 5;

        return `
            <div class="category-card" data-category-id="${category.id}" style="animation: fadeInUp 0.6s ease ${index * 0.05}s backwards;">
                <div class="category-header">
                    <div class="category-icon">${category.icon}</div>
                    <div>
                        <h3 class="category-title">${category.title}</h3>
                        <span class="category-count">${category.services.length} service${category.services.length !== 1 ? 's' : ''}</span>
                    </div>
                </div>
                <p class="category-description">${category.description}</p>
                <div class="service-list">
                    ${displayServices.map(service => `
                        <div class="service-item">
                            <div>
                                <a href="${service.url}" target="_blank" rel="noopener noreferrer" class="service-link">
                                    ${escapeHtml(service.name)}
                                </a>
                                <p class="service-description">${escapeHtml(service.description)}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                ${hasMore ? `
                    <button class="expand-btn" data-category-id="${category.id}">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"></path>
                        </svg>
                        <span>View all ${category.services.length} services</span>
                    </button>
                ` : ''}
            </div>
        `;
    }).join('');

    // Add click handlers for expand buttons
    document.querySelectorAll('.expand-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const categoryId = btn.dataset.categoryId;
            openModal(categoryId);
        });
    });

    animateOnScroll();
}

// Open modal with category services
function openModal(categoryId) {
    const category = categoriesData.find(cat => cat.id === categoryId);
    if (!category) return;

    currentModalCategory = category;
    modalSearchQuery = '';
    modalSearchInput.value = '';

    // Update modal header
    modalIcon.textContent = category.icon;
    modalTitle.textContent = category.title;
    modalSubtitle.textContent = `${category.services.length} services available`;

    // Render services
    renderModalServices();

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    currentModalCategory = null;
    modalSearchQuery = '';
}

// Render modal services
function renderModalServices() {
    if (!currentModalCategory) return;

    let services = currentModalCategory.services;

    // Filter by search query
    if (modalSearchQuery) {
        services = services.filter(service =>
            service.name.toLowerCase().includes(modalSearchQuery) ||
            service.description.toLowerCase().includes(modalSearchQuery)
        );
    }

    if (services.length === 0) {
        modalBody.innerHTML = `
            <div class="modal-no-results">
                <div class="modal-no-results-icon">🔍</div>
                <h3>No services found</h3>
                <p>Try adjusting your search query</p>
            </div>
        `;
        return;
    }

    modalBody.innerHTML = `
        <div class="modal-services-grid">
            ${services.map(service => `
                <div class="modal-service-card">
                    <a href="${service.url}" target="_blank" rel="noopener noreferrer" class="modal-service-link">
                        ${escapeHtml(service.name)}
                    </a>
                    <p class="modal-service-description">${escapeHtml(service.description)}</p>
                </div>
            `).join('')}
        </div>
    `;
}

// Get filtered categories
function getFilteredCategories() {
    let filtered = categoriesData;

    if (currentFilter !== 'all') {
        filtered = filtered.filter(cat => cat.id === currentFilter);
    }

    if (searchQuery) {
        filtered = filtered.filter(category => {
            const titleMatch = category.title.toLowerCase().includes(searchQuery);
            const descMatch = category.description.toLowerCase().includes(searchQuery);
            const serviceMatch = category.services.some(service =>
                service.name.toLowerCase().includes(searchQuery) ||
                service.description.toLowerCase().includes(searchQuery)
            );
            return titleMatch || descMatch || serviceMatch;
        });
    }

    return filtered;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Setup event listeners
function setupEventListeners() {
    // Search input
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        clearSearch.style.display = searchQuery ? 'block' : 'none';
        renderCategories();
    });

    // Clear search
    clearSearch.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        clearSearch.style.display = 'none';
        renderCategories();
    });

    // Filter buttons
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.category;
            renderCategories();
        });
    });

    // Modal close button
    modalClose.addEventListener('click', closeModal);

    // Click outside modal to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Modal search
    modalSearchInput.addEventListener('input', (e) => {
        modalSearchQuery = e.target.value.toLowerCase().trim();
        renderModalServices();
    });

    // Escape key to close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (modal.classList.contains('active')) {
                closeModal();
            } else if (document.activeElement === searchInput) {
                searchInput.value = '';
                searchQuery = '';
                clearSearch.style.display = 'none';
                renderCategories();
                searchInput.blur();
            }
        }

        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (!modal.classList.contains('active')) {
                searchInput.focus();
            }
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animate elements on scroll
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.category-card').forEach(card => {
        observer.observe(card);
    });
}

// Add loading state
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Start the app by loading data
loadData();
