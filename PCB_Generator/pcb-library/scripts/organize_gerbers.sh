#!/bin/bash

# organize_gerbers.sh
# Organizes Gerber files by project, separating PCB and plate files
# Usage: ./organize_gerbers.sh <source_repo_path> <project_name>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check arguments
if [ $# -lt 2 ]; then
    print_error "Usage: $0 <source_repo_path> <project_name>"
    exit 1
fi

SOURCE_REPO="$1"
PROJECT_NAME="$2"

# Get script directory and set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PCB_DIR="$(dirname "$SCRIPT_DIR")"
GERBERS_DIR="$PCB_DIR/gerbers"
PROJECT_GERBERS_DIR="$GERBERS_DIR/$PROJECT_NAME"

print_info "Organizing Gerber files for project: $PROJECT_NAME"
print_info "Source repository: $SOURCE_REPO"

# Check if source repository exists
if [ ! -d "$SOURCE_REPO" ]; then
    print_error "Source repository not found: $SOURCE_REPO"
    exit 1
fi

# Create project gerbers directory structure
mkdir -p "$PROJECT_GERBERS_DIR/pcb"
mkdir -p "$PROJECT_GERBERS_DIR/plate"

# Find Gerber files (common extensions)
GERBER_EXTENSIONS=("*.gbr" "*.gbl" "*.gtl" "*.gbs" "*.gts" "*.gbo" "*.gto" "*.gm1" "*.gko" "*.drl" "*.txt")
GERBER_ZIP_PATTERN="*gerber*.zip"

# Track found files
FOUND_FILES=0
PCB_FILES=0
PLATE_FILES=0

# Function to determine if file is plate-related
is_plate_file() {
    local filename=$(basename "$1")
    local lowercase=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    
    if [[ "$lowercase" == *"plate"* ]] || [[ "$lowercase" == *"switch"* ]]; then
        return 0
    fi
    return 1
}

# Function to validate Gerber completeness
validate_gerber_set() {
    local dir="$1"
    local type="$2"
    
    # Required layers for a complete PCB Gerber set
    local has_top_copper=false
    local has_bottom_copper=false
    local has_drill=false
    local has_outline=false
    
    for file in "$dir"/*; do
        if [ -f "$file" ]; then
            local basename=$(basename "$file")
            local lowercase=$(echo "$basename" | tr '[:upper:]' '[:lower:]')
            
            # Check for top copper
            if [[ "$lowercase" == *".gtl"* ]] || [[ "$lowercase" == *"top"*"copper"* ]] || [[ "$lowercase" == *"f.cu"* ]]; then
                has_top_copper=true
            fi
            
            # Check for bottom copper
            if [[ "$lowercase" == *".gbl"* ]] || [[ "$lowercase" == *"bottom"*"copper"* ]] || [[ "$lowercase" == *"b.cu"* ]]; then
                has_bottom_copper=true
            fi
            
            # Check for drill file
            if [[ "$lowercase" == *".drl"* ]] || [[ "$lowercase" == *"drill"* ]] || [[ "$lowercase" == *".txt"* ]]; then
                has_drill=true
            fi
            
            # Check for outline
            if [[ "$lowercase" == *".gko"* ]] || [[ "$lowercase" == *".gm1"* ]] || [[ "$lowercase" == *"edge"* ]] || [[ "$lowercase" == *"outline"* ]]; then
                has_outline=true
            fi
        fi
    done
    
    # Report validation results
    print_info "Validating $type Gerber set:"
    
    if [ "$has_top_copper" = true ]; then
        print_info "  ✓ Top copper layer found"
    else
        print_warning "  ✗ Top copper layer missing"
    fi
    
    if [ "$has_bottom_copper" = true ]; then
        print_info "  ✓ Bottom copper layer found"
    else
        print_warning "  ✗ Bottom copper layer missing"
    fi
    
    if [ "$has_drill" = true ]; then
        print_info "  ✓ Drill file found"
    else
        print_warning "  ✗ Drill file missing"
    fi
    
    if [ "$has_outline" = true ]; then
        print_info "  ✓ Board outline found"
    else
        print_warning "  ✗ Board outline missing"
    fi
    
    if [ "$has_top_copper" = true ] && [ "$has_bottom_copper" = true ] && [ "$has_drill" = true ] && [ "$has_outline" = true ]; then
        print_info "  ${GREEN}Complete Gerber set${NC}"
        return 0
    else
        print_warning "  ${YELLOW}Incomplete Gerber set - manual review recommended${NC}"
        return 1
    fi
}

# Search for Gerber ZIP files
print_info "Searching for Gerber ZIP archives..."
while IFS= read -r -d '' zipfile; do
    print_info "Found Gerber ZIP: $(basename "$zipfile")"
    
    # Determine if it's a plate file
    if is_plate_file "$zipfile"; then
        TARGET_DIR="$PROJECT_GERBERS_DIR/plate"
        print_info "  → Identified as PLATE Gerber"
        ((PLATE_FILES++))
    else
        TARGET_DIR="$PROJECT_GERBERS_DIR/pcb"
        print_info "  → Identified as PCB Gerber"
        ((PCB_FILES++))
    fi
    
    # Copy the ZIP file
    cp "$zipfile" "$TARGET_DIR/"
    print_info "  → Copied to $TARGET_DIR"
    
    # Extract ZIP to temporary directory for validation
    TEMP_DIR=$(mktemp -d)
    unzip -q "$zipfile" -d "$TEMP_DIR"
    
    # Copy extracted files as well
    find "$TEMP_DIR" -type f \( -name "*.gbr" -o -name "*.gbl" -o -name "*.gtl" -o -name "*.gbs" -o -name "*.gts" -o -name "*.gbo" -o -name "*.gto" -o -name "*.gm1" -o -name "*.gko" -o -name "*.drl" -o -name "*.txt" \) -exec cp {} "$TARGET_DIR/" \;
    
    # Cleanup temp directory
    rm -rf "$TEMP_DIR"
    
    ((FOUND_FILES++))
done < <(find "$SOURCE_REPO" -type f -iname "$GERBER_ZIP_PATTERN" -print0)

# Search for loose Gerber files
print_info "Searching for loose Gerber files..."
for ext in "${GERBER_EXTENSIONS[@]}"; do
    while IFS= read -r -d '' gerberfile; do
        # Skip if already in our gerbers directory
        if [[ "$gerberfile" == *"/gerbers/"* ]]; then
            continue
        fi
        
        print_info "Found Gerber file: $(basename "$gerberfile")"
        
        # Determine if it's a plate file
        if is_plate_file "$gerberfile"; then
            TARGET_DIR="$PROJECT_GERBERS_DIR/plate"
            print_info "  → Identified as PLATE Gerber"
            ((PLATE_FILES++))
        else
            TARGET_DIR="$PROJECT_GERBERS_DIR/pcb"
            print_info "  → Identified as PCB Gerber"
            ((PCB_FILES++))
        fi
        
        # Copy the file
        cp "$gerberfile" "$TARGET_DIR/"
        print_info "  → Copied to $TARGET_DIR"
        
        ((FOUND_FILES++))
    done < <(find "$SOURCE_REPO" -type f -iname "$ext" -print0)
done

# Validate Gerber sets
print_info ""
print_info "Validating Gerber file completeness..."

if [ "$(ls -A "$PROJECT_GERBERS_DIR/pcb" 2>/dev/null)" ]; then
    validate_gerber_set "$PROJECT_GERBERS_DIR/pcb" "PCB"
else
    print_warning "No PCB Gerber files found"
fi

if [ "$(ls -A "$PROJECT_GERBERS_DIR/plate" 2>/dev/null)" ]; then
    validate_gerber_set "$PROJECT_GERBERS_DIR/plate" "PLATE"
else
    print_info "No plate Gerber files found (this is normal for many projects)"
    # Remove empty plate directory
    rmdir "$PROJECT_GERBERS_DIR/plate" 2>/dev/null || true
fi

# Summary
print_info ""
print_info "========================================="
print_info "Gerber Organization Summary"
print_info "========================================="
print_info "Project: $PROJECT_NAME"
print_info "Total files found: $FOUND_FILES"
print_info "PCB files: $PCB_FILES"
print_info "Plate files: $PLATE_FILES"
print_info "Output directory: $PROJECT_GERBERS_DIR"
print_info "========================================="

if [ $FOUND_FILES -eq 0 ]; then
    print_warning "No Gerber files found in source repository"
    print_warning "Please check if Gerber files are available or use a different source"
    exit 1
fi

print_info "${GREEN}Gerber organization complete!${NC}"
