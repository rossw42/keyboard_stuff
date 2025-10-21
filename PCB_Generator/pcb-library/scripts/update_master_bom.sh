#!/usr/bin/env bash

# Master BOM Update Script
# Consolidates all project BOMs into master BOM
# Usage: ./update_master_bom.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PCB_ROOT="$(dirname "$SCRIPT_DIR")"
BOM_DIR="${PCB_ROOT}/boms"
CONFIG_FILE="${SCRIPT_DIR}/normalization_config.json"

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

# Check if BOM directory exists
if [ ! -d "$BOM_DIR" ]; then
    log_error "BOM directory not found: $BOM_DIR"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    log_error "python3 is required but not installed"
    exit 1
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    log_info "Creating default normalization config..."
    python3 "${SCRIPT_DIR}/normalize_components.py" create-config "$CONFIG_FILE"
fi

log_section "Updating Master BOM"

# Run BOM consolidation
log_info "Consolidating BOMs from all projects..."
if python3 "${SCRIPT_DIR}/consolidate_bom.py" "$BOM_DIR" "$CONFIG_FILE"; then
    log_section "Master BOM Update Complete!"
    log_info "Generated files:"
    log_info "  - ${BOM_DIR}/master-bom.csv"
    log_info "  - ${BOM_DIR}/master-bom-summary.md"
    log_info "  - ${BOM_DIR}/by-category/*.csv"
else
    log_error "Failed to consolidate BOMs"
    exit 1
fi

exit 0
