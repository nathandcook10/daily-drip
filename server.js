import express from 'express';
import Stripe from 'stripe';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '');
const app = express();

app.use(cors());
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// --- Secure Backend Product Price Definitions (Prevents Price Tampering) ---
const PRODUCT_PRICES = {
  "prod_robot_012": 2999, // in cents ($29.99)
  "prod_monkey_011": 2999,
  "prod_peace_010": 2999,
  "prod_sage_009": 2999,
  "prod_binary_008": 3499,
  "prod_vapor_007": 2999,
  "prod_neural_006": 2999,
  "prod_pixel_005": 3299
};

const PRODUCT_NAMES = {
  "prod_robot_012": "Outperformed by a ROBOT. Again.",
  "prod_monkey_011": "Punch the Monkey",
  "prod_peace_010": "Peace Sign and Hands T-Shirt",
  "prod_sage_009": "Sage Archives Graphic Tee",
  "prod_binary_008": "Binary Genesis",
  "prod_vapor_007": "Vaporwave Paradox",
  "prod_neural_006": "Neural Echoes",
  "prod_pixel_005": "Pixelated Soul"
};

// --- Stripe Checkout Session Creation Endpoint ---
app.post('/api/create-checkout-session', async (req, res) => {
  try {
    const { items } = req.body; // Expects array of { id, title, size, quantity }

    if (!items || items.length === 0) {
      return res.status(400).json({ error: "Cart items cannot be empty." });
    }

    // Build standard line items securely mapping ID to correct price
    const lineItems = items.map(item => {
      const priceInCents = PRODUCT_PRICES[item.id] || 2999;
      const productName = PRODUCT_NAMES[item.id] || item.title;

      return {
        price_data: {
          currency: 'usd',
          product_data: {
            name: `${productName} (Size: ${item.size})`,
            metadata: {
              productId: item.id,
              size: item.size
            }
          },
          unit_amount: priceInCents,
        },
        quantity: item.quantity,
      };
    });

    // Create the secure Stripe checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: lineItems,
      mode: 'payment',
      success_url: `${req.headers.origin}/?success=true`,
      cancel_url: `${req.headers.origin}/?canceled=true`,
    });

    res.json({ url: session.url });
  } catch (error) {
    console.error('💧 [Daily Drip Server] Error creating checkout session:', error);
    res.status(500).json({ error: error.message });
  }
});

// --- Production Static Assets Serving ---
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'dist')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
  });
} else {
  // Simple welcome endpoint for dev health checks
  app.get('/', (req, res) => {
    res.send('💧 Daily Drip Express API Server running...');
  });
}

const PORT = process.env.PORT || 5005;
app.listen(PORT, () => {
  console.log(`💧 [Daily Drip Server] Server running on port ${PORT}`);
});
