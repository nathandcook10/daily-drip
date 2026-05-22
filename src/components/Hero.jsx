import React from 'react';

export default function Hero() {
  return (
    <section className="hero">
      <div className="container hero-split">
        {/* Left Column: Bold Copy & CTA */}
        <div className="hero-content">
          <span className="hero-badge">
            Daily Drop 004
          </span>
          
          <h1 className="hero-title">Wear Your Story</h1>
          
          <p className="hero-desc">
            Express individuality through evolving designs that capture the essence of our times. Each release is custom designed and produced sustainably.
          </p>
          
          <div className="hero-ctas">
            <a href="#catalog" className="hero-btn">
              Shop Releases
            </a>
          </div>
        </div>

        {/* Right Column: Premium Visual Card (4:3 showcase crop) */}
        <div className="hero-visual">
          <div 
            style={{
              position: 'relative',
              width: '100%',
              aspectRatio: '4 / 3',
              borderRadius: '16px',
              overflow: 'hidden',
              border: '1px solid var(--border-glass)',
              boxShadow: '0 20px 40px rgba(45, 62, 51, 0.05)'
            }}
          >
            <img 
              src="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&q=80&w=700&h=600" 
              alt="Premium Streetwear Lookbook fit" 
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                display: 'block'
              }}
            />
            {/* Subtle brand vignette overlay */}
            <div 
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: 'linear-gradient(0deg, rgba(23, 26, 24, 0.2) 0%, transparent 50%)',
                pointerEvents: 'none'
              }}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
