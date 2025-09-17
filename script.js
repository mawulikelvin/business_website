// Nicky G. Computers - E-commerce Website JavaScript
// Cart and Product Management System with Mobile Money Integration

class NickyGEcommerce {
    constructor() {
        this.cart = [];
        this.products = [];
        this.services = [];
        this.currentCategory = 'all';
        this.currentSort = 'name';
        this.currentPriceRange = 'all';
        
        this.init();
        this.loadSampleData();
    }

    init() {
        // DOM Elements
        this.cartBtn = document.getElementById('cart-btn');
        this.cartCount = document.getElementById('cart-count');
        this.cartModal = document.getElementById('cart-modal');
        this.confirmationModal = document.getElementById('confirmation-modal');
        this.searchModal = document.getElementById('search-modal');
        
        // Event Listeners
        this.setupEventListeners();
        this.setupMobileMenu();
        this.renderProducts();
        this.updateCartDisplay();
    }

    setupEventListeners() {
        // Cart Modal
        this.cartBtn.addEventListener('click', () => this.openCartModal());
        document.getElementById('close-cart').addEventListener('click', () => this.closeModal('cart-modal'));
        
        // Confirmation Modal
        document.getElementById('close-confirmation').addEventListener('click', () => this.closeModal('confirmation-modal'));
        
        // Search Modal
        document.getElementById('search-btn').addEventListener('click', () => this.openSearchModal());
        document.getElementById('close-search').addEventListener('click', () => this.closeModal('search-modal'));
        document.getElementById('search-submit').addEventListener('click', () => this.performSearch());
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.performSearch();
        });
        
        // Order Form
        document.getElementById('order-form').addEventListener('submit', (e) => this.handleOrderSubmission(e));
        
        // Contact Form
        document.getElementById('contact-form').addEventListener('submit', (e) => this.handleContactForm(e));
        
        // Category Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.filterByCategory(e.target.dataset.category));
        });
        
        // Filters
        document.getElementById('price-range').addEventListener('change', (e) => this.filterByPrice(e.target.value));
        document.getElementById('sort-by').addEventListener('change', (e) => this.sortProducts(e.target.value));
        
        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
        
        // Smooth scrolling for navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href').substring(1);
                this.scrollToSection(target);
            });
        });
    }

    setupMobileMenu() {
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const navMenu = document.getElementById('nav-menu');
        
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    loadSampleData() {
        // Sample Products Data
        this.products = [
            {
                id: 'laptop-hp-001',
                name: 'HP Pavilion 15 Laptop',
                category: 'computers',
                subCategory: 'laptops',
                brand: 'HP',
                price: 3500.00,
                currency: 'GHS',
                shortDescription: 'Powerful laptop for work and entertainment',
                longDescription: 'HP Pavilion 15 with Intel Core i5 processor, 8GB RAM, 256GB SSD, and 15.6-inch Full HD display. Perfect for students and professionals.',
                images: ['💻'],
                stock: 5,
                isFeatured: true,
                attributes: {
                    processor: 'Intel Core i5',
                    ram: '8GB',
                    storage: '256GB SSD',
                    screen_size: '15.6 inch'
                }
            },
            {
                id: 'phone-samsung-001',
                name: 'Samsung Galaxy A54',
                category: 'phones',
                subCategory: 'smartphones',
                brand: 'Samsung',
                price: 1800.00,
                currency: 'GHS',
                shortDescription: 'Feature-rich smartphone with excellent camera',
                longDescription: 'Samsung Galaxy A54 with 128GB storage, 6GB RAM, triple camera system, and long-lasting battery.',
                images: ['phone.jpg'],
                stock: 8,
                isFeatured: true,
                attributes: {
                    storage: '128GB',
                    ram: '6GB',
                    camera: 'Triple Camera',
                    battery: '5000mAh'
                }
            },
            {
                id: 'desktop-dell-001',
                name: 'Dell OptiPlex Desktop',
                category: 'computers',
                subCategory: 'desktops',
                brand: 'Dell',
                price: 2800.00,
                currency: 'GHS',
                shortDescription: 'Reliable desktop computer for office use',
                longDescription: 'Dell OptiPlex desktop with Intel Core i3, 4GB RAM, 500GB HDD, perfect for office work and basic computing needs.',
                images: ['🖥️'],
                stock: 3,
                isFeatured: false,
                attributes: {
                    processor: 'Intel Core i3',
                    ram: '4GB',
                    storage: '500GB HDD',
                    type: 'Desktop'
                }
            },
            {
                id: 'phone-iphone-001',
                name: 'iPhone 12',
                category: 'phones',
                subCategory: 'smartphones',
                brand: 'Apple',
                price: 4200.00,
                currency: 'GHS',
                shortDescription: 'Premium iPhone with advanced features',
                longDescription: 'iPhone 12 with 128GB storage, A14 Bionic chip, dual camera system, and 5G connectivity.',
                images: ['phone.jpg'],
                stock: 2,
                isFeatured: true,
                attributes: {
                    storage: '128GB',
                    chip: 'A14 Bionic',
                    camera: 'Dual Camera',
                    connectivity: '5G'
                }
            },
            {
                id: 'accessory-mouse-001',
                name: 'Wireless Mouse',
                category: 'accessories',
                subCategory: 'peripherals',
                brand: 'Logitech',
                price: 85.00,
                currency: 'GHS',
                shortDescription: 'Ergonomic wireless mouse',
                longDescription: 'Logitech wireless mouse with ergonomic design, long battery life, and precise tracking.',
                images: [''],
                stock: 15,
                isFeatured: false,
                attributes: {
                    type: 'Wireless',
                    battery: 'Long-lasting',
                    design: 'Ergonomic'
                }
            },
            {
                id: 'accessory-keyboard-001',
                name: 'Mechanical Keyboard',
                category: 'accessories',
                subCategory: 'peripherals',
                brand: 'Corsair',
                price: 320.00,
                currency: 'GHS',
                shortDescription: 'RGB mechanical gaming keyboard',
                longDescription: 'Corsair mechanical keyboard with RGB backlighting, tactile switches, and durable construction.',
                images: [''],
                stock: 7,
                isFeatured: false,
                attributes: {
                    type: 'Mechanical',
                    lighting: 'RGB',
                    switches: 'Tactile'
                }
            },
            {
                id: 'stationary-notebook-001',
                name: 'Exercise Books (Pack of 10)',
                category: 'stationary',
                subCategory: 'books',
                brand: 'Local',
                price: 25.00,
                currency: 'GHS',
                shortDescription: 'Quality exercise books for students',
                longDescription: 'Pack of 10 quality exercise books, 80 pages each, suitable for all school subjects.',
                images: [''],
                stock: 50,
                isFeatured: false,
                attributes: {
                    pages: '80 pages',
                    quantity: '10 books',
                    type: 'Exercise Books'
                }
            },
            {
                id: 'stationary-pens-001',
                name: 'Ballpoint Pens (Pack of 12)',
                category: 'stationary',
                subCategory: 'writing',
                brand: 'Bic',
                price: 18.00,
                currency: 'GHS',
                shortDescription: 'Reliable ballpoint pens',
                longDescription: 'Pack of 12 Bic ballpoint pens in blue ink, smooth writing and long-lasting.',
                images: [''],
                stock: 30,
                isFeatured: false,
                attributes: {
                    ink: 'Blue',
                    quantity: '12 pens',
                    brand: 'Bic'
                }
            }
        ];

        // Sample Services Data
        this.services = [
            {
                id: 'service-repair-001',
                name: 'Computer Repair',
                category: 'IT Services',
                description: 'Professional repair services for desktops and laptops, troubleshooting hardware and software issues.',
                durationEstimate: '1-3 hours',
                priceRange: '50-200 GHS',
                availability: 'Walk-in, Mon-Sat',
                icon: '',
                isFeatured: true
            },
            {
                id: 'service-internet-001',
                name: 'Internet Cafe',
                category: 'Digital Services',
                description: 'High-speed internet access, computer usage, printing, and scanning services.',
                durationEstimate: 'Hourly rates',
                priceRange: '2-5 GHS per hour',
                availability: 'Daily, 7am-10pm',
                icon: '',
                isFeatured: true
            }
        ];
    }

    // Product Management
    renderProducts() {
        const featuredGrid = document.getElementById('featured-products-grid');
        const productsGrid = document.getElementById('products-grid');
        
        if (featuredGrid) {
            featuredGrid.innerHTML = this.generateProductsHTML(this.products.filter(p => p.isFeatured).slice(0, 4));
        }
        
        if (productsGrid) {
            const filteredProducts = this.getFilteredProducts();
            productsGrid.innerHTML = this.generateProductsHTML(filteredProducts);
        }
    }

    generateProductsHTML(products) {
        return products.map(product => `
            <div class="product-card fade-in" data-category="${product.category}">
                <div class="product-image">
                    ${product.images[0]}
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-price">GHS ${product.price.toFixed(2)}</p>
                    <p class="product-description">${product.shortDescription}</p>
                    <button class="add-to-cart-btn" onclick="ecommerce.addToCart('${product.id}')">
                        Add to Cart
                    </button>
                </div>
            </div>
        `).join('');
    }

    getFilteredProducts() {
        let filtered = this.products;
        
        // Filter by category
        if (this.currentCategory !== 'all') {
            filtered = filtered.filter(p => p.category === this.currentCategory);
        }
        
        // Filter by price range
        if (this.currentPriceRange !== 'all') {
            const [min, max] = this.currentPriceRange.split('-').map(p => p.replace('+', ''));
            filtered = filtered.filter(p => {
                if (max) {
                    return p.price >= parseInt(min) && p.price <= parseInt(max);
                } else {
                    return p.price >= parseInt(min);
                }
            });
        }
        
        // Sort products
        filtered.sort((a, b) => {
            switch (this.currentSort) {
                case 'price-low':
                    return a.price - b.price;
                case 'price-high':
                    return b.price - a.price;
                case 'featured':
                    return b.isFeatured - a.isFeatured;
                default:
                    return a.name.localeCompare(b.name);
            }
        });
        
        return filtered;
    }

    filterByCategory(category) {
        this.currentCategory = category;
        
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-category="${category}"]`).classList.add('active');
        
        this.renderProducts();
    }

    filterByPrice(priceRange) {
        this.currentPriceRange = priceRange;
        this.renderProducts();
    }

    sortProducts(sortBy) {
        this.currentSort = sortBy;
        this.renderProducts();
    }

    // Cart Management
    addToCart(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;
        
        const existingItem = this.cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({
                ...product,
                quantity: 1
            });
        }
        
        this.updateCartDisplay();
        this.showNotification(`${product.name} added to cart!`);
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.updateCartDisplay();
        this.renderCartItems();
    }

    updateCartQuantity(productId, quantity) {
        const item = this.cart.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            this.updateCartDisplay();
            this.renderCartItems();
        }
    }

    updateCartDisplay() {
        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        this.cartCount.textContent = totalItems;
        
        if (totalItems > 0) {
            this.cartCount.style.display = 'flex';
        } else {
            this.cartCount.style.display = 'none';
        }
    }

    getCartTotal() {
        return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    // Modal Management
    openCartModal() {
        this.renderCartItems();
        this.cartModal.style.display = 'block';
    }

    openSearchModal() {
        this.searchModal.style.display = 'block';
        document.getElementById('search-input').focus();
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    renderCartItems() {
        const cartItemsContainer = document.getElementById('cart-items');
        const cartTotalElement = document.getElementById('cart-total');
        
        if (this.cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="text-center">Your cart is empty</p>';
            cartTotalElement.textContent = '0.00';
            return;
        }
        
        cartItemsContainer.innerHTML = this.cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <p>Quantity: 
                        <button onclick="ecommerce.updateCartQuantity('${item.id}', ${item.quantity - 1})">-</button>
                        ${item.quantity}
                        <button onclick="ecommerce.updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
                    </p>
                </div>
                <div class="cart-item-actions">
                    <p class="cart-item-price">GHS ${(item.price * item.quantity).toFixed(2)}</p>
                    <button onclick="ecommerce.removeFromCart('${item.id}')" style="color: var(--primary-red); background: none; border: none; cursor: pointer;">Remove</button>
                </div>
            </div>
        `).join('');
        
        cartTotalElement.textContent = this.getCartTotal().toFixed(2);
    }

    // Order Management
    handleOrderSubmission(e) {
        e.preventDefault();
        
        if (this.cart.length === 0) {
            this.showNotification('Your cart is empty!', 'error');
            return;
        }
        
        const formData = new FormData(e.target);
        const orderData = {
            customerName: formData.get('name'),
            customerPhone: formData.get('phone'),
            customerMessage: formData.get('message'),
            items: this.cart,
            total: this.getCartTotal(),
            orderDate: new Date().toISOString(),
            orderReference: this.generateOrderReference()
        };
        
        // Show confirmation modal
        this.showOrderConfirmation(orderData);
        
        // Clear cart
        this.cart = [];
        this.updateCartDisplay();
        
        // Close cart modal
        this.closeModal('cart-modal');
    }

    generateOrderReference() {
        const timestamp = Date.now().toString().slice(-6);
        const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
        return `NG${timestamp}${random}`;
    }

    showOrderConfirmation(orderData) {
        document.getElementById('final-total').textContent = orderData.total.toFixed(2);
        document.getElementById('order-reference').textContent = orderData.orderReference;
        
        this.confirmationModal.style.display = 'block';
        
        // Store order data (in a real app, this would be sent to a server)
        console.log('Order placed:', orderData);
    }

    // Search Functionality
    performSearch() {
        const query = document.getElementById('search-input').value.toLowerCase().trim();
        const resultsContainer = document.getElementById('search-results');
        
        if (!query) {
            resultsContainer.innerHTML = '<p>Please enter a search term</p>';
            return;
        }
        
        const results = this.products.filter(product => 
            product.name.toLowerCase().includes(query) ||
            product.shortDescription.toLowerCase().includes(query) ||
            product.category.toLowerCase().includes(query) ||
            product.brand.toLowerCase().includes(query)
        );
        
        if (results.length === 0) {
            resultsContainer.innerHTML = '<p>No products found</p>';
        } else {
            resultsContainer.innerHTML = `
                <h3>Search Results (${results.length})</h3>
                ${this.generateProductsHTML(results)}
            `;
        }
    }

    // Contact Form
    handleContactForm(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const contactData = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            subject: formData.get('subject'),
            message: formData.get('message'),
            timestamp: new Date().toISOString()
        };
        
        // In a real application, this would be sent to a server
        console.log('Contact form submitted:', contactData);
        
        this.showNotification('Thank you for your message! We will get back to you soon.');
        e.target.reset();
    }

    // Utility Functions
    scrollToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const elementPosition = element.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: elementPosition,
                behavior: 'smooth'
            });
        }
    }

    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'error' ? 'var(--primary-red)' : '#10B981'};
            color: white;
            padding: var(--spacing-md);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Global scroll function for hero buttons
function scrollToSection(sectionId) {
    ecommerce.scrollToSection(sectionId);
}

// Initialize the e-commerce system when the page loads
let ecommerce;
document.addEventListener('DOMContentLoaded', () => {
    ecommerce = new NickyGEcommerce();
});

// Add notification animations to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
