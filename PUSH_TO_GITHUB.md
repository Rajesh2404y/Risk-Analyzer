# 🚀 Push to GitHub - Step by Step

## Quick Commands

```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

git add .
git commit -m "Complete AI-Based Personal Expense Risk Analyzer with email alerts"
git push origin main
```

## Detailed Steps

### Step 1: Navigate to Project
```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"
```

### Step 2: Check Git Status
```bash
git status
```

### Step 3: Add All Files
```bash
git add .
```

### Step 4: Commit Changes
```bash
git commit -m "Complete AI-Based Personal Expense Risk Analyzer with email alerts"
```

### Step 5: Push to GitHub
```bash
git push origin main
```

## If You Get Errors

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git
git push -u origin main
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push origin main
```

### Error: "branch main doesn't exist"
```bash
git branch -M main
git push -u origin main
```

### Error: "Authentication failed"
```bash
# Use GitHub Personal Access Token
# Generate at: https://github.com/settings/tokens
# Use token as password when prompted
```

## Fresh Start (If Needed)

```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

# Remove existing git
rmdir /s /q .git

# Initialize fresh
git init
git add .
git commit -m "Initial commit: AI-Based Personal Expense Risk Analyzer"
git branch -M main
git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git
git push -u origin main
```

## Verify .gitignore

Make sure `.gitignore` exists and contains:
```
.env
node_modules/
__pycache__/
*.pyc
dist/
```

This protects your sensitive data!

## After Pushing

Visit: https://github.com/Rajesh2404y/Risk-Analyzer

You should see:
- ✅ All your code
- ✅ README.md
- ✅ Frontend and Backend folders
- ✅ No .env file (protected)

## Done! 🎉

Your project is now on GitHub!
