# Stripe Checkout Integration Task List

A structured checklist of planned tasks for the Stripe Checkout payment gateway integration. These tasks will remain pending until you or Albie are ready to proceed with execution.

---

## 🛠️ Backend Setup (Express + Stripe)
- [ ] Initialize backend dependencies
  - [ ] Install `express`, `stripe`, `cors`, and `dotenv`
  - [ ] Install devDependency `concurrently` (to run Vite and Express concurrently in development)
- [ ] Create `server.js` backend server
  - [ ] Configure environment variable loading and Stripe SDK setup
  - [ ] Implement secure `POST /api/create-checkout-session` mapping cart items to backend price definitions
  - [ ] Configure Express to serve production static built files (`/dist`)
- [ ] Create `.env.example` configuration template

---

## 💻 Frontend Configuration
- [ ] Configure API Proxy in `vite.config.js` for seamless development proxying
- [ ] Update npm scripts in `package.json`
  - [ ] Add `"server": "node server.js"`
  - [ ] Add `"dev": "concurrently \"vite\" \"node server.js\""`

---

## 💧 Stripe Checkout Integration
- [ ] Adapt main `App.jsx`
  - [ ] Make `handleCheckout` async and fetch from `/api/create-checkout-session`
  - [ ] Implement redirection to the Stripe Checkout Session URL
  - [ ] Add `useEffect` hook to read query parameters (`?success=true` / `?canceled=true`)
  - [ ] Implement cart-clearing and premium notification toasts for success/cancel events
- [ ] Adapt `CartDrawer.jsx`
  - [ ] Integrate async checkout and handle loading spinner state on "Secure Checkout" button click

---

## 🧪 Verification & Testing
- [ ] Verify local Express server starts successfully
- [ ] Confirm proxying routes correctly from port `5173` to `5000`
- [ ] Test Stripe sandbox checkout flow
  - [ ] Redirection to `checkout.stripe.com`
  - [ ] Successful payment redirect (`?success=true`) clearing cart and displaying toast
  - [ ] Cancel payment redirect (`?canceled=true`) preserving cart and displaying cancel toast
