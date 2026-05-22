# Prompt 02: Meta Ads Campaign Planner & CLI Command Builder

Use this prompt when you are launching a paid social media marketing campaign for a new drop. It guides the AI to write high-converting ad copy in our distinct streetwear voice, research highly targeted Facebook/Instagram interests, and output the exact command-line script to run our automated python ads manager.

---

## 🔧 1. Parameters Checklist
Before copying the template, fill out these four key values. They are highlighted in **red emoji markers** inside the template below so you can locate them instantly.

*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [PRODUCT_NAME] 🔴</span>: The name of your new streetwear item (e.g., *Sage Earth Block Tee*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [RETAIL_PRICE] 🔴</span>: Price of the product in USD (e.g., *34.00*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [CORE_CONCEPT_OR_THEME] 🔴</span>: The visual vibe and meaning behind the design (e.g., *sustainable growth, minimal organic aesthetics*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [URL_TO_ARTWORK] 🔴</span>: The public URL of the flat transparent PNG design artwork (e.g., a link to your raw GitHub file).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [MOCKUP_FILE_NAME] 🔴</span>: The file name of your ad mockup saved inside the `Core Art` folder (e.g., *sage_tee_mockup*).
*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [DAILY_BUDGET] 🔴</span>: The daily budget in USD (default is *10.00*).

---

## 📋 2. Copy-Paste Prompt Template

```text
Hi assistant! I need to plan and launch a targeted Meta Ads campaign (Facebook & Instagram) for our new Daily Drip streetwear drop called "🔴 [PRODUCT_NAME] 🔴".

First, please read our Meta Ads guide to understand how our scripts are wired:
- docs/conversations/002_meta_ads_setup.md
- scripts/daily_drip_manager.py

Here are the details for the new product:
- Title: 🔴 [PRODUCT_NAME] 🔴
- Price: $🔴 [RETAIL_PRICE] 🔴
- Core Concept: 🔴 [CORE_CONCEPT_OR_THEME] 🔴
- Target Audience Focus: Skateboard culture, minimalist fashion, organic apparel.

Please perform the following tasks:
1. DEVELOP HIGH-CONVERGENCE AD COPY:
   - Create 3 copy variations (Primary Ad Copy, Headline, and Description) optimized for Facebook/Instagram feeds.
   - Maintain the "Daily Drip" voice: minimal, organic, street-literate, slightly exclusive ("vaulted release").
   - Highlight our sustainable zero-waste printing model ("organic direct-to-garment", "once vaulted, never printed again").

2. COMPILE TARGET INTERESTS:
   - Provide a list of 5-10 specific, high-intent interests to target in Ads Manager that align with this specific design (e.g. "Minimalist Fashion", "Aimé Leon Dore", "Skateboard culture").
   - Group them into a comma-separated format for our script command line.

3. STRUCTURE THE CAMPAIGN BUDGET:
   - Suggest a daily starting budget ($🔴 [DAILY_BUDGET] 🔴) and a campaign schedule.
   
4. GENERATE THE PYTHON CLI AUTOMATION COMMAND:
   - Generate the exact, copy-paste terminal command to launch this product and paused adset via `scripts/daily_drip_manager.py create-drip`.
   - Map all variables precisely:
     --title "🔴 [PRODUCT_NAME] 🔴"
     --desc "[Ad Copy Variation 1]"
     --design-url "🔴 [URL_TO_ARTWORK] 🔴"
     --mockup-path "/Users/nathan/Daily Drip/Core Art/🔴 [MOCKUP_FILE_NAME] 🔴.png"
     --price 🔴 [RETAIL_PRICE] 🔴
     --budget 🔴 [DAILY_BUDGET] 🔴
     --interests "[Comma-separated, interest, list]"

Ready! Let's draft this campaign and review the copy and CLI parameters.
```

---

## 💡 Pro-Tips for Nathan & Alby:
- Running this prompt will output a complete shell command. For safety, the Python script publishes the campaign and adset in a **paused** state. 
- You can copy-paste the output command into your terminal, run it, and then go to [Meta Ads Manager](https://adsmanager.facebook.com/) to visually inspect the mockup and text before flipping the toggle to active.
