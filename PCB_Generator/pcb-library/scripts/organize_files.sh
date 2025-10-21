#!/usr/bin/env bash

# File Organization Script
# Detects file types and organizes them into appropriate directories
# Usage: ./organize_files.sh <project-name>

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

log_info "Organizing files for project: $PROJECT_NAME"

# Create project-specific directories
create_project_dirs() {
    local project="$1"
    
    log_info "Creating directory structure for $project..."
    
    mkdir -p "${PCB_ROOT}/gerbers/${project}/pcb"
    mkdir -p "${PCB_ROOT}/gerbers/${project}/plate"
    mkdir -p "${PCB_ROOT}/design-files/${project}/kicad"
    mkdir -p "${PCB_ROOT}/design-files/${project}/eagle"
    mkdir -p "${PCB_ROOT}/design-files/${project}/libraries"
    mkdir -p "${PCB_ROOT}/3d-models/cases/${project}/stl"
    mkdir -p "${PCB_ROOT}/3d-models/cases/${project}/step"
    mkdir -p "${PCB_ROOT}/3d-models/plates/${project}"
    mkdir -p "${PCB_ROOT}/3d-models/accessories/component-cradles/${project}"
    mkdir -p "${PCB_ROOT}/3d-models/accessories/covers/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/plates/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/cases/${project}"
    mkdir -p "${PCB_ROOT}/cad-drawings/covers/${project}"
    mkdir -p "${PCB_ROOT}/boms/${project}"
    mkdir -p "${PCB_ROOT}/docs/build-guides/${project}"
    mkdir -p "${PCB_ROOT}/firmware/qmk-configs/${project}"
    mkdir -p "${PCB_ROOT}/firmware/flashing-guides"
}

# Detect file type based on extension and content
detect_file_type() {
    local file="$1"
    local filename=$(basename "$file")
    local extension="${filename##*.}"
    local lowercase_ext=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
    local lowercase_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    
    # Gerber files (various extensions)
    if [[ "$lowercase_ext" =~ ^(gbr|gbl|gbo|gbs|gko|gtl|gto|gts|gtp|gm1|gm2|gm3|g[0-9]+|drl|xln|txt)$ ]]; then
        # Check if it's a drill file
        if [[ "$lowercase_name" =~ (drill|drl|xln) ]]; then
            echo "gerber"
        # Check if it's likely a plate file
        elif [[ "$lowercase_name" =~ (plate|switch) ]]; then
            echo "gerber-plate"
        else
            echo "gerber"
        fi
        return
    fi
    
    # Gerber ZIP archives
    if [[ "$lowercase_ext" == "zip" ]] && [[ "$lowercase_name" =~ (gerber|pcb|plate) ]]; then
        if [[ "$lowercase_name" =~ plate ]]; then
            echo "gerber-plate-zip"
        else
            echo "gerber-zip"
        fi
        return
    fi
    
    # KiCad files
    if [[ "$lowercase_ext" =~ ^(kicad_pcb|kicad_sch|kicad_pro|kicad_prl|kicad_mod|lib|dcm|sch|pro)$ ]]; then
        echo "kicad"
        return
    fi
    
    # Eagle files
    if [[ "$lowercase_ext" =~ ^(brd|sch)$ ]]; then
        # Check if it's actually Eagle (not KiCad .sch)
        if grep -q "eagle" "$file" 2>/dev/null || grep -q "EAGLE" "$file" 2>/dev/null; then
            echo "eagle"
            return
        fi
    fi
    
    # 3D model files
    if [[ "$lowercase_ext" =~ ^(stl|step|stp)$ ]]; then
        if [[ "$lowercase_ext" == "stl" ]]; then
            if [[ "$lowercase_name" =~ (case|housing|enclosure) ]]; then
                echo "stl-case"
            elif [[ "$lowercase_name" =~ (plate|switch) ]]; then
                echo "stl-plate"
            elif [[ "$lowercase_name" =~ (cradle|holder|support) ]]; then
                echo "stl-accessory"
            elif [[ "$lowercase_name" =~ (cover|lid|top|bottom) ]]; then
                echo "stl-cover"
            else
                echo "stl-case"  # Default to case
            fi
        else
            echo "step-case"
        fi
        return
    fi
    
    # CAD drawing files
    if [[ "$lowercase_ext" =~ ^(dxf|svg|dwg)$ ]]; then
        if [[ "$lowercase_name" =~ (plate|switch) ]]; then
            echo "dxf-plate"
        elif [[ "$lowercase_name" =~ (case|housing) ]]; then
            echo "dxf-case"
        elif [[ "$lowercase_name" =~ (cover|lid) ]]; then
            echo "dxf-cover"
        else
            echo "dxf-plate"  # Default to plate
        fi
        return
    fi
    
    # BOM files
    if [[ "$lowercase_name" =~ ^(bom|bill.*material|parts.*list) ]] || [[ "$lowercase_ext" == "csv" && "$lowercase_name" =~ (component|part) ]]; then
        echo "bom"
        return
    fi
    
    # Documentation files
    if [[ "$lowercase_ext" =~ ^(md|pdf|txt|html|htm)$ ]]; then
        if [[ "$lowercase_name" =~ ^(readme|build.*guide|assembly|instruction) ]]; then
            echo "doc"
        elif [[ "$lowercase_name" =~ (flash|firmware|program) ]]; then
            echo "firmware-doc"
        elif [[ "$lowercase_name" =~ (license|copying) ]]; then
            echo "license"
        fi
        return
    fi
    
    # Firmware files
    if [[ "$lowercase_name" =~ (keymap|config\.h|rules\.mk) ]] || [[ -d "$file" && "$lowercase_name" =~ (qmk|firmware|keymaps) ]]; then
        echo "firmware"
        return
    fi
    
    # Library files
    if [[ "$lowercase_name" =~ (footprint|symbol|library|\.lib|\.mod) ]]; then
        echo "library"
        return
    fi
    
    # Unknown
    echo "unknown"
}

