#!/usr/bin/env bash

# 3D Model Organization Script
# Collects, organizes, and validates STL and STEP files
# Usage: ./organize_3d_models.sh <project-name>

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PCB_ROOT="$(dirname "$SCRIPT_DIR")"
TEMP_DIR="${PCB_ROOT}/.temp"

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

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Validate inputs
if [ $# -ne 1 ]; then
    log_error "Usage: $0 <project-name>"
    log_error "Example: $0 discipline"
    exit 1
fi

PROJECT_NAME="$1"
SOURCE_DIR="${TEMP_DIR}/${PROJECT_NAME}"

# Validate source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    log_error "Source directory not found: $SOURCE_DIR"
    log_error "Please run collect_repository.sh first"
    exit 1
fi

log_info "Organizing 3D models and CAD files for project: $PROJECT_NAME"

# Create project-specific 3D model directories
create_3d_dirs() {
    local project="$1"
    
    log_info "Creating 3D model directory structure for $project..."
    
    mkdir -p "${PCB_ROOT}/3d-models/cases/${project}/stl"
    mkdir -p "${PCB_ROOT}/3d-models/cases/${project}/step"
    mkdir -p "${PCB_ROOT}/3d-models/plates/${project}"
    mkdir -p "${PCB_ROOT}/3d-models/accessories/component-cradles/${project}"
    mkdir -p "${PCB_ROOT}/3d-models/accessories/covers/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/plates/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/cases/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/covers/${project}"
}

# Validate STL file integrity
validate_stl() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Check if file is readable
    if [ ! -r "$file" ]; then
        log_error "Cannot read file: $filename"
        return 1
    fi
    
    # Check file size (STL files should be > 84 bytes minimum header)
    local filesize=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    if [ "$filesize" -lt 84 ]; then
        log_error "STL file too small (corrupted?): $filename ($filesize bytes)"
        return 1
    fi
    
    # Check for STL header (ASCII or binary)
    local header=$(head -c 5 "$file" 2>/dev/null || echo "")
    if [[ "$header" == "solid" ]]; then
        log_debug "Valid ASCII STL: $filename"
        return 0
    elif [ "$filesize" -gt 84 ]; then
        # Binary STL files don't start with "solid"
        log_debug "Valid binary STL: $filename"
        return 0
    else
        log_warn "Unrecognized STL format: $filename"
        return 1
    fi
}

# Detect 3D model type based on filename
detect_3d_type() {
    local filename="$1"
    local lowercase_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    
    # Case files
    if [[ "$lowercase_name" =~ (case|housing|enclosure|shell|body|frame|tray) ]]; then
        echo "case"
        return
    fi
    
    # Plate files
    if [[ "$lowercase_name" =~ (plate|switch.*plate|mounting.*plate) ]]; then
        echo "plate"
        return
    fi
    
    # Component cradles/holders
    if [[ "$lowercase_name" =~ (cradle|holder|support|socket|mount) ]]; then
        echo "cradle"
        return
    fi
    
    # Covers/lids
    if [[ "$lowercase_name" =~ (cover|lid|top|bottom|cap) ]]; then
        echo "cover"
        return
    fi
    
    # Default to case if unclear
    echo "case"
}

# Detect CAD drawing type
detect_cad_type() {
    local filename="$1"
    local lowercase_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    
    # Plate drawings
    if [[ "$lowercase_name" =~ (plate|switch) ]]; then
        echo "plate"
        return
    fi
    
    # Case drawings
    if [[ "$lowercase_name" =~ (case|housing|enclosure) ]]; then
        echo "case"
        return
    fi
    
    # Cover drawings
    if [[ "$lowercase_name" =~ (cover|lid|top|bottom) ]]; then
        echo "cover"
        return
    fi
    
    # Default to plate (most common for DXF files)
    echo "plate"
}

