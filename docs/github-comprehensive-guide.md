# GitHub Comprehensive Guide for Cherry-in-the-Haystack

**Target Audience:** CS college student who knows basic Git commands
**Goal:** Understand GitHub concepts and safely manage cherry-in-the-haystack repository

---

## 📚 Table of Contents
1. [GitHub vs Git](#github-vs-git)
2. [Core Concepts](#core-concepts)
3. [Branching Strategy](#branching-strategy)
4. [Common Workflows](#common-workflows)
5. [Safety Procedures](#safety-procedures)
6. [Project-Specific Workflows](#project-specific-workflows)
7. [GitHub GUI Features](#github-gui-features)
8. [Troubleshooting](#troubleshooting)

---

## 🐘 GitHub vs Git: What's the Difference?

### Git (Version Control System)
- **Local tool** on your machine
- Tracks file changes, allows commits, branches, merges
- **Offline capable** - works without internet
- Commands: `git add`, `git commit`, `git push`, `git pull`

### GitHub (Hosting Platform)
- **Cloud service** that hosts Git repositories
- Stores code remotely
- Adds collaboration features: Issues, Pull Requests, Actions, Wiki
- **Online required** - needs internet
- URL: `https://github.com/`

### Analogy
```
Git = Your local file system with superpowers
GitHub = Dropbox + Google Docs + Code collaboration
```

---

## 🎯 Core Concepts

### Repository (Repo)
- A project folder with version history
- **Local repo:** `C:\Users\Hankeol\Desktop\Dev\cherry-in-the-helper`
- **Remote repo:** `github.com/username/repo-name.git`

### Commit
- A **snapshot** of your code at a point in time
- Has:
  - Unique ID (SHA hash, e.g., `a1b2c3d`)
  - Author (you)
  - Timestamp
  - Commit message (description of changes)
- **Think:** "Save point" in a video game

### Branch
- **Parallel timeline** of your code
- **Main branch:** `main` (or `master` in older repos)
- **Feature branches:** `feature/add-login`, `bugfix/fix-crash`
- **Think:** Different timelines in movies (like Everything Everywhere All At Once)

### Merge
- Combining changes from one branch into another
- **Types:**
  - `merge`: Creates a merge commit
  - `rebase`: Rewrites history to be linear
- **Think:** Combining two movie timelines into one

### Push
- Upload your local commits to GitHub
- **Command:** `git push`
- **Think:** Uploading your save game to cloud storage

### Pull
- Download changes from GitHub to your local machine
- **Command:** `git pull`
- **Think:** Downloading the latest cloud save to your local machine

### Clone
- Download a repository from GitHub to your local machine
- **Command:** `git clone <url>`
- **Think:** Downloading an entire project folder

---

## 🌳 Branching Strategy for cherry-in-the-haystack

### Current Branch Structure
```
main (production)
├── Your working code
└── Stable, deployed code

epic-1-2-integration (temporary)
├── Integration work
├── Testing
└── Will be merged to main when complete

feat/pdf-extractor-v2 (reference)
├── PDF extraction code
├── Historical
└── Read-only (don't commit here)

feat/pdf-knowledge-extractor (reference)
├── RSS + LLM analysis code
├── Historical
└── Read-only (don't commit here)

feature/ontology (reference)
├── GraphDB + ontology code
├── Historical
└── Read-only (don't commit here)
```

### Branch Naming Conventions
```
main                    # Production code
epic-1-2-integration   # Temporary integration work
feature/<name>         # New features (when we start adding new features)
bugfix/<name>          # Bug fixes
hotfix/<name>          # Urgent production fixes
```

---

## 🔀 Common Workflows

### Workflow 1: Create a Pre-Integration Backup

#### Why?
Create a "save point" before risky work so you can always go back.

#### Commands:
```bash
# 1. Check current branch
git branch
# Output: * main

# 2. Check for uncommitted changes
git status

# 3. Stage all changes (add to staging area)
git add .

# 4. Commit with message
git commit -m "Pre-integration backup: Epic 1 & 2 safe state"

# 5. Create a tag (named save point)
git tag pre-epic-1-2-integration-20250405-120000

# 6. Verify tag was created
git tag
# Output: pre-epic-1-2-integration-20250405-120000

# 7. Push to remote (backup to cloud)
git push origin main
git push origin pre-epic1-2-integration-20250405-120000
```

#### What Each Command Does:
| Command | What Happens |
|---------|-------------|
| `git branch` | Shows current branch |
| `git status` | Shows changed files not yet committed |
| `git add .` | Stages all changes for commit |
| `git commit` | Creates local save point with message |
| `git tag <name>` | Creates named reference to commit |
| `git push` | Uploads commits/tags to GitHub |

---

### Workflow 2: Create Integration Branch

#### Why?
Work on Epic 1 + 2 integration separately from main code.

#### Commands:
```bash
# 1. Create new branch from current branch
git checkout -b epic-1-2-integration

# 2. Verify you're on new branch
git branch
# Output:
#   * epic-1-2-integration
#     main

# 3. Push new branch to GitHub
git push -u origin epic-1-2-integration
```

#### What `-b` Flag Does:
- `git checkout -b <branch-name>` = Create new branch AND switch to it
- Equivalent to:
  ```bash
  git branch <branch-name>  # Create branch
  git checkout <branch-name>  # Switch to branch
  ```

#### What `-u` Flag Does:
- `-u` = "upstream" — Sets up tracking relationship
- First push: `git push -u origin epic-1-2-integration`
- Future pushes: `git push` (no `-u` needed)

---

### Workflow 3: Explore Other Branches Without Committing

#### Why?
Review code from feature branches without merging them into your work.

#### Commands:
```bash
# 1. Create a worktree (parallel checkout)
git worktree add ../temp-feature-ontology origin/feature/ontology

# 2. Work in the worktree
cd ../temp-feature-ontology
ls -la

# 3. Review code, take notes

# 4. Remove worktree when done (cleanup)
git worktree remove ../temp-feature-ontology
```

#### What is a Worktree?
- **Multiple working directories** from the same repository
- Allows you to work on different branches simultaneously
- **Like:** Having 2 folders with the same project, different branches checked out

#### Visual:
```
cherry-in-the-haystack/          # Main folder
├── .git/                        # Git database
├── main/                        # Main branch files
└── epic-1-2-integration/        # Integration branch files

../temp-feature-ontology/        # Worktree (separate folder)
└── feature-ontology/            # Feature branch files
```

---

### Workflow 4: Cherry-Pick Specific Commits

#### Why?
Extract specific commits from one branch without merging entire branch.

#### Commands:
```bash
# 1. View commit history
git log origin/feature/ontology --oneline

# 2. View commit details
git show <commit-hash> --stat

# 3. Cherry-pick (copy) a commit
git cherry-pick <commit-hash>

# 4. If conflicts occur:
#    - Open conflicted files
#    - Fix conflicts
#    - git add <files>
#    - git cherry-pick --continue
```

#### What Cherry-Picking Does:
```
Branch A: A → B → C → D
Branch B: X → Y → Z

git cherry-pick <commit C from Branch A>

Branch B becomes: X → Y → Z → C → D
                              ↑
                         Copied from Branch A
```

---

## 🛡️ Safety Procedures

### Safety Principle
**Always create a backup before risky operations.**

### Pre-Integration Backup Checklist
```bash
□ Commit all current work
□ Create backup tag
□ Push to remote
□ Verify backup exists on GitHub
□ Only then start integration work
```

### Rollback Hierarchy

#### Level 1: Undo Last Commit (Keep Changes)
```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Make fixes
git add <files>
git commit -m "Fixed: descriptive message"
```

#### Level 2: Reset to Backup Tag (Keep Files)
```bash
# Reset to backup, keep your files
git reset pre-epic-1-2-integration-*

# Review changes
git status

# Re-commit if needed
git add .
git commit -m "Redo: integration work"
```

#### Level 3: Full Rollback (Lose Integration Work)
```bash
# Go back to main, keep integration branch as reference
git checkout main

# Optionally delete integration branch
git branch -D epic-1-2-integration
```

---

## 📋 Project-Specific Workflows

### Workflow 1: Backup Before Integration

```bash
# 1. Save current work
git add .
git commit -m "Pre-integration backup: Epic 1 & 2 safe state"

# 2. Create backup tag with timestamp
git tag pre-epic-1-2-integration-$(date +%Y%m%d-%H%M%S)

# 3. Push to remote
git push origin main
git push origin pre-epic-1-2-integration-$(date +%Y%m%d-%H%M%S)

# 4. Create integration branch
git checkout -b epic-1-2-integration

# 5. Push integration branch
git push -u origin epic-1-2-integration
```

### Workflow 2: Daily Standup Sync

```bash
# At end of each work day:
git add .
git commit -m "Progress: completed [X, Y, Z]"

# Push to remote (backup + team visibility)
git push

# Morning: pull latest changes
git pull
```

### Workflow 3: Merge Integration to Main

**ONLY when Epic 1 + 2 is complete and tested:**

```bash
# 1. Switch to main
git checkout main

# 2. Pull latest main (in case others updated)
git pull origin main

# 3. Merge integration branch
git merge epic-1-2-integration

# 4. Push merged result
git push origin main

# 5. (Optional) Delete integration branch
git branch -d epic-1-2-integration
git push origin --delete epic-1-2-integration
```

---

## 🌐 GitHub GUI Features

### Viewing Commits
- **URL:** `github.com/<username>/<repo>/commits`
- **What you see:** List of commits, authors, timestamps
- **Filter by branch:** Use dropdown to select branch
- **Search commits:** Use search box to find specific commits

### Viewing File History
- Navigate to any file on GitHub
- Click "History" button (top right)
- **What you see:** Line-by-line changes, commit by commit

### Comparing Branches
- **URL:** `github.com/<username>/<repo>/compare`
- **Format:** `github.com/<username>/<repo>/compare/main...feature-branch`
- **What you see:** Side-by-side diff of files between branches

### Creating Issues
- Navigate to repository
- Click "Issues" tab
- Click "New Issue"
- Fill in title, description
- Add labels (e.g., `bug`, `enhancement`, `epic-1`)
- Assign to team members
- Click "Submit new issue"

### Resolving Merge Conflicts (GitHub GUI)
- Go to "Pull requests" tab
- Click on conflicted PR
- GitHub will show conflict interface
- Edit files directly in browser to resolve
- Mark as resolved
- Commit merge

---

## 🔍 Troubleshooting

### Problem: "Detached HEAD" state

**What happened?**
You checked out a specific commit directly (not a branch). You're in "no-man's land."

**Solution:**
```bash
# View where you are
git log --oneline

# Return to a branch
git checkout main  # or any branch name

# If you want to create a branch from here
git checkout -b new-branch-name
```

---

### Problem: "Failed to push"

**What happened?**
- Local branch is behind remote
- Someone else pushed to remote and your history diverged

**Solution:**
```bash
# Option 1: Pull first (merge remote changes)
git pull
git push

# Option 2: Force push (DANGEROUS - overwrites remote)
git push --force  # ONLY if you're sure

# Option 3: Rebase your changes on top of remote
git pull --rebase
git push
```

---

### Problem: Merge Conflict

**What happened?**
- You and someone else edited the same line of code differently
- Git doesn't know which version to keep

**Solution:**
```bash
# 1. See which files conflict
git status

# 2. Open conflicted files
# Look for <<<<<<< ======= , >>>>>>> markers

# 3. Edit files to resolve conflicts
# Keep what you want, remove markers

# 4. Stage resolved files
git add <resolved-files>

# 5. Complete merge
git commit -m "Resolved merge conflicts"
```

---

### Problem: "Untracked files would be overwritten"

**What happened?**
- You have local files not in Git that would be overwritten
- Git protects you from losing work

**Solution:**
```bash
# Option 1: Stash local changes
git stash
git pull
git stash pop  # Restore your changes after pull

# Option 2: Commit local files first
git add <files>
git commit -m "WIP: local files"
git pull
```

---

## 📊 GitHub Operations Summary

| Operation | Git Command | GitHub Concept | Purpose |
|-----------|------------|-----------------|---------|
| Create save point | `git commit` | Commit | Save current state |
| Create named save point | `git tag` | Tag | Mark milestone |
| Upload to cloud | `git push` | Push | Backup + share |
| Download from cloud | `git pull` | Pull/Fetch | Get updates |
| Switch timeline | `git checkout` | Checkout | Change branches |
| Combine timelines | `git merge` | Merge/Pull Request | Integrate work |
| Copy commit | `git cherry-pick` | Cherry-pick | Extract specific change |
| Parallel checkout | `git worktree add` | Worktree | Explore without merging |

---

## 🎓 Key Takeaways

1. **Git is local, GitHub is remote** - Git works offline, GitHub needs internet
2. **Commit = Save point** - Each commit is a snapshot you can return to
3. **Tag = Named save point** - Tags mark important milestones (releases, backups)
4. **Branch = Timeline** - Different parallel versions of your code
5. **Push = Backup + Share** - Pushing uploads your code to GitHub
6. **Pull = Update + Download** - Pulling gets others' changes
7. **Merge = Integrate** - Merging combines work from different timelines
8. **Worktree = Parallel workspace** - Worktrees let you work on multiple branches simultaneously

---

## 🚀 Quick Reference Commands

### Essential Commands
```bash
# Check current state
git status
git branch
git log --oneline --graph --all

# Save work
git add .
git commit -m "message"

# Branch management
git checkout <branch>
git checkout -b <new-branch>
git branch -d <branch>  # Delete local branch
git push -d origin <branch>  # Delete remote branch

# Remote operations
git push
git pull
git fetch
```

### Safety Commands
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~

# Reset to tag (keep files)
git reset <tag-name>

# Undo all commits since tag (lose changes)
git reset --hard <tag-name>

# View diff before committing
git diff              # Changes not staged
git diff --staged      # Staged changes
git diff HEAD~1        # Last commit changes
```

---

## 📚 Additional Resources

- **Pro Git Book:** https://git-scm.com/book/
- **GitHub Docs:** https://docs.github.com/
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet.pdf

---

**Last Updated:** 2026-04-05
**For:** cherry-in-the-haystack team
**Maintained by:** Tech Lead
