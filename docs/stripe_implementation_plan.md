# Stripe Integration Implementation Plan

Integrate Stripe Checkout into the **Daily Drip** React + Vite web application to process secure, real-time customer payments. We will build a lightweight Express backend to create Stripe Checkout sessions, configure Vite to proxy API requests during development, and adapt the frontend Cart Drawer to redirect to the secure Stripe Checkout page.

---

## User Review Required

> [!IMPORTANT]
> **Stripe Credentials Required:** To test or use the Stripe checkout in a real environment, you will need to add your Stripe API credentials to a `.env` file in the project root. We will provide a `.env.example` template. For local testing, you should use Stripe's test keys (`sk_test_...`).
> 
> **Printify/Production Routing:** Currently, this integration handles Stripe payment collection. In a production pipeline, successful Stripe checkout webhooks would be registered to automatically route orders to Printify. We will implement standard placeholders and comments for where to hook up Printify fulfillment in the future.

---

## Open Questions

None at this time. The architecture is straightforward and utilizes the existing React application structure.

---

## Proposed Changes

### Backend Component (Express + Stripe)

We will introduce a lightweight Express backend at the root of the project to securely handle Stripe Checkout session creation.

#### [NEW] [server.js](file:///Users/nathan/Daily%20Drip/server.js)
- A Node.js Express server configured to run on port `5000` (or `PORT` env variable).
- Integrates the official `stripe` Node SDK.
- Exposes a `POST /api/create-checkout-session` endpoint that receives cart items, securely maps them to backend price definitions (to prevent price-tampering), and returns a Stripe Session URL.
- Serves the built static files (`/dist`) in a production environment.

#### [NEW] [.env.example](file:///Users/nathan/Daily%20Drip/.env.example)
- Environment variable template file.
- Contains placeholders for:
  - `STRIPE_SECRET_KEY` (Stripe Test/Live secret API key)
  - `PORT` (Backend server port, default `5000`)

---

### Frontend Component (React + Vite)

We will modify the frontend configuration, main application state, and Cart Drawer to fetch the Stripe Checkout session and handle success/cancel events.

#### [MODIFY] [vite.config.js](file:///Users/nathan/Daily%20Drip/vite.config.js)
- Configure Vite's dev server proxy to forward `/api` requests to `http://localhost:5000` in development.

#### [MODIFY] [package.json](file:///Users/nathan/Daily%20Drip/package.json)
- Add backend dependency `stripe`, `express`, `cors`, `dotenv`.
- Add dev dependency `concurrently` (to run the React app and Node backend concurrently in development).
- Add scripts:
  - `"server"`: `node server.js`
  - `"dev"`: `concurrently "vite" "node server.js"`

#### [MODIFY] [App.jsx](file:///Users/nathan/Daily%20Drip/src/App.jsx)
- **Stripe Checkout Hook:** Modify `handleCheckout` to be an async function. It will make a `POST` request to `/api/create-checkout-session` sending only the product IDs, sizes, and quantities.
- **Redirection:** Dynamically redirect the browser window to the Stripe-hosted checkout page via `window.location.href = session.url`.
- **Query Parameter Detection:** Add a `useEffect` hook to scan the URL on load for `?success=true` (successful transaction) or `?canceled=true` (cancelled/returned).
  - On `success=true`: Clear the local cart state, trigger a premium success notification toast, and clean up browser history query params.
  - On `canceled=true`: Trigger a canceled/returned notification toast and clean up browser history query params.

#### [MODIFY] [CartDrawer.jsx](file:///Users/nathan/Daily%20Drip/src/components/CartDrawer.jsx)
- Modify checkout button logic to correctly execute the async `onCheckout` function and handle the loading spinner during the Stripe network handshake.

---

## Verification Plan

### Automated & Integration Tests
1. **Dependency Verification:** Install dependencies and run linting to ensure no TypeScript/React syntax issues.
2. **Server Launch:** Run `npm run server` to confirm the Express backend starts up correctly on port 5000.
3. **Endpoint Validation:** Perform a curl POST request to `/api/create-checkout-session` with a mock cart payload and verify that Stripe returns a valid checkout session URL.

### Manual Verification
1. **Dev Server Run:** Launch development environment using `npm run dev`. Confirm both Vite and the Express server run concurrently.
2. **Stripe Redirection:** Fill the cart in the browser, click "Secure Checkout", and verify that the user is immediately redirected to a secure Stripe Checkout page (`checkout.stripe.com`).
3. **Success Redirection:** Simulating a successful purchase in Stripe test mode, verify that the redirection returns to `http://localhost:5173/?success=true`, the cart is emptied, and a gorgeous premium success toast displays.
4. **Canceled Redirection:** Click the back arrow in Stripe Checkout to return, verify redirection to `http://localhost:5173/?canceled=true`, the cart remains preserved, and a checkout canceled toast displays.
