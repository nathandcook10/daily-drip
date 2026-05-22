import React from 'react';
import ProductCard from './ProductCard';
import { ArrowLeft } from 'lucide-react';

const ARCHIVED_PRODUCTS = [
  {
    id: "prod_robot_012",
    title: "Outperformed by a ROBOT. Again.",
    price: 29.99,
    badge: "TODAY'S DRIP #012",
    description: "A bold streetwear graphic celebrating the inevitable takeover of our digital counterparts. Outperformed, but stylish.",
    imageFront: "/assets/flats/flat_robot_front.png",
    imageBack: "/assets/flats/flat_robot_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_monkey_011",
    title: "Punch the Monkey",
    price: 29.99,
    badge: "ARCHIVE #011",
    description: "Classic vintage vibes meets modern street expression. A playful take on cultural nostalgia.",
    imageFront: "/assets/flats/flat_monkey_front.png",
    imageBack: "/assets/flats/flat_monkey_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_peace_010",
    title: "Peace Sign and Hands T-Shirt",
    price: 29.99,
    badge: "ARCHIVE #010",
    description: "Iconic streetwear symbol of peace, connection, and visual expression. An elegant dark-mode fit.",
    imageFront: "/assets/flats/flat_peace_front.png",
    imageBack: "/assets/flats/flat_peace_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_sage_009",
    title: "Sage Archives Graphic Tee",
    price: 29.99,
    badge: "VAULT #009",
    description: "A calm organic streetwear catalog design with intelligence. Hand-printed on heavy cotton.",
    imageFront: "/assets/flats/flat_sage_front.png",
    imageBack: "/assets/flats/flat_sage_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_binary_008",
    title: "Binary Genesis",
    price: 34.99,
    badge: "VAULT #008",
    description: "Visualizing the dawn of artificial cognition. A rich tapestry of binary matrices and biological forms.",
    imageFront: "/assets/flats/flat_binary_front.png",
    imageBack: "/assets/flats/flat_binary_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_vapor_007",
    title: "Vaporwave Paradox",
    price: 29.99,
    badge: "VAULT #007",
    description: "Glitch art aesthetic detailing consumerist nostalgia and cyberspace relics in neon slate.",
    imageFront: "/assets/flats/flat_vapor_front.png",
    imageBack: "/assets/flats/flat_vapor_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_neural_006",
    title: "Neural Echoes",
    price: 29.99,
    badge: "VAULT #006",
    description: "Intricate line-work conveying the residual signals of artificial minds. Thought-provoking and minimalist.",
    imageFront: "/assets/flats/flat_neural_front.png",
    imageBack: "/assets/flats/flat_neural_back.png",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_pixel_005",
    title: "Pixelated Soul",
    price: 32.99,
    badge: "VAULT #005",
    description: "Where classic human portraits meet 8-bit digital deconstruction. An ultimate expression of hybrid identity.",
    imageFront: "/assets/flats/flat_pixel_front.png",
    imageBack: "/assets/flats/flat_pixel_back.png",
    sizes: ["S", "M", "L", "XL"]
  }
];

export default function ArchiveList({ onAddToCart, onBack }) {
  // Scroll to top when component mounts
  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  return (
    <section className="catalog" id="archive-catalog" style={{ paddingTop: '120px', minHeight: '80vh' }}>
      <div className="container">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={14} />
          BACK TO HOME
        </button>
        
        <div className="section-header">
          <div>
            <h2 className="section-title">VAULT <span>ARCHIVES</span></h2>
            <p className="section-subtitle" style={{ marginTop: '1rem' }}>
              The complete catalog. Active drops alongside historical, highly sought-after vaulted items.
            </p>
          </div>
          <div className="section-subtitle">
            All printings are produced sustainably using direct-to-garment organic cotton blanks by Printify.
          </div>
        </div>
        
        <div className="product-grid">
          {ARCHIVED_PRODUCTS.map(product => (
            <ProductCard 
              key={product.id}
              product={product}
              onAddToCart={onAddToCart}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