# Copy file with validation
copy_with_validation() {
    local src="$1"
    local dest_dir="$2"
    local filename=$(basename "$src")
    
    # Ensure destination directory exists
    mkdir -p "$dest_dir"
    
    # Check if file already exists
    if [ -f "${dest_dir}/${filename}" ]; then
        log_warn "File already exists: ${dest_dir}/${filename}"
        # Compare file sizes
        local src_size=$(stat -f%z "$src" 2>/dev/null || stat -c%s "$src" 2>/dev/null)
        local dest_size=$(stat -f%z "${dest_dir}/${filename}" 2>/dev/null || stat -c%s "${dest_dir}/${filename}" 2>/dev/null)
        
        if [ "$src_size" -eq "$dest_size" ]; then
            log_debug "Identical file exists, skipping: $filename"
            return 0
        else
            log_warn "Different file with same name exists, creating backup"
            local timestamp=$(date +%Y%m%d_%H%M%S)
            mv "${dest_dir}/${filename}" "${dest_dir}/${filename}.${timestamp}.bak"
        fi
    fi
    
    # Copy file
    cp "$src" "${dest_dir}/${filename}"
    log_debug "Copied: $filename -> $dest_dir"
}

# Process STL files
process_stl_files() {
    local source="$1"
    local project="$2"
    local count=0
    local valid_count=0
    local invalid_count=0
    
    log_info "Processing STL files..."
    
    while IFS= read -r -d '' file; do
        ((count++))
        local filename=$(basename "$file")
        
        # Validate STL file
        if validate_stl "$file"; then
            ((valid_count++))
            
            # Detect type and copy to appropriate directory
            local model_type=$(detect_3d_type "$filename")
            
            case "$model_type" in
                case)
                    copy_with_validation "$file" "${PCB_ROOT}/3d-models/cases/${project}/stl"
                    ;;
                plate)
                    copy_with_validation "$file" "${PCB_ROOT}/3d-models/plates/${project}"
                    ;;
                cradle)
                    copy_with_validation "$file" "${PCB_ROOT}/3d-models/accessories/component-cradles/${project}"
                    ;;
                cover)
                    copy_with_validation "$file" "${PCB_ROOT}/3d-models/accessories/covers/${project}"
                    ;;
            esac
        else
            ((invalid_count++))
            log_warn "Skipping invalid STL file: $filename"
        fi
    done < <(find "$source" -type f -iname "*.stl" ! -path '*/.git/*' -print0)
    
    log_info "STL files processed: $count total, $valid_count valid, $invalid_count invalid"
}

# Process STEP files
process_step_files() {
    local source="$1"
    local project="$2"
    local count=0
    
    log_info "Processing STEP files..."
    
    while IFS= read -r -d '' file; do
        ((count++))
        local filename=$(basename "$file")
        
        # Detect type and copy to appropriate directory
        local model_type=$(detect_3d_type "$filename")
        
        case "$model_type" in
            case)
                copy_with_validation "$file" "${PCB_ROOT}/3d-models/cases/${project}/step"
                ;;
            plate)
                copy_with_validation "$file" "${PCB_ROOT}/3d-models/plates/${project}"
                ;;
            cradle)
                copy_with_validation "$file" "${PCB_ROOT}/3d-models/accessories/component-cradles/${project}"
                ;;
            cover)
                copy_with_validation "$file" "${PCB_ROOT}/3d-models/accessories/covers/${project}"
                ;;
        esac
    done < <(find "$source" -type f \( -iname "*.step" -o -iname "*.stp" \) ! -path '*/.git/*' -print0)
    
    log_info "STEP files processed: $count"
}

# Process DXF and CAD files
process_cad_files() {
    local source="$1"
    local project="$2"
    local count=0
    
    log_info "Processing CAD drawing files..."
    
    while IFS= read -r -d '' file; do
        ((count++))
        local filename=$(basename "$file")
        
        # Detect type and copy to appropriate directory
        local cad_type=$(detect_cad_type "$filename")
        
        case "$cad_type" in
            plate)
                copy_with_validation "$file" "${PCB_ROOT}/cad-drawings/plates/${project}"
                ;;
            case)
                copy_with_validation "$file" "${PCB_ROOT}/cad-drawings/cases/${project}"
                ;;
            cover)
                copy_with_validation "$file" "${PCB_ROOT}/cad-drawings/covers/${project}"
                ;;
        esac
    done < <(find "$source" -type f \( -iname "*.dxf" -o -iname "*.svg" -o -iname "*.dwg" \) ! -path '*/.git/*' -print0)
    
    log_info "CAD drawing files processed: $count"
}

