import React, { useState, useEffect } from 'react';
import { ShoppingBag, User, Menu, X } from 'lucide-react';

export default function Header({ cartCount, onCartOpen }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="container header-container">
        {/* Branded Logo */}
        <a href="#" className="logo-link">
          <img className="logo-img" src="/assets/logo-long.png" alt="Daily Drip Logo" />
        </a>

        {/* Navigation Links */}
        <nav className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
          <a href="#" className="nav-link active" onClick={() => setIsMenuOpen(false)}>Home</a>
          <a href="#catalog" className="nav-link" onClick={() => setIsMenuOpen(false)}>Catalog</a>
          <a href="#story" class="nav-link" onClick={() => setIsMenuOpen(false)}>Our Story</a>
          <a href="#contact" className="nav-link" onClick={() => setIsMenuOpen(false)}>Contact</a>
        </nav>

        {/* Action Panel */}
        <div className="nav-actions">
          {/* Account Decorative Btn */}
          <button className="icon-btn" aria-label="Account">
            <User size={20} />
          </button>

          {/* Cart Icon Trigger */}
          <button className="icon-btn" onClick={onCartOpen} aria-label="Open Cart">
            <ShoppingBag size={20} />
            {cartCount > 0 && <span className="cart-count">{cartCount}</span>}
          </button>

          {/* Mobile Hamburg Trigger */}
          <div className="hamburger" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </div>
        </div>
      </div>
    </header>
  );
}
