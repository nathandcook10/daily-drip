# 💧 Daily Drip

> Welcome to **Daily Drip**! This is a collaborative space for Nathan and Alby.

---

## 🚀 Getting Started

This repository has been initialized with a solid foundation. 

### 🤝 How to Collaborate

Follow these steps to link this local directory to a GitHub repository so you and Alby can work together:

#### 1. Create a GitHub Repository
1. Go to [github.com/new](https://github.com/new) (ensure you are logged in).
2. Name the repository **`daily-drip`** (or another name you prefer).
3. Set the repository visibility to **Private** (or Public if you want anyone to see it).
4. **Leave "Add a README", "Add .gitignore", and "Choose a license" UNCHECKED** (since we've already created them for you).
5. Click **Create repository**.

#### 2. Link This Local Folder to GitHub
Once the repository is created, copy the commands under **"…or push an existing repository from the command line"** on the GitHub setup page. It will look like this:

```bash
# Add the remote URL pointing to your GitHub repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/daily-drip.git

# Push your main branch to GitHub
git push -u origin main
```

#### 3. Share with Alby
1. On your new GitHub repository page, click on the **Settings** tab.
2. Select **Collaborators** from the left-hand menu.
3. Click **Add people** and enter Alby's GitHub username or email address.
4. Once Alby accepts the invite, he can clone the repository to his computer using:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/daily-drip.git
   ```

---

## 🛠️ Project Structure
```
Daily Drip/
├── .gitignore   # Ignores IDE files, OS junk, and dependencies
└── README.md    # You are here!
```

---

## ⚡ Development Workflow

When working together, it's best practice to:
1. **Pull before starting work:** Always fetch the latest changes Alby made:
   ```bash
   git pull origin main
   ```
2. **Commit often:** Keep your commits small and descriptive:
   ```bash
   git add .
   git commit -m "Add feature/update detail"
   ```
3. **Push to share:** Send your updates back to GitHub:
   ```bash
   git push origin main
   ```
