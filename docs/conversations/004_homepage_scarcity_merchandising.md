# 💧 Conversation Log 004: Homepage Scarcity Merchandising & Capsule Navigation

**Date:** May 23, 2026  
**Participants:** Alby, Nathan, Antigravity AI Pair Programmer

---

## 1. Context & Objective
Alby and Nathan reviewed the storefront merchandising layout to determine the best way to utilize the homepage's finite real estate. Since the majority of storefront traffic lands directly on Product Detail Pages (PDPs) from social media and paid meta campaigns, the homepage's primary job is to establish the **brand vibe (Organic Sage Streetwear)** and create **immediate urgency / FOMO** for returning and cold visitors.

---

## 2. Iterative Design Process & Feedback Loops

During our pair-programming session, we went through a comprehensive, visual design exploration in Chrome:

### Step 1: Strategic Merchandising Proposal
* **The Idea**: Introduce category tabs to filter design capsules, keep the active drips grid compact, and display a "Recently Vaulted" grid showing sold-out designs in grayscale with a diagonal strike-through to prove drop scarcity immediately. We also proposed a technical hero banner with spec sheets.
* **Review**: Alby and Nathan loved the lower sections (Categories, Active Grid, and Vault Archives) but wanted to highlight the physical garment visually in the hero section at the top.

### Step 2: Asymmetric Split Hero
* **The Idea**: Redesigned the top hero block into a 50/50 split, showing the model lookbook image of the "Outperformed by a ROBOT" design on the right with a diagnostics overlay card, and detailed descriptions on the left.
* **Review**: They liked having the model image but requested simplifying the left text block drastically and zooming in on the t-shirt so it was the absolute visual center.

### Step 3: Zoomed-in Central Showcase
* **The Idea**: Overhauled the top hero to a centered lookbook frame displaying the model photo.
* **Review Loop**: 
  1. *First Attempt*: Zoomed in deeply (195%) on the model's torso. It was over-cropped, making the t-shirt outline hard to distinguish.
  2. *Second Attempt*: Zoomed out to a balanced `135%` scale centered vertically at `15%`, framing the neckline, sleeves, and graphic text, and taller framing card dimensions (`480px x 520px`) for a complete, un-cropped fit view.
  3. *Decision*: After seeing the zoomed-in lookbook option, Alby and Nathan decided to **omit the top hero section modifications entirely** to preserve their existing `<Hero />` styling, but **fully implement the lower sections** (Capsules, Active Drops, recently vaulted grids) which they agreed were perfect.

---

## 3. Final Merchandising Strategy Implemented

We successfully integrated the selected sections directly into the React storefront:

```
├── Home Hero (Original Clean Intro preserved)
├── Capsule Navigation Tabs (ALL, TECH, RETRO filters)
├── Active Drops Grid (Outperformed by a ROBOT, Punch the Monkey, Peace Sign)
└── Recently Vaulted Grid (Sage Archives, Binary Genesis, Vaporwave Paradox - SOLD OUT in Grayscale)
```

### Key Component Technical Implementations:

1. **`src/styles/global.css`**: Added styling for `.product-card.vaulted` to apply a grayscale filter (`100%`), reduced opacity (`0.65`), a dashed card border, and a premium diagonal linear-gradient strike-through overlay. Added capsule tab selector chip styling.
2. **`src/components/ProductCard.jsx`**: Supported dynamic `isVaulted` checking. For vaulted drops:
   * Disables the add-to-cart button and sets label to `VAULTED / SOLD OUT`.
   * Hides the size overlays on hover.
   * Replaces the size swatches picker with a red monospaced notification: `DROP CLOSED - This release has reached printing limits and is vaulted.`
3. **`src/components/ProductList.jsx`**:
   * Assigned category metadata (`TECH` or `RETRO`) to all designs.
   * Placed interactive tab selector chips (`All Drops`, `[ 01 / TECH & DATA ]`, `[ 02 / RETRO NOSTALGIA ]`) at the top of the catalog.
   * Rendered the filtered Active Drops grid.
   * Implemented the **Recently Vaulted** teaser grid directly underneath, displaying 3 sold-out items to generate immediate FOMO.
   * Added a unified `EXPLORE COMPLETE VAULT ARCHIVE` CTA button leading to the history catalog.

---

*Log co-authored by Alby and Antigravity AI — May 23, 2026*
