import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import ProductList from './components/ProductList';
import ArchiveList from './components/ArchiveList';
import CartDrawer from './components/CartDrawer';
import Footer from './components/Footer';
import { ArrowRight, Bell } from 'lucide-react';

export default function App() {
  // --- States ---
  const [view, setView] = useState('home');
  const [cart, setCart] = useState(() => {
    const saved = localStorage.getItem('daily_drip_cart_react');
    return saved ? JSON.parse(saved) : [];
  });
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [toasts, setToasts] = useState([]);

  // --- Effects ---
  useEffect(() => {
    localStorage.setItem('daily_drip_cart_react', JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('success') === 'true') {
      setCart([]);
      showToast("🎉 Payment Successful! Order created sustainably.");
      
      // Scrub query parameters from browser URL
      const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
      window.history.replaceState({ path: newUrl }, '', newUrl);
    } else if (params.get('canceled') === 'true') {
      showToast("⚠️ Payment Canceled. Cart items preserved.");
      
      // Scrub query parameters
      const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
      window.history.replaceState({ path: newUrl }, '', newUrl);
    }
  }, []);

  // --- Toast Manager ---
  const showToast = (message) => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 4000);
  };

  // --- Cart Actions ---
  const handleAddToCart = (product, size) => {
    setCart(prev => {
      const idx = prev.findIndex(item => item.id === product.id && item.size === size);
      if (idx > -1) {
        const next = [...prev];
        next[idx].quantity += 1;
        return next;
      } else {
        return [...prev, {
          id: product.id,
          title: product.title,
          price: product.price,
          size: size,
          image: product.imageFront || '/assets/logo-icon.png', // Use real product image thumbnail!
          quantity: 1
        }];
      }
    });
    
    showToast(`Added ${product.title} (${size}) to Cart`);
    setIsCartOpen(true);
  };

  const handleUpdateQuantity = (productId, size, change) => {
    setCart(prev => {
      const idx = prev.findIndex(item => item.id === productId && item.size === size);
      if (idx === -1) return prev;
      
      const next = [...prev];
      next[idx].quantity += change;
      
      if (next[idx].quantity <= 0) {
        return next.filter((_, i) => i !== idx);
      }
      return next;
    });
  };

  const handleRemoveItem = (productId, size) => {
    setCart(prev => prev.filter(item => !(item.id === productId && item.size === size)));
    showToast(`Item removed from Cart`);
  };

  const handleCheckout = async (total) => {
    try {
      showToast("Redirecting to Secure Checkout...");
      
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items: cart }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Failed to create checkout session.");
      }

      const data = await response.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        throw new Error("No checkout URL returned from server.");
      }
    } catch (error) {
      console.error("Checkout failed:", error);
      alert(`❌ CHECKOUT ERROR\n\n${error.message}`);
    }
  };

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Dynamic Glassmorphic Navigation */}
      <Header 
        cartCount={cartCount} 
        onCartOpen={() => setIsCartOpen(true)} 
        view={view}
        setView={setView}
      />

      {view === 'archive' ? (
        <ArchiveList 
          onAddToCart={handleAddToCart} 
          onBack={() => setView('home')} 
        />
      ) : (
        <>
          {/* Streetwear Intro Section */}
          <Hero />

          {/* Repeating Text Marquee Loop */}
          <section className="marquee-container">
            <div className="marquee-content">
              <span>DAILY CAPTURE IN WEARABLE ART</span>
              <span>ZERO EXCESS STOCK</span>
              <span>OUTPERFORMED BY A ROBOT</span>
              <span>HUMAN MEANING IN APPAREL</span>
              <span>DAILY CAPTURE IN WEARABLE ART</span>
              <span>ZERO EXCESS STOCK</span>
              <span>OUTPERFORMED BY A ROBOT</span>
              <span>HUMAN MEANING IN APPAREL</span>
            </div>
          </section>

          {/* Dynamic Interactive Product Grid */}
          <ProductList 
            onAddToCart={handleAddToCart} 
            onShopAllClick={() => setView('archive')} 
          />

          {/* Narrative Story Section */}
          <section className="story" id="story">
            <div className="container story-grid">
              {/* Brand Visual artwork from Core Art */}
              <div className="story-media">
                <img className="story-img" src="/assets/design-element.png" alt="Brand visual artwork" />
                <div className="story-overlay" />
              </div>
              
              <div className="story-content">
                <h2 className="story-title">EACH T-SHIRT IS A CANVAS</h2>
                <p className="story-desc">
                  We believe clothes shouldn’t be billboards for corporations, but canvases for daily meaning. Collaborating with advanced creative intelligences, we design daily t-shirts that encapsulate human emotion, technology shifts, and modern philosophy.
                </p>
                <p className="story-desc">
                  By utilizing a zero-waste print-on-demand cycle, we ensure that every single garment has an owner waiting for it. Zero excess stock, maximum human engagement.
                </p>
                <a href="#catalog" className="story-cta">
                  VIEW THE RELEASES
                  <ArrowRight size={16} style={{ marginLeft: '8px' }} />
                </a>
              </div>
            </div>
          </section>
        </>
      )}

      {/* Footer Block */}
      <Footer />

      {/* Slide-out Sidebar Cart Drawer */}
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onCheckout={handleCheckout}
      />

      {/* Toast Alert Popups Container */}
      <div className="toast-container">
        {toasts.map(toast => (
          <div key={toast.id} className="toast show">
            <Bell size={16} style={{ color: 'var(--color-accent)' }} />
            <span>{toast.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
