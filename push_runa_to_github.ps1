# PowerShell script to push runa directory to GitHub
# This script helps manage the subtree workflow for the Runa project

Write-Host "Pushing Runa directory to GitHub..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "runa")) {
    Write-Host "Error: runa directory not found. Please run this script from the monorepo root." -ForegroundColor Red
    exit 1
}

# Add all changes
Write-Host "Adding changes..." -ForegroundColor Yellow
git add .

# Commit changes if there are any
$status = git status --porcelain
if ($status) {
    $commitMessage = Read-Host "Enter commit message (or press Enter for default)"
    if (-not $commitMessage) {
        $commitMessage = "Update Runa project"
    }
    git commit -m $commitMessage
    Write-Host "Changes committed." -ForegroundColor Green
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

# Push to the main monorepo
Write-Host "Pushing to monorepo..." -ForegroundColor Yellow
git push

# Push the runa subtree to GitHub
Write-Host "Pushing runa subtree to GitHub..." -ForegroundColor Yellow
try {
    git subtree push --prefix=runa runa-origin main
    Write-Host "Successfully pushed runa to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "Subtree push failed. Trying alternative approach..." -ForegroundColor Yellow
    # Alternative: push the entire repo and let GitHub handle it
    git push runa-origin main
    Write-Host "Pushed to GitHub using alternative method." -ForegroundColor Green
}

Write-Host "Done!" -ForegroundColor Green 