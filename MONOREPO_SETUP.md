# Monorepo Setup for Runa Project

This monorepo contains the Runa programming language project along with other related projects. The `runa` directory is maintained as a separate GitHub repository while being part of this monorepo.

## Current Setup

- **Monorepo**: Contains `runa` directory and other projects
- **Runa Repository**: `https://github.com/SybertneticsAISolutions/Runa.git`
- **Remote Name**: `runa-origin`

## Directory Structure

```
MonoRepo/
├── runa/                    # Runa programming language project
│   ├── src/                # Source code
│   ├── docs/               # Documentation
│   ├── tests/              # Test files
│   └── ...
├── docs/                   # Monorepo documentation
├── hermod/                 # Hermod project (future)
└── ...
```

## Workflow

### Daily Development

1. **Make changes** in the `runa/` directory
2. **Commit changes** to the monorepo:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
3. **Push to GitHub** using the provided script:
   ```powershell
   .\push_runa_to_github.ps1
   ```

### Manual Push Process

If you prefer to push manually:

1. **Push to monorepo** (if you have a monorepo remote):
   ```bash
   git push
   ```

2. **Push runa to GitHub**:
   ```bash
   git push runa-origin main
   ```

## Build Artifacts

The `.gitignore` file has been updated to exclude:
- Rust build artifacts (`target/`, `*.rlib`, `*.d`, etc.)
- Python artifacts (`__pycache__/`, `*.pyc`, etc.)
- IDE files (`.vscode/`, `.idea/`, etc.)
- OS files (`.DS_Store`, `Thumbs.db`, etc.)

## Troubleshooting

### If subtree push fails:
The current setup uses a simple approach where the entire repository is pushed to GitHub. The `runa` directory is the main content, so this works well.

### If you need to reset the GitHub repository:
1. Delete the repository on GitHub
2. Create a new repository
3. Update the remote:
   ```bash
   git remote set-url runa-origin https://github.com/SybertneticsAISolutions/Runa.git
   ```
4. Push:
   ```bash
   git push runa-origin main
   ```

## Future Improvements

- Consider using Git submodules for cleaner separation
- Implement automated CI/CD for the Runa project
- Add more sophisticated subtree management if needed

## Notes

- The `runa` directory is the primary content for the GitHub repository
- Build artifacts are excluded to keep the repository clean
- The monorepo structure allows for easy development while maintaining separate repositories 