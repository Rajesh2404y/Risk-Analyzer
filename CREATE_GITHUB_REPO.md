# Create GitHub Repository First

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `Risk-Analyzer`
   - **Description**: `AI-Based Personal Expense Risk Analyzer with ML predictions and email alerts`
   - **Visibility**: Public (or Private)
   - **DO NOT** check "Initialize with README" (you already have one)
3. Click **Create repository**

## Step 2: Push Your Code

After creating the repository, run these commands:

```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI-Based Personal Expense Risk Analyzer"

# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git

# Push
git push -u origin main
```

## If Repository Already Exists

If you already created it, just push:

```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git
git branch -M main
git push -u origin main
```

## Authentication

When prompted for credentials:
- **Username**: Rajesh2404y
- **Password**: Use Personal Access Token (not your GitHub password)

### Generate Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all)
4. Click "Generate token"
5. Copy the token
6. Use it as password when pushing

## Done!

Visit: https://github.com/Rajesh2404y/Risk-Analyzer

Your project is now on GitHub! 🎉
