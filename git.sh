#!/bin/bash

# Variables - replace these with your repository details
GITHUB_USERNAME="your-username"   # Replace with your GitHub username
REPO_NAME="your-repo-name"        # Replace with the repository name you want to delete and recreate
LOCAL_REPO_PATH="/path/to/your/local/repo"  # Replace with the local path to your repository

# Step 1: Delete the repository on GitHub
echo "Deleting GitHub repository: $REPO_NAME"
gh repo delete "$GITHUB_USERNAME/$REPO_NAME" --confirm

# Step 2: Create a new repository on GitHub
echo "Recreating GitHub repository: $REPO_NAME"
gh repo create "$REPO_NAME" --public  # Use --private if you want a private repository

# Step 3: Initialize a new Git repository in the local directory (if not already initialized)
cd "$LOCAL_REPO_PATH"
git init

# Step 4: Set the new GitHub repository as the remote origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Step 5: Add all files and commit
git add .
git commit -m "Initial commit after recreation"

# Step 6: Push the changes to the new GitHub repository
git push -u origin main  # Replace 'main' with your default branch name if different

echo "Repository $REPO_NAME recreated and pushed to GitHub successfully."
