import React, { useState } from 'react';
import ProductCard from './ProductCard';
import { ArrowRight } from 'lucide-react';

const PRODUCTS = [
  {
    id: "69c856f897378918e2031d54",
    title: "Outperformed by a ROBOT. Again.",
    price: 29.99,
    badge: "TODAY'S DRIP #012",
    description: "A bold streetwear graphic celebrating the inevitable takeover of our digital counterparts. Outperformed, but stylish.",
    imageFront: "/assets/flats/flat_robot_front.png",
    imageBack: "/assets/flats/flat_robot_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "TECH"
  },
  {
    id: "69bb7e1e6291a03e2604a0ec",
    title: "Punch the Monkey",
    price: 29.99,
    badge: "ARCHIVE #011",
    description: "Classic vintage vibes meets modern street expression. A playful take on cultural nostalgia.",
    imageFront: "/assets/flats/flat_monkey_front.png",
    imageBack: "/assets/flats/flat_monkey_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "RETRO"
  },
  {
    id: "69d1b80c2e352db3e70cf7c5",
    title: "Peace Sign and Hands T-Shirt",
    price: 29.99,
    badge: "ARCHIVE #010",
    description: "Iconic streetwear symbol of peace, connection, and visual expression. An elegant dark-mode fit.",
    imageFront: "/assets/flats/flat_peace_front.png",
    imageBack: "/assets/flats/flat_peace_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "RETRO"
  }
];

const VAULTED_PRODUCTS = [
  {
    id: "6a1121add4d1eee5d1083056",
    title: "Sage Archives Graphic Tee",
    price: 29.99,
    badge: "VAULT #009",
    description: "A calm organic streetwear catalog design with intelligence. Hand-printed on heavy cotton.",
    imageFront: "/assets/flats/flat_sage_front.png",
    imageBack: "/assets/flats/flat_sage_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "TECH"
  },
  {
    id: "6a1121b24a67803eff0228ad",
    title: "Binary Genesis",
    price: 34.99,
    badge: "VAULT #008",
    description: "Visualizing the dawn of artificial cognition. A rich tapestry of binary matrices and biological forms.",
    imageFront: "/assets/flats/flat_binary_front.png",
    imageBack: "/assets/flats/flat_binary_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "TECH"
  },
  {
    id: "6a1121b7a8fde5fbe80e64b5",
    title: "Vaporwave Paradox",
    price: 29.99,
    badge: "VAULT #007",
    description: "Glitch art aesthetic detailing consumerist nostalgia and cyberspace relics in neon slate.",
    imageFront: "/assets/flats/flat_vapor_front.png",
    imageBack: "/assets/flats/flat_vapor_back.png",
    sizes: ["S", "M", "L", "XL"],
    category: "RETRO"
  }
];