# Copy file to destination with naming consistency
copy_file() {
    local src="$1"
    local dest_dir="$2"
    local filename=$(basename "$src")
    
    # Ensure destination directory exists
    mkdir -p "$dest_dir"
    
    # Check if file already exists
    if [ -f "${dest_dir}/${filename}" ]; then
        log_warn "File already exists: ${dest_dir}/${filename}"
        # Create backup with timestamp
        local timestamp=$(date +%Y%m%d_%H%M%S)
        local backup="${dest_dir}/${filename}.${timestamp}.bak"
        log_warn "Creating backup: $backup"
        mv "${dest_dir}/${filename}" "$backup"
    fi
    
    # Copy file
    cp "$src" "${dest_dir}/${filename}"
    log_debug "Copied: $filename -> $dest_dir"
}

# Process files in repository
process_files() {
    local source="$1"
    local project="$2"
    
    log_info "Scanning files in $source..."
    
    # Counters
    local gerber_count=0
    local kicad_count=0
    local eagle_count=0
    local stl_count=0
    local dxf_count=0
    local bom_count=0
    local doc_count=0
    local firmware_count=0
    local unknown_count=0
    
    # Find all files (excluding .git directory)
    while IFS= read -r -d '' file; do
        # Skip directories
        [ -f "$file" ] || continue
        
        local file_type=$(detect_file_type "$file")
        
        case "$file_type" in
            gerber)
                copy_file "$file" "${PCB_ROOT}/gerbers/${project}/pcb"
                ((gerber_count++))
                ;;
            gerber-plate)
                copy_file "$file" "${PCB_ROOT}/gerbers/${project}/plate"
                ((gerber_count++))
                ;;
            gerber-zip)
                copy_file "$file" "${PCB_ROOT}/gerbers/${project}/pcb"
                ((gerber_count++))
                ;;
            gerber-plate-zip)
                copy_file "$file" "${PCB_ROOT}/gerbers/${project}/plate"
                ((gerber_count++))
                ;;
            kicad)
                copy_file "$file" "${PCB_ROOT}/design-files/${project}/kicad"
                ((kicad_count++))
                ;;
            eagle)
                copy_file "$file" "${PCB_ROOT}/design-files/${project}/eagle"
                ((eagle_count++))
                ;;
            stl-case)
                copy_file "$file" "${PCB_ROOT}/3d-models/cases/${project}/stl"
                ((stl_count++))
                ;;
            stl-plate)
                copy_file "$file" "${PCB_ROOT}/3d-models/plates/${project}"
                ((stl_count++))
                ;;
            stl-accessory)
                copy_file "$file" "${PCB_ROOT}/3d-models/accessories/component-cradles/${project}"
                ((stl_count++))
                ;;
            stl-cover)
                copy_file "$file" "${PCB_ROOT}/3d-models/accessories/covers/${project}"
                ((stl_count++))
                ;;
            step-case)
                copy_file "$file" "${PCB_ROOT}/3d-models/cases/${project}/step"
                ((stl_count++))
                ;;
            dxf-plate)
                copy_file "$file" "${PCB_ROOT}/cad-drawings/plates/${project}"
                ((dxf_count++))
                ;;
            dxf-case)
                copy_file "$file" "${PCB_ROOT}/cad-drawings/cases/${project}"
                ((dxf_count++))
                ;;
            dxf-cover)
                copy_file "$file" "${PCB_ROOT}/cad-drawings/covers/${project}"
                ((dxf_count++))
                ;;
            bom)
                copy_file "$file" "${PCB_ROOT}/boms/${project}"
                ((bom_count++))
                ;;
            doc)
                copy_file "$file" "${PCB_ROOT}/docs/build-guides/${project}"
                ((doc_count++))
                ;;
            firmware-doc)
                copy_file "$file" "${PCB_ROOT}/firmware/flashing-guides"
                ((firmware_count++))
                ;;
            firmware)
                # Copy firmware directories or files
                if [ -d "$file" ]; then
                    cp -r "$file" "${PCB_ROOT}/firmware/qmk-configs/${project}/"
                else
                    copy_file "$file" "${PCB_ROOT}/firmware/qmk-configs/${project}"
                fi
                ((firmware_count++))
                ;;
            library)
                copy_file "$file" "${PCB_ROOT}/design-files/${project}/libraries"
                ;;
            license)
                copy_file "$file" "${PCB_ROOT}/docs/build-guides/${project}"
                ;;
            unknown)
                ((unknown_count++))
                ;;
        esac
    done < <(find "$source" -type f ! -path '*/.git/*' -print0)
    
    # Print summary
    log_info "File organization complete!"
    log_info "Summary:"
    log_info "  Gerber files: $gerber_count"
    log_info "  KiCad files: $kicad_count"
    log_info "  Eagle files: $eagle_count"
    log_info "  3D models: $stl_count"
    log_info "  CAD drawings: $dxf_count"
    log_info "  BOM files: $bom_count"
    log_info "  Documentation: $doc_count"
    log_info "  Firmware files: $firmware_count"
    log_info "  Unknown/skipped: $unknown_count"
}

# Main execution
create_project_dirs "$PROJECT_NAME"
process_files "$SOURCE_DIR" "$PROJECT_NAME"

log_info "Files organized successfully for project: $PROJECT_NAME"
log_info "Next step: Run metadata extraction script"

exit 0
