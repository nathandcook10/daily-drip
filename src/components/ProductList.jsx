import React from 'react';
import ProductCard from './ProductCard';

const PRODUCTS = [
  {
    id: "prod_robot_012",
    title: "Outperformed by a ROBOT. Again.",
    price: 29.99,
    badge: "TODAY'S DRIP #012",
    description: "A bold streetwear graphic celebrating the inevitable takeover of our digital counterparts. Outperformed, but stylish.",
    imageFront: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/9226356700390701280_2048.jpg?v=1774737225&width=600",
    imageBack: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/14890164672711313126_2048.jpg?v=1774737227&width=600",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_monkey_011",
    title: "Punch the Monkey",
    price: 29.99,
    badge: "ARCHIVE #011",
    description: "Classic vintage vibes meets modern street expression. A playful take on cultural nostalgia.",
    imageFront: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/14427770582284497701_2048.jpg?v=1774724955&width=600",
    imageBack: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/505426938446300089_2048.jpg?v=1774724956&width=600",
    sizes: ["S", "M", "L", "XL"]
  },
  {
    id: "prod_peace_010",
    title: "Peace Sign and Hands T-Shirt",
    price: 29.99,
    badge: "ARCHIVE #010",
    description: "Iconic streetwear symbol of peace, connection, and visual expression. An elegant dark-mode fit.",
    imageFront: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/8514859190100196355_2048.jpg?v=1775351979&width=600",
    imageBack: "https://ivwgiw-k5.myshopify.com/cdn/shop/files/8611523600852697158_2048.jpg?v=1775351981&width=600",
    sizes: ["S", "M", "L", "XL"]
  }
];

export default function ProductList({ onAddToCart }) {
  return (
    <section className="catalog" id="catalog">
      <div className="container">
        <div className="section-header">
          <div>
            <h2 class="section-title">ACTIVE <span>DRIPS</span></h2>
            <p className="section-subtitle" style={{ marginTop: '1rem' }}>
              A fresh visual release. Once sold out, these designs are vaulted and never printed again.
            </p>
          </div>
          <div className="section-subtitle">
            All printings are produced sustainably using direct-to-garment organic cotton blanks by Printify.
          </div>
        </div>
        
        <div className="product-grid">
          {PRODUCTS.map(product => (
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
