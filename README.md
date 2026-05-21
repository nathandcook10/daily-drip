# 💧 The Daily Drip Storefront & Automation Suite

Welcome to **The Daily Drip** streetwear catalog project. This workspace consists of two integrated components:
1. **React + Vite Storefront**: Rebuilt from Shopify to feature a highly aesthetic, clean, earth-tone minimal streetwear layout matching our high-end branding (whites, organic sage greens, forest greens, and deep charcoal).
2. **Python CLI Suite**: Handles automated unisex t-shirt creation via the **Printify API** and programmatically publishes Meta ad campaigns via the **Meta Marketing API**.

---

## 🤝 3-Step Access Guide for Alby

If you want your collaborator **Alby** to jump in, clone this codebase, and manage products, here is exactly what needs to be done:

### Step 1: Nathan Pushes the Code to a Private GitHub Repository
Run these commands in your local terminal to link this folder to your GitHub:
```bash
# Initialize git and stage changes
git init
git add .
git commit -m "feat: initial storefront release with sage earth-tone layout"

# Create a repository named "daily-drip" on github.com, then run:
git remote add origin https://github.com/nathandcook10/daily-drip.git
git branch -M main
git push -u origin main
```
*Note: Go to repository **Settings** -> **Collaborators** on GitHub, click **Add People**, and invite Alby.*

### Step 2: Alby Clones the Code & Runs the Dev Storefront
Once invited, Alby can run these commands on his machine to launch the interactive catalog:
```bash
# Clone the private repository
git clone https://github.com/nathandcook10/daily-drip.git
cd daily-drip

# Install dependencies and start the local development server
npm install
npm run dev
```
*The local storefront will now be running on Alby's computer at `http://localhost:5173`!*

### Step 3: Alby Manages Visual Designs & Drops
Alby can easily sync layouts and assets:
* **Visual Mockups**: Drop design flat-layups or model mockups into `public/assets/`.
* **Product Catalog**: Add or edit releases in `src/components/ProductList.jsx` to live-update the storefront.
* **Auto-Publish to Shopify/Printify**: Setup credentials in `scripts/.env` and drop artwork images into the local machine, then run:
  ```bash
  python3 scripts/daily_drip_manager.py --image "your_design.png" --title "Design Name" --price 29.99
  ```

---

## ⚡ Development & Launch Commands

### Storefront Dev Server
Starts the React web application with Hot Module Replacement (HMR).
```bash
npm run dev
```

### Storefront Production Build
Compiles static HTML/JS/CSS assets to the `/dist` directory for fast deployment.
```bash
npm run build
```

---

## 🤖 Python Automation Suite (`/scripts`)

The daily workflow uses the local script managers in the `/scripts` directory to automate production:
* `daily_drip_manager.py`: Connects APIs into a unified CLI drop tool.
* `printify_api.py`: Integrates Unisex Bella+Canvas 3001 product building, mockup uploads, and fulfillment routing.
* `meta_ads_api.py`: Publishes adsets, sets pixel tracking, and schedules targeted campaigns.

To configure, copy `.env.example` to `.env` and fill out your tokens:
```bash
cp scripts/.env.example scripts/.env
```
