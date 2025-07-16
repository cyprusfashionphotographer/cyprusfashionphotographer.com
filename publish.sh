#!/bin/bash

# Set user
git config user.name "cyprusfashionphotographer"
git config user.email "cyprusfashionphotographer@outlook.com"

# Commit and push
git checkout main
git add .
git commit -m "Update"
git push