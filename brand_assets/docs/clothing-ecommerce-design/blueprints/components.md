# Clothing E-Commerce Interactive Component Blueprints

These blueprints contain high-fidelity, highly visual, copy-pasteable **HTML & CSS blueprints** for four essential interactive e-commerce components. Every component relies on the semantic CSS variables defined in the brand themes, ensuring they automatically restyle when hotswapping brand styles.

---

## 1. The Dual-Image Editorial Card

This catalog card features a dual-image reveal where the flat-lay catalog photo seamlessly cross-fades into a body fit/model shot on pointer hover, paired with an elegant scale-up transition and price indicator.

### Component Markup (HTML)

```html
<div class="product-card">
  <div class="product-media">
    <!-- Model fit shot (Default background display) -->
    <img src="/assets/product-model.jpg" alt="Sage T-Shirt Fit" class="product-img img-model" />
    <!-- Flat-lay shot (Revealed on hover) -->
    <img src="/assets/product-flat.jpg" alt="Sage T-Shirt Detail" class="product-img img-flat" />
    <span class="product-badge">New Drop</span>
    
    <!-- Hover size-chips selection trigger -->
    <div class="hover-size-overlay">
      <span class="size-chip" data-size="S">S</span>
      <span class="size-chip" data-size="M">M</span>
      <span class="size-chip" data-size="L">L</span>
      <span class="size-chip" data-size="XL">XL</span>
    </div>
  </div>
  
  <div class="product-info">
    <div class="product-title-row">
      <h3 class="product-title">Sage Essential Tee</h3>
      <span class="product-price">$38.00</span>
    </div>
    <button class="btn-add-cart">Add to Cart</button>
  </div>
</div>
```

### Component Styling (CSS)

```css
.product-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-glass);
  border-radius: var(--border-radius-card, 8px);
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.product-card:hover {
  transform: translateY(-8px);
  border-color: var(--border-light);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
}

.product-media {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4; /* Editorial portrait aspect ratio */
  overflow: hidden;
}

.product-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), 
              transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Image Cross-fade logic */
.product-img.img-flat {
  opacity: 0;
}

.product-card:hover .product-img.img-model {
  opacity: 0;
  transform: scale(1.05);
}

.product-card:hover .product-img.img-flat {
  opacity: 1;
  transform: scale(1.02);
}

.product-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  background: var(--color-accent);
  color: var(--bg-base);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 6px 12px;
  border-radius: 4px;
}

/* Hover size overlay drawer */
.hover-size-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(0deg, rgba(0, 0, 0, 0.4) 0%, transparent 100%);
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 24px 16px 16px 16px;
  transform: translateY(100%);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 5;
}

.product-card:hover .hover-size-overlay {
  transform: translateY(0);
  opacity: 1;
}

.size-chip {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.9);
  color: #111;
  font-size: 11px;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.size-chip:hover {
  background: var(--color-accent);
  color: var(--bg-base);
  transform: scale(1.1);
}

.product-info {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.product-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.product-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-primary);
}

.product-price {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-accent);
}

.btn-add-cart {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-glass);
  color: var(--color-text-primary);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 14px;
  border-radius: var(--border-radius-button, 4px);
  cursor: pointer;
  width: 100%;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-add-cart:hover {
  background: var(--color-accent);
  color: var(--bg-base);
  border-color: var(--color-accent);
}
```

---

## 2. Dynamic Glassmorphic Navigation Header

This header features an dynamic layout which sits fully transparently over full-bleed hero media sections on page load, and morphs into a frosted glass backdrop once scrolled ≥ 80px from top.

### Component Markup (HTML)

```html
<header class="header header-fixed header-transparent" id="site-header">
  <div class="container header-container">
    <a href="/" class="logo-link">
      <img src="/assets/logo.png" alt="Daily Drip Logo" class="logo-img" />
    </a>
    
    <nav class="nav-links">
      <a href="#catalog" class="nav-link active">Catalog</a>
      <a href="#story" class="nav-link">Our Story</a>
      <a href="#drops" class="nav-link">Drops</a>
    </nav>
    
    <div class="nav-actions">
      <button class="icon-btn cart-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        <span class="cart-count">2</span>
      </button>
    </div>
  </div>
</header>
```

### Component Styling (CSS)

```css
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 100;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-bottom: 1px solid transparent;
}

/* Glassmorphism activation class injected via JS on scroll */
.header.scrolled {
  height: 68px;
  background: var(--bg-glass);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border-glass);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo-img {
  height: 38px;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.header.scrolled .logo-img {
  height: 30px;
}

.nav-links {
  display: flex;
  gap: 40px;
}

.nav-link {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-secondary);
  position: relative;
  padding: 8px 0;
}

.nav-link:hover, .nav-link.active {
  color: var(--color-text-primary);
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-accent);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.nav-link:hover::after, .nav-link.active::after {
  width: 100%;
}

.cart-btn {
  position: relative;
  background: none;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
  padding: 8px;
  display: flex;
}

.cart-count {
  position: absolute;
  top: 0px;
  right: 0px;
  background: var(--color-accent);
  color: var(--bg-base);
  font-size: 9px;
  font-weight: 900;
  min-width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 10px rgba(var(--color-accent-rgb), 0.3);
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Badge scale pop dynamic click */
.cart-count.pop {
  transform: scale(1.3);
}
```

---

## 3. The Soft Out-of-Stock Size Picker

