import React from 'react';
import { ArrowDown } from 'lucide-react';

export default function Hero() {
  return (
    <section className="hero">
      <div className="container hero-grid">
        {/* Left Column: Bold Copy & CTA */}
        <div className="hero-content">
          <span className="badge-daily">💧 Active Daily Collection</span>
          <h1 className="hero-title">Wear Your Story</h1>
          <p className="hero-description">
            Express individuality through evolving designs that capture the essence of our times. Each release is custom designed and produced sustainably.
          </p>
          <div className="hero-ctas">
            <a href="#catalog" className="btn-primary">
              EXPLORE RELEASES
              <ArrowDown size={16} strokeWidth={3} />
            </a>
            <a href="#story" className="btn-secondary">OUR MISSION</a>
          </div>
          <div style={{ marginTop: '2rem' }}>
            <span className="accent-text">meaning over materials...</span>
          </div>
        </div>

        {/* Right Column: Premium Visual Card */}
        <div className="hero-visual">
          <div 
            style={{
              background: '#ffffff',
              border: '1px solid rgba(9, 18, 8, 0.1)',
              borderRadius: '12px',
              padding: '3rem',
              width: '100%',
              maxWidth: '420px',
              height: '360px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              boxShadow: '0 15px 35px rgba(9, 18, 8, 0.08)',
              position: 'relative',
              overflow: 'hidden'
            }}
          >
            <div 
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '4px',
                background: 'linear-gradient(90deg, #2e4a29, #a6b89c)'
              }}
            />
            
            <img 
              src="/assets/logo-icon.png" 
              alt="Daily Drip Icon" 
              style={{ 
                height: '80px', 
                width: 'auto', 
                marginBottom: '2rem',
                animation: 'pulse 3s infinite'
              }} 
            />
            
            <h3 style={{ fontSize: '0.85rem', fontWeight: 900, letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '1rem', color: '#091208' }}>
              THE DAILY DRIP
            </h3>
            
            <p style={{ fontSize: '0.7rem', color: '#3d4a3c', textAlign: 'center', lineHeight: 1.6, maxWidth: '280px', fontWeight: 300 }}>
              Wear your philosophy. Designs rotate dynamically. Zero excess stock. Made just for you.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
