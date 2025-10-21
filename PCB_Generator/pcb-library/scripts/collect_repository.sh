#!/usr/bin/env bash

# Repository Collection Script
# Clones GitHub repositories with error handling and retry logic
# Usage: ./collect_repository.sh <github-url> <project-name>

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PCB_ROOT="$(dirname "$SCRIPT_DIR")"
TEMP_DIR="${PCB_ROOT}/.temp"
MAX_RETRIES=3
INITIAL_BACKOFF=2

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate inputs
if [ $# -ne 2 ]; then
    log_error "Usage: $0 <github-url> <project-name>"
    log_error "Example: $0 https://github.com/coseyfannitutti/discipline discipline"
    exit 1
fi

REPO_URL="$1"
PROJECT_NAME="$2"

# Validate GitHub URL format
if ! echo "$REPO_URL" | grep -qE '^https://github\.com/[^/]+/[^/]+/?$'; then
    log_error "Invalid GitHub URL format: $REPO_URL"
    log_error "Expected format: https://github.com/username/repository"
    exit 1
fi

# Validate project name (alphanumeric, hyphens, underscores only)
if ! echo "$PROJECT_NAME" | grep -qE '^[a-zA-Z0-9_-]+$'; then
    log_error "Invalid project name: $PROJECT_NAME"
    log_error "Project name must contain only letters, numbers, hyphens, and underscores"
    exit 1
fi

log_info "Starting repository collection for: $PROJECT_NAME"
log_info "Repository URL: $REPO_URL"

# Create temp directory if it doesn't exist
mkdir -p "$TEMP_DIR"

# Clone destination
CLONE_DIR="${TEMP_DIR}/${PROJECT_NAME}"

# Function to clone repository with retry logic
clone_with_retry() {
    local url="$1"
    local dest="$2"
    local attempt=1
    local backoff=$INITIAL_BACKOFF
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log_info "Clone attempt $attempt of $MAX_RETRIES..."
        
        # Remove existing directory if present
        if [ -d "$dest" ]; then
            log_warn "Removing existing clone directory: $dest"
            rm -rf "$dest"
        fi
        
        # Attempt to clone
        if git clone --depth 1 "$url" "$dest" 2>&1; then
            log_info "Successfully cloned repository"
            return 0
        else
            log_warn "Clone attempt $attempt failed"
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                log_info "Waiting ${backoff}s before retry..."
                sleep $backoff
                backoff=$((backoff * 2))  # Exponential backoff
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    log_error "Failed to clone repository after $MAX_RETRIES attempts"
    return 1
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    log_error "git is not installed. Please install git and try again."
    exit 1
fi

# Check network connectivity
if ! ping -c 1 github.com &> /dev/null; then
    log_error "Cannot reach github.com. Please check your network connection."
    exit 1
fi

# Clone the repository
if ! clone_with_retry "$REPO_URL" "$CLONE_DIR"; then
    exit 1
fi

# Verify clone was successful
if [ ! -d "$CLONE_DIR/.git" ]; then
    log_error "Clone directory exists but is not a valid git repository"
    exit 1
fi

# Get repository metadata
cd "$CLONE_DIR"
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_DATE=$(git log -1 --format=%cd --date=short)
log_info "Cloned commit: $COMMIT_HASH (date: $COMMIT_DATE)"

# Count files in repository
FILE_COUNT=$(find . -type f ! -path './.git/*' | wc -l | tr -d ' ')
log_info "Repository contains $FILE_COUNT files"

log_info "Repository cloned successfully to: $CLONE_DIR"
log_info "Next step: Run file organization script to process files"

exit 0
