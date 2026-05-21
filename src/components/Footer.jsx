import React from 'react';
import { Instagram, Youtube, Twitter } from 'lucide-react';

export default function Footer() {
  const handleNewsletterSubmit = (e) => {
    e.preventDefault();
    alert('💧 Subscribed! Welcome to the Stream.');
    e.target.reset();
  };

  return (
    <footer className="footer" id="contact">
      <div className="container footer-grid">
        {/* Brand & Info Block */}
        <div className="footer-brand">
          <img className="footer-logo" src="/assets/logo-long-white.png" alt="Daily Drip Logo" />
          <p className="footer-tagline">
            Wear the Moment. A programmatically designed, daily-shifting aesthetic catalog of wearable narratives.
          </p>
          <div className="social-links">
            <a href="#" className="social-link" aria-label="Instagram"><Instagram size={16} /></a>
            <a href="#" className="social-link" aria-label="YouTube"><Youtube size={16} /></a>
            <a href="#" className="social-link" aria-label="Twitter"><Twitter size={16} /></a>
          </div>
        </div>
        
        {/* Navigation Links */}
        <div className="footer-nav">
          <h4 className="footer-heading">DIRECTORY</h4>
          <div className="footer-links">
            <a href="#" className="footer-link">Home</a>
            <a href="#catalog" className="footer-link">Daily Releases</a>
            <a href="#story" className="footer-link">Our Story</a>
            <a href="#" className="footer-link">Refund Policy</a>
            <a href="#" className="footer-link">Terms of Service</a>
          </div>
        </div>
        
        {/* Newsletter Block */}
        <div className="footer-newsletter">
          <h4 className="footer-heading">JOIN THE STREAM</h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--color-text-secondary)', lineHeight: 1.5, fontWeight: 300 }}>
            Never miss a meaningful drop. Subscribe to get early access previews of upcoming releases.
          </p>
          <form className="newsletter-form" onSubmit={handleNewsletterSubmit}>
            <input 
              type="email" 
              className="newsletter-input" 
              placeholder="ENTER YOUR EMAIL" 
              aria-label="Email for Newsletter" 
              required 
            />
            <button type="submit" className="btn-newsletter">JOIN</button>
          </form>
        </div>
      </div>
      
      {/* Footer Bottom Legal */}
      <div className="container footer-bottom">
        <p>&copy; 2026 The Daily Drip. Powered programmatically by AI & Printify.</p>
        <p>Secure SSL checkout processed locally with Stripe integrations.</p>
      </div>
    </footer>
  );
}
