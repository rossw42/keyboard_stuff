#!/usr/bin/env bash

# Master Repository Processing Script
# Orchestrates cloning, organizing, and metadata extraction
# Usage: ./process_repository.sh <github-url> <project-name>

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# Validate inputs
if [ $# -ne 2 ]; then
    log_error "Usage: $0 <github-url> <project-name>"
    log_error "Example: $0 https://github.com/coseyfannitutti/discipline discipline"
    exit 1
fi

REPO_URL="$1"
PROJECT_NAME="$2"

log_section "Processing Repository: $PROJECT_NAME"
log_info "Repository URL: $REPO_URL"

# Step 1: Clone repository
log_section "Step 1/3: Cloning Repository"
if ! "${SCRIPT_DIR}/collect_repository.sh" "$REPO_URL" "$PROJECT_NAME"; then
    log_error "Failed to clone repository"
    exit 1
fi

# Step 2: Organize files
log_section "Step 2/3: Organizing Files"
if ! "${SCRIPT_DIR}/organize_files.sh" "$PROJECT_NAME"; then
    log_error "Failed to organize files"
    exit 1
fi

# Step 3: Extract metadata
log_section "Step 3/3: Extracting Metadata"
if ! "${SCRIPT_DIR}/extract_metadata.sh" "$PROJECT_NAME" "$REPO_URL"; then
    log_error "Failed to extract metadata"
    exit 1
fi

log_section "Processing Complete!"
log_info "Project: $PROJECT_NAME"
log_info "Files organized in PCB directory structure"
log_info "Project README: docs/build-guides/${PROJECT_NAME}/README.md"
log_info "Repository inventory updated: docs/repository_inventory.md"

exit 0
