#!/bin/bash

echo "=== README.md contents ==="
cat /mnt/persist/workspace/README.md

echo -e "\n=== Git repository information ==="
cd /mnt/persist/workspace
git status
git log --oneline -10 2>/dev/null || echo "No commits found"
git branch -a 2>/dev/null || echo "No branches found"

echo -e "\n=== Checking for any hidden files ==="
ls -la /mnt/persist/workspace/
find /mnt/persist/workspace -name ".*" -type f | head -20