# Generate project-specific 3D model inventory
generate_inventory() {
    local project="$1"
    local inventory_file="${PCB_ROOT}/3d-models/cases/${project}/README.md"
    
    log_info "Generating 3D model inventory for $project..."
    
    cat > "$inventory_file" << EOF
# 3D Models - ${project}

## Overview

This directory contains 3D models and CAD drawings for the ${project} keyboard project.

## Available Files

### STL Files (3D Printing)

EOF
    
    # List STL files
    if [ -d "${PCB_ROOT}/3d-models/cases/${project}/stl" ]; then
        local stl_count=$(find "${PCB_ROOT}/3d-models/cases/${project}/stl" -name "*.stl" | wc -l | tr -d ' ')
        if [ "$stl_count" -gt 0 ]; then
            echo "**Case STL Files:** $stl_count file(s)" >> "$inventory_file"
            echo "" >> "$inventory_file"
            find "${PCB_ROOT}/3d-models/cases/${project}/stl" -name "*.stl" -exec basename {} \; | sort | while read -r file; do
                echo "- \`$file\`" >> "$inventory_file"
            done
            echo "" >> "$inventory_file"
        fi
    fi
    
    # List STEP files
    cat >> "$inventory_file" << EOF

### STEP Files (CAD Editing)

EOF
    
    if [ -d "${PCB_ROOT}/3d-models/cases/${project}/step" ]; then
        local step_count=$(find "${PCB_ROOT}/3d-models/cases/${project}/step" \( -name "*.step" -o -name "*.stp" \) | wc -l | tr -d ' ')
        if [ "$step_count" -gt 0 ]; then
            echo "**Case STEP Files:** $step_count file(s)" >> "$inventory_file"
            echo "" >> "$inventory_file"
            find "${PCB_ROOT}/3d-models/cases/${project}/step" \( -name "*.step" -o -name "*.stp" \) -exec basename {} \; | sort | while read -r file; do
                echo "- \`$file\`" >> "$inventory_file"
            done
            echo "" >> "$inventory_file"
        fi
    fi
    
    # Add usage notes
    cat >> "$inventory_file" << EOF

## Usage Notes

### 3D Printing (STL Files)

- **Material:** PLA, PETG, or ABS recommended
- **Layer Height:** 0.2mm standard, 0.1mm for fine details
- **Infill:** 20-30% for structural parts
- **Supports:** May be required depending on geometry
- **Orientation:** Check for optimal print orientation

### CAD Editing (STEP Files)

- STEP files can be imported into most CAD software (FreeCAD, Fusion 360, SolidWorks, etc.)
- Use for modifications, measurements, or creating custom variants
- Maintain original file as reference when making changes

## Related Files

- **Plates:** See \`../../plates/${project}/\`
- **Accessories:** See \`../../accessories/\`
- **CAD Drawings:** See \`../../../cad-drawings/\`
- **PCB Files:** See \`../../../gerbers/${project}/\`

## Source

Original files from the ${project} repository.
See main documentation for license and attribution information.

EOF
    
    log_info "Inventory generated: $inventory_file"
}

# Main execution
create_3d_dirs "$PROJECT_NAME"
process_stl_files "$SOURCE_DIR" "$PROJECT_NAME"
process_step_files "$SOURCE_DIR" "$PROJECT_NAME"
process_cad_files "$SOURCE_DIR" "$PROJECT_NAME"
generate_inventory "$PROJECT_NAME"

log_info "3D model organization complete for project: $PROJECT_NAME"

exit 0
