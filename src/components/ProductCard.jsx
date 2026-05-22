import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';

const PDP_MAP = {
  prod_robot_012: "pdp_outperformed_by_robot.html",
  prod_monkey_011: "pdp_punch_the_monkey.html",
  prod_peace_010: "pdp_peace_sign.html",
  prod_sage_009: "pdp_sage_archives.html",
  prod_binary_008: "pdp_binary_genesis.html",
  prod_vapor_007: "pdp_vaporwave_paradox.html",
  prod_neural_006: "pdp_neural_echoes.html",
  prod_pixel_005: "pdp_pixelated_soul.html"
};

export default function ProductCard({ product, onAddToCart }) {
  const [selectedSize, setSelectedSize] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const pdpUrl = `/docs/clothing-ecommerce-design/${PDP_MAP[product.id] || ''}`;

  return (
    <div className="product-card">
      <span className="product-badge">{product.badge}</span>
      
      {/* Product Image Viewer with Size Hover Selector Overlay */}
      {product.imageFront ? (
        <a href={pdpUrl} className="product-media-link" style={{ display: 'block', width: '100%', color: 'inherit' }}>
          <div className="product-media">
            <img className="product-img img-model" src={product.imageFront} alt={`${product.title} flat model`} />
            {product.imageBack && (
              <img className="product-img img-flat" src={product.imageBack} alt={`${product.title} flat layup`} />
            )}
            
            {/* Themed Size Selection Overlay on Hover */}
            <div className="card-size-overlay">
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
          <span className="product-price">${product.price.toFixed(2)}</span>
        </div>
        
        <p style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: 1.5, marginBottom: '1.25rem', fontWeight: 300 }}>
          {product.description}
        </p>

        {/* Stateful Size Swatches Picker */}
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
        
        {/* Full-width Direct Add to Cart Button with Micro-Interaction Feedback */}
        <button 
          className={`btn-add-cart ${selectedSize ? 'ready' : ''}`}
          onClick={() => {
            if (selectedSize) {
              onAddToCart(product, selectedSize);
            } else {
              setFeedback("CHOOSE A SIZE ABOVE!");
              setTimeout(() => setFeedback(null), 2000);
            }
          }}
        >
          {feedback ? feedback : (selectedSize ? `ADD TO CART` : 'SELECT SIZE')}
        </button>
      </div>
    </div>
  );
}

