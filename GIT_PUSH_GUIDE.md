# Push to GitHub Repository

## Quick Commands

```bash
# Navigate to project root
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit changes
git commit -m "Complete Risk Analyzer with email alerts and AI insights"

# Add remote repository
git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git

# Push to main branch
git push -u origin main
```

## If Repository Already Exists

```bash
cd "C:\Users\Rajesh Yuvaraja\Risk-Analyzer"

# Add all changes
git add .

# Commit
git commit -m "Update: Email alerts, MySQL fixes, and code improvements"

# Push
git push origin main
```

## If You Get Errors

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/Rajesh2404y/Risk-Analyzer.git
git push -u origin main
```

### Error: "failed to push"
```bash
# Force push (use carefully)
git push -f origin main
```

### Error: "branch main doesn't exist"
```bash
# Create and push main branch
git branch -M main
git push -u origin main
```

## Create .gitignore First

```bash
# Create .gitignore to exclude sensitive files
echo "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Node
node_modules/
dist/
.npm

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite" > .gitignore

git add .gitignore
git commit -m "Add gitignore"
```

## Complete Fresh Push

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
