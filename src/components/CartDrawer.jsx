import React, { useState } from 'react';
import { X, Trash2, ShoppingBag, ShieldCheck } from 'lucide-react';

export default function CartDrawer({ 
  isOpen, 
  onClose, 
  cartItems, 
  onUpdateQuantity, 
  onRemoveItem,
  onCheckout 
}) {
  const [isCheckoutLoading, setIsCheckoutLoading] = useState(false);

  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const handleCheckoutClick = () => {
    if (cartItems.length === 0) return;
    setIsCheckoutLoading(true);
    setTimeout(() => {
      onCheckout(subtotal);
      setIsCheckoutLoading(false);
    }, 2000);
  };

  return (
    <>
      {/* Sliding Drawer Overlay */}
      <div 
        className={`cart-drawer-overlay ${isOpen ? 'active' : ''}`}
        onClick={onClose}
      />
      
      {/* Sidebar Cart Container */}
      <aside className={`cart-drawer ${isOpen ? 'active' : ''}`}>
        <div className="cart-header">
          <h3 className="cart-title">
            <ShoppingBag size={18} />
            YOUR DRIP
          </h3>
          <button 
            className="close-cart-btn"
            onClick={onClose}
            aria-label="Close Shopping Cart"
          >
            <X size={20} />
          </button>
        </div>

        {/* Cart Item Grid */}
        <div className="cart-items">
          {cartItems.length === 0 ? (
            <div className="cart-empty-msg">
              <p>YOUR DRIP IS EMPTY.</p>
              <p style={{ marginTop: '1rem', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                FIND TODAY'S MEANING IN THE CATALOG.
              </p>
            </div>
          ) : (
            cartItems.map((item, idx) => (
              <div className="cart-item" key={`${item.id}-${item.size}-${idx}`}>
                {/* Cart Thumbnail Placeholder */}
                <div className="cart-item-media">
                  <div className="cart-item-placeholder">
                    <ShoppingBag size={24} strokeWidth={1.5} />
                  </div>
                </div>
                
                <div className="cart-item-info">
                  <div>
                    <h4 className="cart-item-title">{item.title}</h4>
                    <div className="cart-item-meta">
                      <span>SIZE: {item.size}</span>
                    </div>
                  </div>
                  
                  <div className="cart-item-actions">
                    <div className="qty-counter">
                      <button 
                        className="qty-btn"
                        onClick={() => onUpdateQuantity(item.id, item.size, -1)}
                      >
                        -
                      </button>
                      <span className="qty-val">{item.quantity}</span>
                      <button 
                        className="qty-btn"
                        onClick={() => onUpdateQuantity(item.id, item.size, 1)}
                      >
                        +
                      </button>
                    </div>
                    
                    <span className="cart-item-price">
                      ${(item.price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                </div>
                
                <button 
                  className="remove-item-btn"
                  onClick={() => onRemoveItem(item.id, item.size)}
                  aria-label="Remove Item"
                >
                  <X size={14} />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Footer Billing Block */}
        <div className="cart-footer">
          <div className="cart-summary-row">
            <span className="cart-summary-label">Subtotal</span>
            <span className="cart-summary-value">${subtotal.toFixed(2)}</span>
          </div>
          
          <p style={{ fontSize: '0.65rem', color: 'var(--color-text-secondary)', lineHeight: 1.4, fontWeight: 300 }}>
            Shipping & taxes calculated at checkout. Orders processed immediately and pushed directly to print fulfillment.
          </p>
          
          <button 
            className="btn-checkout"
            onClick={handleCheckoutClick}
            disabled={cartItems.length === 0 || isCheckoutLoading}
          >
            {isCheckoutLoading ? (
              <>
                <svg 
                  className="spinner" 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="16" 
                  height="16" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  style={{ marginRight: '8px' }}
                >
                  <circle cx="12" cy="12" r="10" strokeOpacity={0.25} />
                  <path d="M4 12a8 8 0 0 1 8-8V0C5.37 0 0 5.37 0 12h4z" />
                </svg>
                SECURE ROUTING...
              </>
            ) : (
              <>
                <ShieldCheck size={18} />
                SECURE CHECKOUT
              </>
            )}
          </button>
        </div>
      </aside>
    </>
  );
}
