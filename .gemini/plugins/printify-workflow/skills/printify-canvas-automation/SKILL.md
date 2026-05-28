---
name: printify-canvas-automation
description: >-
  Strictly enforces a granular, step-by-step workflow for creating, upscaling, and synchronizing Printify apparel graphics, flat lays, and Uwear lifestyle shots. Mandatory checkpoints enforce user approval to prevent destructive operations.
---

# Printify & Uwear End-to-End Workflow

## Overview
This skill defines a strict state machine for creating T-shirt graphics, mathematically baking them onto 4500x5100 canvases, pushing them surgically to the Printify API, and generating Uwear lifestyle mockups.

**CRITICAL RULE:** You must NEVER skip an approval checkpoint. You must NEVER assume a source file.

---

## Phase 1: Graphic Creation & Strict Approval
1. **Ideation:** Iterate with the user on a raw design concept (e.g., text logo, photo, etc.).
2. **Review:** Present the raw design iterations to the user.
3. **Revisions:** Iterate until the user explicitly states it is perfect.
4. **APPROVAL CHECKPOINT (USER):** You must stop and wait for the user to explicitly approve the final raw graphic.
5. **Artifact Hygiene (CRITICAL):** Immediately delete all old/failed versions from the folder. The ONLY files that survive are the approved ones (e.g., `design_for_dark_shirts.png`). *Never accidentally use a v1 or scrape an old graphic from an API.*
6. **Placement Gathering:** Explicitly ask the user: "What is the exact placement and scale for this graphic? (e.g., left chest, full back, exact padding)."

---

## Phase 2: Local Upscaling & Canvas Baking (The "Factory")
7. **Source of Truth:** Pull **ONLY** the approved local files from Phase 1. *NEVER scrape the Printify API to source a graphic.*
8. **Mandatory Upscale:** Mathematically upscale the graphic to the highest resolution (Lanczos + Unsharp filter) so the smallest dimension hits at least 4000px if needed.
9. **Color & Ink Mapping:** Generate the required ink variants (e.g., white ink vs. black ink). *If the graphic is a photograph, STRICTLY BYPASS any text-color inversion rules.*
10. **Baking to Canvas:** Paste the upscaled graphics onto transparent `4500x5100` master canvases at the exact coordinates requested.
11. **Naming Standard:** Name the canvases with strict placement prefixes:
    - `front_design_for_light_shirts.png`
    - `front_design_for_dark_shirts.png`
    - `back_design_for_light_shirts.png`
    - `back_design_for_dark_shirts.png`
12. **BAKE REVIEW CHECKPOINT (USER):** Present the final baked canvases to the user to verify the scale and placement BEFORE touching the Printify API. Stop and wait for approval.

---

## Phase 3: Surgical Printify API Synchronization
13. **Image Upload:** Upload the approved 4500x5100 canvases to Printify's media library and retrieve their new Image IDs.
14. **State Retrieval (CRITICAL):** Fetch the *current* state of the Printify product. Pull down the `blueprint_id`, `variants` (including prices and SKUs), and specific `mockups` selections.
15. **Surgical Payload Construction:** Instead of creating a brand new payload from scratch, precisely inject the new Image IDs into the `print_areas` of the existing JSON data. *This guarantees prices, variants, and specific flat lay mockup choices are never overwritten or reset.* Map the correct `_light_shirts` image to the light variants, and `_dark_shirts` image to the dark variants.
16. **API Sync:** Send the surgical payload back to Printify via `PUT /v1/.../products/{id}.json`.
17. **Propagation Wait:** Wait exactly 60 seconds to allow Printify's internal servers to render and propagate the new flat lay mockups across their CDN.

---

## Phase 4: Flat Lay Review & Uwear Lifestyle Generation
18. **Fetch Mockups:** Download the newly generated Printify flat lays.
19. **FINANCIAL CHECKPOINT (USER):** Present the flat lays to the user and explicitly ask: *"Are these 100% correct? If yes, I will trigger Uwear. This will consume your API credits."* Stop and wait for explicit financial approval.
20. **Uwear Execution:** Upon explicit approval, trigger the Uwear API to generate the premium lifestyle models (Streetwear, Layered, etc.).
21. **Safe Polling:** Monitor the Uwear API with strict timeouts (e.g. 15-second request timeouts, 30 max attempts).
22. **Asset Save:** Download the final high-res lifestyle shots into the codebase folder (e.g., `public/assets/models/`).

---

## Phase 5: Website Go-Live
23. **Code Update:** Update the website code (PDP HTML/React components) to point to the new Uwear assets and flat lays.
24. **Final Verification:** Verify the UI layout is correct and present the final result to the user.
