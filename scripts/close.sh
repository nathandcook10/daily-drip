#!/bin/bash
# 💧 Daily Drip - Session Wrapup and Notification Utility

# Color codes for premium CLI output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}💧 [Daily Drip] WRAPPING UP CURRENT SESSION...${NC}"

# Find repo root
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Check if we have active changes to commit
CHANGES=$(git status --porcelain)

if [ -n "$CHANGES" ]; then
    echo -e "${YELLOW}⚡ Found uncommitted changes in your workspace:${NC}"
    git status -s
    echo ""
    
    # Prompt for commit message
    read -p "📝 Enter commit message (or press enter for default 'chore: daily drip update'): " msg
    if [ -z "$msg" ]; then
        msg="chore: daily drip update"
    fi
    
    echo -e "${BLUE}🔄 Staging and committing changes...${NC}"
    git add .
    git commit -m "$msg"
else
    echo -e "${GREEN}✅ No uncommitted changes in workspace. Workspace is clean!${NC}"
fi

# Push latest commits to GitHub
echo -e "${BLUE}🚀 Pushing changes to GitHub...${NC}"
if git push; then
    echo -e "${GREEN}✅ Pushed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️ Git push failed or nothing to push. Proceeding to notification...${NC}"
fi

# Text Alby
echo -e "${BLUE}💬 Sending closing notification to Alby...${NC}"
python3 "$REPO_ROOT/scripts/notify_alby.py" close

echo -e "${GREEN}🎉 All done! Session closed and Alby has been notified.${NC}"
