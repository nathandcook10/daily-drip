import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';

export default function ProductCard({ product, onAddToCart }) {
  const [selectedSize, setSelectedSize] = useState('M');

  return (
    <div className="product-card">
      <span className="product-badge">{product.badge}</span>
      
      {/* Product Image Viewer (Supports dynamic hover swap and Alby visual placeholders) */}
      <div className="product-media">
        {product.imageFront ? (
          <>
            <img className="product-img img-model" src={product.imageFront} alt={`${product.title} flat model`} />
            {product.imageBack && (
              <img className="product-img img-flat" src={product.imageBack} alt={`${product.title} flat layup`} />
            )}
          </>
        ) : (
          <div className="placeholder-visual">
            <HelpCircle size={48} strokeWidth={1} />
            <span className="placeholder-tag">DESIGN FILES IN SYNC</span>
            <span style={{ fontSize: '0.55rem', color: 'var(--color-text-muted)', fontWeight: 700, letterSpacing: '0.1em' }}>
              ALBY INPUT PENDING
            </span>
          </div>
        )}
      </div>
      
      {/* Product Information */}
      <div className="product-info">
        <div className="product-title-row">
          <h3 className="product-title">{product.title}</h3>
          <span className="product-price">${product.price.toFixed(2)}</span>
        </div>
        
        <p style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: 1.5, marginBottom: '2rem', fontWeight: 300 }}>
          {product.description}
        </p>
        
        {/* Purchase Options */}
        <div className="product-actions-row">
          <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.1em', color: 'var(--color-text-muted)' }}>
            Select Size
          </div>
          
          <div className="size-picker">
            {product.sizes.map(s => (
              <button 
                key={s}
                className={`size-btn ${selectedSize === s ? 'active' : ''}`}
                onClick={() => setSelectedSize(s)}
              >
                {s}
              </button>
            ))}
          </div>
          
          <button 
            className="btn-add-cart"
            onClick={() => onAddToCart(product, selectedSize)}
          >
            ADD TO CART
          </button>
        </div>
      </div>
    </div>
  );
}