This component displays a size selector where out-of-stock sizes remain visible but styled at low opacity with a diagonal strike-through, preserving design balance while preventing selection errors.

### Component Markup (HTML)

```html
<div class="size-selector-block">
  <span class="selector-label">Select Size</span>
  <div class="size-grid">
    <button class="size-btn" data-size="S">S</button>
    <button class="size-btn" data-size="M">M</button>
    <button class="size-btn size-out-of-stock" data-size="L" disabled>L</button>
    <button class="size-btn" data-size="XL">XL</button>
  </div>
</div>
```

### Component Styling (CSS)

```css
.size-selector-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.selector-label {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-secondary);
}

.size-grid {
  display: flex;
  gap: 8px;
}

.size-btn {
  width: 48px;
  height: 48px;
  border: 1px solid var(--border-glass);
  background: var(--bg-surface-elevated);
  color: var(--color-text-primary);
  font-size: 12px;
  font-weight: 700;
  border-radius: var(--border-radius-card, 4px);
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.size-btn:hover:not(:disabled) {
  border-color: var(--color-text-primary);
  background: var(--bg-base);
}

.size-btn.active {
  background: var(--color-text-primary);
  color: var(--bg-base);
  border-color: var(--color-text-primary);
}

/* Soft out-of-stock diagonal strike-through styling */
.size-btn.size-out-of-stock {
  opacity: 0.35;
  cursor: not-allowed;
  background: var(--bg-surface);
  border-color: var(--border-glass);
}

.size-btn.size-out-of-stock::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top right, 
              transparent calc(50% - 0.5px), 
              var(--color-text-primary) 50%, 
              transparent calc(50% + 0.5px));
  pointer-events: none;
}
```

---

## 4. Frosted Glass Checkout Drawer

The slide-out drawer occupies exactly the right portion of the screen, utilizing frosted glassmorphism overlays and dark backdrop animations.

### Component Markup (HTML)

```html
<!-- Background Backdrop overlay mask -->
<div class="cart-backdrop active"></div>

<!-- Slide-out Drawer Panel -->
<div class="cart-drawer open">
  <div class="cart-drawer-header">
    <h2 class="cart-drawer-title">Shopping Cart (2)</h2>
    <button class="close-drawer-btn">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </button>
  </div>
  
  <div class="cart-drawer-items">
    <!-- Item block -->
    <div class="cart-item">
      <img src="/assets/product-thumbnail.jpg" alt="Sage Tee" class="cart-item-img" />
      <div class="cart-item-details">
        <h4 class="cart-item-name">Sage Essential Tee</h4>
        <span class="cart-item-meta">Size: XL</span>
        <div class="cart-item-actions">
          <div class="qty-stepper">
            <button class="qty-btn">-</button>
            <span class="qty-val">1</span>
            <button class="qty-btn">+</button>
          </div>
          <span class="cart-item-price">$38.00</span>
        </div>
      </div>
    </div>
  </div>
  
  <div class="cart-drawer-footer">
    <div class="cart-total-row">
      <span>Subtotal</span>
      <span>$38.00</span>
    </div>
    <button class="btn-checkout">Proceed to Checkout</button>
  </div>
</div>
```

### Component Styling (CSS)

```css
/* Dark backdrop mask */
.cart-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  z-index: 200;
  opacity: 0;
  pointer-events: none;
  backdrop-filter: blur(4px);
  transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.cart-backdrop.active {
  opacity: 1;
  pointer-events: auto;
}

/* Sliding Cart Panel */
.cart-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  max-width: 420px;
  height: 100vh;
  z-index: 201;
  background: var(--bg-glass);
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);
  border-left: 1px solid var(--border-glass);
  box-shadow: -10px 0 40px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.cart-drawer.open {
  transform: translateX(0);
}

.cart-drawer-header {
  padding: 32px 24px;
  border-bottom: 1px solid var(--border-glass);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-drawer-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-primary);
}

.close-drawer-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-primary);
}

.cart-drawer-items {
  flex-grow: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  display: flex;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-glass);
}

.cart-item-img {
  width: 80px;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  border-radius: var(--border-radius-card, 4px);
  border: 1px solid var(--border-glass);
  background: var(--bg-surface);
}

.cart-item-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.cart-item-name {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.cart-item-meta {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-bottom: 12px;
}

.cart-item-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.qty-stepper {
  display: flex;
  align-items: center;
  border: 1px solid var(--border-glass);
  border-radius: 4px;
  overflow: hidden;
  background: var(--bg-surface-elevated);
}

.qty-btn {
  width: 28px;
  height: 28px;
  cursor: pointer;
  font-weight: 700;
  transition: background 0.2s ease;
}

.qty-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

.qty-val {
  padding: 0 12px;
  font-size: 12px;
  font-weight: 700;
}

.cart-item-price {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-accent);
}

.cart-drawer-footer {
  padding: 32px 24px;
  border-top: 1px solid var(--border-glass);
  background: rgba(255, 255, 255, 0.3);
}

.cart-total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
}

.btn-checkout {
  background: var(--color-accent);
  color: var(--bg-base);
  border: none;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 16px;
  width: 100%;
  cursor: pointer;
  border-radius: var(--border-radius-button, 4px);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 20px rgba(var(--color-accent-rgb), 0.15);
}

.btn-checkout:hover {
  background: var(--color-text-primary);
  transform: translateY(-2px);
  box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}
```
