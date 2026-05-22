import React, { useState, useEffect } from 'react';
import { ShoppingBag, User, Menu, X } from 'lucide-react';

export default function Header({ cartCount, onCartOpen, view, setView }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('Home');

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

  // Sync tab highlights dynamically with external view swaps
  useEffect(() => {
    if (view === 'archive') {
      setActiveTab('Store');
    } else {
      if (window.scrollY < 100 && activeTab === 'Store') {
        setActiveTab('Home');
      }
    }
  }, [view]);

  const handleLinkClick = (tabName, e) => {
    if (e) e.preventDefault();
    setActiveTab(tabName);
    setIsMenuOpen(false);
    
    if (tabName === 'Home') {
      setView('home');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (tabName === 'Store') {
      setView('archive');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (tabName === 'About') {
      setView('home');
      setTimeout(() => {
        const element = document.getElementById('story');
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 80);
    } else if (tabName === 'Contact') {
      setView('home');
      setTimeout(() => {
        const element = document.getElementById('contact');
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 80);
    }
  };

  return (
    <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="container header-container">
        {/* Branded Logo */}
        <a href="#" className="logo-link" onClick={(e) => handleLinkClick('Home', e)}>
          <img className="logo-img" src="/assets/logo-long.png" alt="Daily Drip Logo" />
        </a>

        {/* Navigation Links (Strictly Home, Store, About, Contact) */}
        <nav className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
          <a 
            href="#" 
            className={`nav-link ${activeTab === 'Home' ? 'active' : ''}`} 
            onClick={(e) => handleLinkClick('Home', e)}
          >
            Home
          </a>
          <a 
            href="#catalog" 
            className={`nav-link ${activeTab === 'Store' ? 'active' : ''}`} 
            onClick={(e) => handleLinkClick('Store', e)}
          >
            Store
          </a>
          <a 
            href="#story" 
            className={`nav-link ${activeTab === 'About' ? 'active' : ''}`} 
            onClick={(e) => handleLinkClick('About', e)}
          >
            About
          </a>
          <a 
            href="#contact" 
            className={`nav-link ${activeTab === 'Contact' ? 'active' : ''}`} 
            onClick={(e) => handleLinkClick('Contact', e)}
          >
            Contact
          </a>
        </nav>

        {/* Action Panel */}
        <div className="nav-actions">
          {/* Account Decorative Btn */}
          <button className="icon-btn" aria-label="Account">
            <User size={18} />
          </button>

          {/* Cart Icon Trigger with Dynamic Spring Pop */}
          <button className="icon-btn" onClick={onCartOpen} aria-label="Open Cart">
            <ShoppingBag size={18} />
            {cartCount > 0 && <span className="cart-count">{cartCount}</span>}
          </button>

          {/* Mobile Hamburg Trigger */}
          <div className="hamburger" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </div>
        </div>
      </div>
    </header>
  );
}

