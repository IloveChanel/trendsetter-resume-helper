#!/bin/bash

# Build script for Render deployment
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies with preference for binary packages
pip install --prefer-binary --no-cache-dir -r requirements.txt