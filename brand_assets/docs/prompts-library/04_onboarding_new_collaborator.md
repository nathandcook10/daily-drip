# Prompt 04: Developer & AI Onboarding Bootstrapper

Use this prompt to onboard a new collaborator (like Alby) and immediately align their AI assistant with the entire "Daily Drip" codebase. It tells their AI assistant exactly where to look, how the codebase is structured, and how to verify that their local Git and environment setups are correct.

---

## 🔧 1. Parameters Checklist
Before copying the template, fill out this one key value. It is highlighted in **red emoji markers** inside the template below so you can locate it instantly.

*   <span style="color: #e11d48; font-weight: bold; font-size: 1.1em;">🔴 [DEVELOPER_NAME] 🔴</span>: The name of the new developer cloning the repository (e.g., *Alby*).

---

## 📋 2. Copy-Paste Prompt Template

```text
Hi assistant! I have just cloned our private streetwear e-commerce repository for "The Daily Drip" to my local machine. My name is 🔴 [DEVELOPER_NAME] 🔴 and I am pair-programming with Nathan to build out this brand. 

I need you to scan this workspace and act as my Senior Technical Co-Pilot.

First, please read and process the following files:
1. README.md (Contains the active onboarding guide and dev commands)
2. .cursorrules / .clinerules (Specifies our strict brand design systems)
3. docs/conversations/001_project_setup.md (Explains our initial repository foundations)
4. docs/conversations/002_meta_ads_setup.md (Explains our automation credentials setup)
5. scripts/daily_drip_manager.py (Our main Python automation runner)

Please perform these onboarding tasks for me:
1. VERIFY SYSTEM STRUCTURE:
   - Walk me through the local directory structure so I know where the storefront code (`src/...`), design assets (`public/...`), and automation scripts (`scripts/...`) reside.
   
2. VERIFY LOCAL GIT & ENVS:
   - Check if our local Git configuration matches Nathan's guidelines.
   - Show me how to copy `scripts/.env.example` to `scripts/.env` and walk me through the key API tokens (Printify & Meta) we need to fill out.
   
3. RUN DIAGNOSTIC CHECKS:
   - Provide the exact shell commands I should run to install our React npm dependencies and launch the local development server.
   - Provide the exact shell command to run our automation suite diagnostic tests (`test` command) to verify that my API keys are configured and communicating correctly.

I am ready to collaborate! Let's get my local environment fully verified.
```

---

## 💡 Pro-Tips for Nathan & Alby:
- When Alby clones the repo, he can open his editor, start a new chat session with his AI, and paste this prompt.
- This saves hours of manual explanation, aligning both developers and both AI agents to the exact same architectural standards instantly.
