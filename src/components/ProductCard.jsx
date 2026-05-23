import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';

const PDP_MAP = {
  "69c856f897378918e2031d54": "pdp_outperformed_by_robot.html",
  "69bb7e1e6291a03e2604a0ec": "pdp_punch_the_monkey.html",
  "69d1b80c2e352db3e70cf7c5": "pdp_peace_sign.html",
  "6a1121add4d1eee5d1083056": "pdp_sage_archives.html",
  "6a1121b24a67803eff0228ad": "pdp_binary_genesis.html",
  "6a1121b7a8fde5fbe80e64b5": "pdp_vaporwave_paradox.html",
  "6a1121bc674926aa27006347": "pdp_neural_echoes.html",
  "6a1121c14a67803eff0228bb": "pdp_pixelated_soul.html"
};

export default function ProductCard({ product, onAddToCart }) {
  const [selectedSize, setSelectedSize] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const isVaulted = product.badge && product.badge.startsWith("VAULT");
  const pdpUrl = `/docs/clothing-ecommerce-design/${PDP_MAP[product.id] || ''}`;

  return (
    <div className={`product-card ${isVaulted ? 'vaulted' : ''}`}>
      <span className="product-badge" style={{ backgroundColor: isVaulted ? '#717572' : 'var(--color-accent)' }}>
        {product.badge}
      </span>
      
      {/* Product Image Viewer with Size Hover Selector Overlay */}
      {product.imageFront ? (
        <a href={pdpUrl} className="product-media-link" style={{ display: 'block', width: '100%', color: 'inherit' }}>
          <div className="product-media">
            <img className="product-img img-model" src={product.imageFront} alt={`${product.title} flat model`} />
            {product.imageBack && (
              <img className="product-img img-flat" src={product.imageBack} alt={`${product.title} flat layup`} />
            )}
            
            {/* Themed Size Selection Overlay on Hover (only if active) */}
            {!isVaulted && (
              <div class="card-size-overlay">
                {product.sizes.map(size => (
                  <button 
                    key={size}
                    className={`chip-btn ${selectedSize === size ? 'active' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      e.preventDefault();
                      setSelectedSize(size);
                    }}
                    aria-label={`Select size ${size}`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            )}
          </div>
        </a>
      ) : (
        <div className="product-media">
          <div className="placeholder-visual">
            <HelpCircle size={48} strokeWidth={1} />
            <span className="placeholder-tag">DESIGN FILES IN SYNC</span>
            <span style={{ fontSize: '0.55rem', color: 'var(--color-text-muted)', fontWeight: 700, letterSpacing: '0.1em' }}>
              ALBY INPUT PENDING
            </span>
          </div>
        </div>
      )}
      
      {/* Product Information */}
      <div className="product-info">
        <div className="product-title-row">
          <a href={pdpUrl} style={{ textDecoration: 'none', color: 'inherit' }}>
            <h3 className="product-title" style={{ transition: 'color var(--transition-fast)' }}>{product.title}</h3>
          </a>
          <span className="product-price" style={{ textDecoration: isVaulted ? 'line-through' : 'none' }}>
            ${product.price.toFixed(2)}
          </span>
        </div>
        
        <p style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: 1.5, marginBottom: '1.25rem', fontWeight: 300 }}>
          {product.description}
        </p>

        {/* Stateful Size Swatches Picker (Active vs. Vaulted) */}
        {!isVaulted ? (
          <div style={{ marginBottom: '1.5rem' }}>
            <span className="spec-text" style={{ fontSize: '9px', display: 'block', marginBottom: '8px', color: 'var(--color-text-muted)' }}>
              SELECT SIZE
            </span>
            <div className="size-picker">
              {product.sizes.map(size => (
                <button 
                  key={size}
                  className={`size-btn ${selectedSize === size ? 'active' : ''}`}
                  onClick={() => setSelectedSize(size)}
                  aria-label={`Select size ${size}`}
                >
                  {size}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div style={{ marginBottom: '1.5rem' }}>
            <span className="spec-text" style={{ fontSize: '9px', display: 'block', marginBottom: '8px', color: '#ea5454', fontWeight: 700 }}>
              DROP CLOSED
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', fontWeight: 300, display: 'block', lineHeight: 1.4 }}>
              This release has reached printing limits and is vaulted.
            </span>
          </div>
        )}
        
        {/* Full-width Direct Add to Cart Button with Micro-Interaction Feedback */}
        <button 
          className={`btn-add-cart ${selectedSize && !isVaulted ? 'ready' : ''}`}
          disabled={isVaulted}
          onClick={() => {
            if (selectedSize) {
              onAddToCart(product, selectedSize);
            } else {
              setFeedback("CHOOSE A SIZE ABOVE!");
              setTimeout(() => setFeedback(null), 2000);
            }
          }}
        >
          {isVaulted ? 'VAULTED / SOLD OUT' : (feedback ? feedback : (selectedSize ? `ADD TO CART` : 'SELECT SIZE'))}
        </button>
      </div>
    </div>
  );
}

