# Public Repository Setup

This document explains how to push your Runa development work to the public GitHub repository.

## Current Remote Configuration

- **`runa-origin`**: Your private development repository
- **`public`**: The public GitHub repository at https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang.git

## Quick Push Commands

### Push to Public Repository
```bash
# Push current branch to public repo
git push public main:main

# Push specific branch
git push public feature-branch:feature-branch

# Push and set upstream (for future pushes)
git push -u public main:main
```

### Using the Push Scripts

#### PowerShell (Recommended)
```powershell
# Push main branch
.\push-to-public.ps1

# Push specific branch
.\push-to-public.ps1 feature-branch
```

#### Batch File
```cmd
# Push main branch
push-to-public.bat

# Push specific branch
push-to-public.bat feature-branch
```

## Workflow Recommendations

### 1. Development Cycle
```
1. Work on features in private repo (runa-origin)
2. Test and validate thoroughly
3. Commit changes locally
4. Push to public repo when ready
```

### 2. Branch Strategy
```
main (private) → main (public)     # Stable releases
feature/* (private) → feature/* (public)  # Feature development
```

### 3. Quality Gates
- ✅ All tests passing
- ✅ Documentation updated
- ✅ Code reviewed
- ✅ No proprietary content
- ✅ License compliance verified

## Important Notes

### What Gets Pushed
- Core Runa language implementation
- Standard library modules
- Language specification
- User documentation
- Examples and tests
- Build system

### What Stays Private
- Proprietary development tools
- Internal testing frameworks
- Hermod integration code
- Commercial components
- Development roadmaps

## Troubleshooting

### Authentication Issues
```bash
# Set up personal access token
git remote set-url public https://YOUR_TOKEN@github.com/Sybertnetics-Artificial-Intelligence/RunaLang.git
```

### Merge Conflicts
```bash
# Fetch latest from public
git fetch public

# Merge or rebase
git merge public/main
# OR
git rebase public/main
```

### Reset Public Remote
```bash
# Remove and re-add if needed
git remote remove public
git remote add public https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang.git
```

## Best Practices

1. **Always test locally** before pushing to public
2. **Use meaningful commit messages** for public history
3. **Keep public repo clean** - no WIP commits
4. **Regular sync** - don't let branches diverge too much
5. **Document changes** in public-facing docs

## Need Help?

- Check git status: `git status`
- View remotes: `git remote -v`
- View branch status: `git branch -a`
- Check public repo: https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang
