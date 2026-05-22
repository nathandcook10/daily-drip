import React from 'react';
import ProductCard from './ProductCard';
import { ArrowRight } from 'lucide-react';

const PRODUCTS = [
  {
    id: "prod_robot_012",
    title: "Outperformed by a ROBOT. Again.",
    price: 29.99,
    badge: "TODAY'S DRIP #012",
    description: "A bold streetwear graphic celebrating the inevitable takeover of our digital counterparts. Outperformed, but stylish.",
    imageFront: "/assets/flats/flat_robot_front.png",
    imageBack: "/assets/flats/flat_robot_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_monkey_011",
    title: "Punch the Monkey",
    price: 29.99,
    badge: "ARCHIVE #011",
    description: "Classic vintage vibes meets modern street expression. A playful take on cultural nostalgia.",
    imageFront: "/assets/flats/flat_monkey_front.png",
    imageBack: "/assets/flats/flat_monkey_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_peace_010",
    title: "Peace Sign and Hands T-Shirt",
    price: 29.99,
    badge: "ARCHIVE #010",
    description: "Iconic streetwear symbol of peace, connection, and visual expression. An elegant dark-mode fit.",
    imageFront: "/assets/flats/flat_peace_front.png",
    imageBack: "/assets/flats/flat_peace_back.png",
    sizes: ["S", "M", "L", "XL"]
  }
];

export default function ProductList({ onAddToCart, onShopAllClick }) {
  return (
    <section className="catalog" id="catalog">
      <div className="container">
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
          {PRODUCTS.map(product => (
            <ProductCard 
              key={product.id}
              product={product}
              onAddToCart={onAddToCart}
            />
          ))}

          {/* Shop All Vault Placeholder Card */}
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
        </div>
      </div>
    </section>
  );
}
