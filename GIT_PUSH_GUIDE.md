# Git Push Guide - Creating "Tin" Branch

## Step 1: Initialize Git (Already Done ✅)

```bash
cd "/Users/tinthuzaraye/Documents/Learning_Course/CMPE272/Frontend:Backend"
git init
```

## Step 2: Stage All Files

```bash
git add .
```

## Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Full-stack authentication app with React frontend and Express backend"
```

## Step 4: Create and Switch to "Tin" Branch

```bash
git checkout -b Tin
```

## Step 5: Add Your Existing GitHub Repository as Remote

Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub info:

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
```

**Example:**

```bash
git remote add origin https://github.com/tinthuzaraye/my-fullstack-app.git
```

## Step 6: Push the "Tin" Branch to GitHub

```bash
git push -u origin Tin
```

If you get an error about the branch already existing on GitHub, use:

```bash
git push origin Tin --force
```

## Alternative: If Repository Already Has a Remote

If you're connecting to an existing repository that already has commits:

```bash
# Fetch the existing branches
git fetch origin

# Create your Tin branch
git checkout -b Tin

# Push your branch
git push -u origin Tin
```

## Complete Step-by-Step Commands:

```bash
# Navigate to your project
cd "/Users/tinthuzaraye/Documents/Learning_Course/CMPE272/Frontend:Backend"

# Stage all files
git add .

# Commit your changes
git commit -m "Initial commit: Full-stack authentication app"

# Create and switch to Tin branch
git checkout -b Tin

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push Tin branch to GitHub
git push -u origin Tin
```

## Verify Your Branch

After pushing, you can verify:

```bash
# Check current branch
git branch

# Check remote branches
git branch -r

# Check all branches
git branch -a
```

## Future Updates

After the initial push, to update your Tin branch:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Switch Between Branches

```bash
# Switch to main branch
git checkout main

# Switch back to Tin branch
git checkout Tin

# See all branches
git branch
```

## Notes:

- The `.gitignore` file has been created to exclude:

  - node_modules/
  - .env files (to protect sensitive data)
  - build outputs
  - logs and temporary files

- Your `.env` file with database credentials will NOT be pushed to GitHub (it's in .gitignore)
- Make sure to create a `.env.example` file for others to know what environment variables are needed

## GitHub Repository URL Format:

- HTTPS: `https://github.com/username/repository.git`
- SSH: `git@github.com:username/repository.git`