export default function ProductList({ onAddToCart, onShopAllClick }) {
  const [activeCategory, setActiveCategory] = useState('ALL');

  // Filter lists based on selected category tab
  const filteredActive = PRODUCTS.filter(p => 
    activeCategory === 'ALL' ? true : p.category === activeCategory
  );

  const filteredVaulted = VAULTED_PRODUCTS.filter(p => 
    activeCategory === 'ALL' ? true : p.category === activeCategory
  );

  // Counts for badge chips
  const totalCount = PRODUCTS.length + VAULTED_PRODUCTS.length;
  const techCount = PRODUCTS.filter(p => p.category === 'TECH').length + VAULTED_PRODUCTS.filter(p => p.category === 'TECH').length;
  const retroCount = PRODUCTS.filter(p => p.category === 'RETRO').length + VAULTED_PRODUCTS.filter(p => p.category === 'RETRO').length;

  return (
    <section className="catalog" id="catalog">
      <div className="container">
        
        {/* Capsule Category Navigation Tabs Chips */}
        <div className="capsule-tabs-container">
          <button 
            className={`capsule-tab-chip ${activeCategory === 'ALL' ? 'active' : ''}`}
            onClick={() => setActiveCategory('ALL')}
          >
            All Drops <span className="count">({totalCount})</span>
          </button>
          <button 
            className={`capsule-tab-chip ${activeCategory === 'TECH' ? 'active' : ''}`}
            onClick={() => setActiveCategory('TECH')}
          >
            [ 01 / TECH & DATA ] <span class="count">({techCount})</span>
          </button>
          <button 
            className={`capsule-tab-chip ${activeCategory === 'RETRO' ? 'active' : ''}`}
            onClick={() => setActiveCategory('RETRO')}
          >
            [ 02 / RETRO NOSTALGIA ] <span class="count">({retroCount})</span>
          </button>
        </div>

        {/* SECTION 1: ACTIVE DRIPS GRID */}
        <div>
          <div className="section-header">
            <div>
              <h2 className="section-title">ACTIVE <span>DRIPS</span></h2>
              <p className="section-subtitle" style={{ marginTop: '1rem' }}>
                A fresh visual release. Once sold out, these designs are vaulted and never printed again.
              </p>
            </div>
            <div className="section-subtitle">
              All printings are produced sustainably using direct-to-garment organic cotton blanks by Printify.
            </div>
          </div>
          
          <div className="product-grid">
            {filteredActive.map(product => (
              <ProductCard 
                key={product.id}
                product={product}
                onAddToCart={onAddToCart}
              />
            ))}

            {/* Shop All Vault Placeholder Card - Displayed in active grid if 'ALL' or 'RETRO' selected */}
            {(activeCategory === 'ALL' || activeCategory === 'RETRO') && (
              <div className="product-card shop-all-card" onClick={onShopAllClick}>
                <div className="product-media shop-all-media">
                  <div className="shop-all-visual">
                    <span className="spec-text" style={{ fontSize: '9px', marginBottom: '8px', color: 'var(--color-accent-secondary)' }}>
                      ARCHIVE CATALOGUE
                    </span>
                    <h3 className="shop-all-title">SHOP ALL</h3>
                    <p className="shop-all-desc">Explore the full collection of past design drops</p>
                    <div className="shop-all-arrow-circle">
                      <ArrowRight size={20} className="shop-all-arrow" />
                    </div>
                  </div>
                </div>
                <div className="product-info" style={{ justifyContent: 'center', alignItems: 'center', textAlign: 'center', background: 'transparent' }}>
                  <span className="spec-text" style={{ fontSize: '10px', color: 'var(--color-text-secondary)', fontWeight: 700 }}>
                    EXPLORE VAULT
                  </span>
                  <span style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                    8 TOTAL DESIGNS
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* SECTION 2: RECENTLY VAULTED GRID (FOMO GENERATOR) */}
        {filteredVaulted.length > 0 && (
          <div style={{ marginTop: '100px' }}>
            <div className="section-header">
              <div>
                <h2 className="section-title">RECENTLY <span>VAULTED</span></h2>
                <p className="section-subtitle" style={{ marginTop: '1rem' }}>
                  These designs have reached their printing limit. Once sold out, they are locked in the vault forever.
                </p>
              </div>
              <div className="section-subtitle" style={{ color: '#ea5454', fontWeight: 700 }}>
                CLOSED ARCHIVE • SOLD OUT
              </div>
            </div>
            
            <div className="product-grid">
              {filteredVaulted.map(product => (
                <ProductCard 
                  key={product.id}
                  product={product}
                  onAddToCart={onAddToCart}
                />
              ))}
            </div>

            {/* Bottom Action CTA to Archive Vault view */}
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '60px' }}>
              <button 
                className="story-cta" 
                style={{ cursor: 'pointer', background: 'none', borderBottom: '1px solid var(--color-accent)', paddingBottom: '4px', display: 'inline-flex', alignItems: 'center' }}
                onClick={onShopAllClick}
              >
                EXPLORE COMPLETE VAULT ARCHIVE
                <ArrowRight size={16} style={{ marginLeft: '8px' }} />
              </button>
            </div>
          </div>
        )}

      </div>
    </section>
  );
}
