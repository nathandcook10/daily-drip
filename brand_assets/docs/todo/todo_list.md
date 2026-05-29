# 💧 Daily Drip - Shared To-Do List

This document is the living, single source of truth for the **Daily Drip** codebase tasks, enhancements, and features. It serves as the primary coordination board for **Nathan**, **Alby**, and their **Antigravity** AI pair programmers.

---

## 🤖 Guide for Antigravity AI Agents
When pair-programming, you **must** keep this document up to date:
1. **Always read this file first** when starting a new session or receiving instructions about what to build.
2. **Mark tasks dynamically** as you work on them:
   - `[ ]` for Unstarted/Backlog
   - `[/]` for In Progress (custom notation)
   - `[x]` for Completed
3. **Link references:** When starting or completing a task, append a markdown link to the relevant conversation log under `docs/conversations/` so context is never lost.
4. **Co-authoring:** Do not overwrite other active tasks; append new items with priority labels and author names.

---

## ⚡ Active Feature Backlog

### 💳 Stripe Checkout Integration
* **Priority:** Critical
* **Context:** [Stripe Implementation Plan](file:///Users/nathan/Daily%20Drip/docs/stripe_implementation_plan.md) | [Stripe Tasks Checklist](file:///Users/nathan/Daily%20Drip/docs/stripe_tasks.md) | [Conversation 002 Log](file:///Users/nathan/Daily%20Drip/docs/conversations/002_stripe_integration.md)
* [ ] Setup Express backend structure with Stripe Node SDK integration `[Added: May 22, 2026 by Nathan]`
* [ ] Configure Vite proxy rules to route local `/api` checkout requests seamlessly
* [ ] Replace mock frontend checkout with actual secure redirect flow
* [ ] Configure Stripe success/cancel webhook or callback page handlers
* [ ] Test locally with Stripe CLI and verify live-event fulfillment trigger to Printify

---

## 🧼 Codebase Cleanup & Asset Protection (Clean Sweep)
* **Priority:** High
* **Context:** [Deletion & Clean Sweep Plan](file:///Users/nathan/.gemini/antigravity/brain/da46cf20-1221-482d-8784-38c037702413/implementation_plan.md) | [Audit Log](file:///Users/nathan/Daily%20Drip/docs/conversations/003_codebase_cleanup_audit.md)

### 1. Legacy Script Deletions
* [x] **Delete Broken/Legacy Pipeline Scripts:** Remove `scripts/run_pipeline.py` and `scripts/tshirt_pipeline.py` to prevent confusion with the root modular pipeline. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Delete Legacy Ads & Product Managers:** Remove `scripts/daily_drip_manager.py` along with helper clients `scripts/printify_api.py` and `scripts/meta_ads_api.py`. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Delete Obsolete Helper Scripts:** Clean sweep files `scripts/notify_alby.py`, `scripts/test_fetch.py`, `scripts/copy_assets.py`, `scripts/organize_assets.py`, `scripts/organize_new_assets.py`, `scripts/check_dimensions.py`, `scripts/download_active_flats.py`, and `scripts/extract_prints.py`. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Delete Lookbook & PDF Tools:** Clean sweep legacy compilers `scripts/generate_pdf.py`, `scripts/compile_lookbook.py`, `scripts/generate_pdps.py`, `scripts/update_all_pdps.py`, `scripts/generate_peace_proof.py`, and `scripts/close.sh`. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Move Root Experimental Clutter:** Relocate `nathan-vegas-app/` directory and `nathan_vegas_trip.html` to a safe home folder outside the project. `[Completed: May 27, 2026 | Requested by Nathan]`

### 2. Version Control Asset Protection
* [x] **Ignore Pipeline Staging Directory:** Add `pipeline_staging/` to `.gitignore` to prevent 17MB+ baked canvas files from bloating Git. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Ignore VTO Base and Output Directories:** Add `base_photos/` and `final_pdp_assets/` to `.gitignore` to protect the repo from massive local Hugging Face image outputs. `[Completed: May 27, 2026 | Requested by Nathan]`
* [x] **Ignore Root Temporary PNGs:** Add wildcard rules `*.png` (except inside `public/assets/` or `src/assets/`) to block local test proof images from being checked in. `[Completed: May 27, 2026 | Requested by Nathan]`

---

## 🧹 Codebase & Storefront Optimization

### 1. Code Refactoring & Optimization
* [ ] **Consolidate Product Data Arrays:** Refactor duplicate product lists in `ProductList.jsx` and `ArchiveList.jsx` into a single shared file `src/data/products.js` to ensure single-source reliability. `[Priority: High | Added: May 22, 2026 by Nathan]`
* [ ] **Dynamic Design Counter:** Replace the hardcoded `8 TOTAL DESIGNS` text on the Shop All card in `ProductList.jsx` with a dynamic `.length` read from the products data array. `[Priority: Low | Added: May 22, 2026 by Nathan]`
* [ ] **Migrate PDP_MAP out of Presentation:** Move the `PDP_MAP` object from `ProductCard.jsx` into the central shared product data file. `[Priority: Medium | Added: May 22, 2026 by Nathan]`
* [ ] **Enhance Contact Nav Routing:** Improve the dynamic scroll behavior in `Header.jsx` when transitioning from the Archive to Home view to click 'Contact' so it scrolls reliably without racing. `[Priority: Medium | Added: May 22, 2026 by Nathan]`

### 2. User Experience Polish
* [ ] **Eliminate Browser-Blocking Alerts:** Convert the raw checkout `alert()` in `App.jsx` and newsletter `alert()` in `Footer.jsx` to utilize the modern, smooth React `showToast()` message system. `[Priority: High | Added: May 22, 2026 by Nathan]`
* [ ] **Replace External Hero Media:** Swap the placeholder Unsplash hero image in `Hero.jsx` with a premium brand asset lookbook photography file. `[Priority: High | Added: May 22, 2026 by Nathan]`
* [ ] **Define Placeholder Tag Style:** Add a matching CSS rule in `global.css` for the `.placeholder-tag` class referenced in `ProductCard.jsx` for missing flat images. `[Priority: Low | Added: May 22, 2026 by Nathan]`

### 3. High-Fidelity Asset Sync & Optimization
* [ ] **Audit Low-Res Product Flats:** Investigate and replace `flat_monkey_front/back.png` and `flat_peace_front/back.png` in `/public/assets/flats/` which are currently low-res raw placeholders (10KB–24KB) with high-res equivalents. `[Priority: High | Added: May 22, 2026 by Nathan]`
* [ ] **Brand Asset Compression:** Optimize and compress large PNG logo files (`logo-icon.png`, `logo-daily.png`) and the Story section background image (`design-element.png` - 1.4MB) into modern, lightweight WebP formats. `[Priority: Medium | Added: May 22, 2026 by Nathan]`

---

## 💡 Future Ideas & Enhancements
* [ ] Implement persistent local storage caching for past product drops to speed up archive rendering.
* [ ] Add a dark mode toggle matching premium glassmorphism styling tokens.

---

## ✅ Completed Tasks
* [x] Initialize Git Repository and push to private remote `[Completed: May 20, 2026 | Log: 001_project_setup.md]`
* [x] Draft Stripe payment architecture plans `[Completed: May 22, 2026 | Log: 002_stripe_integration.md]`
* [x] Comprehensive codebase audit scan `[Completed: May 22, 2026 | Log: 003_codebase_cleanup_audit.md]`
