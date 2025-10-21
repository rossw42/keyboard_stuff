#!/usr/bin/env bash

# Metadata Extraction Script
# Extracts project information, license, and file inventory
# Usage: ./extract_metadata.sh <project-name> <github-url>

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

# Validate inputs
if [ $# -ne 2 ]; then
    log_error "Usage: $0 <project-name> <github-url>"
    log_error "Example: $0 discipline https://github.com/coseyfannitutti/discipline"
    exit 1
fi

PROJECT_NAME="$1"
REPO_URL="$2"
SOURCE_DIR="${TEMP_DIR}/${PROJECT_NAME}"

# Validate source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    log_error "Source directory not found: $SOURCE_DIR"
    log_error "Please run collect_repository.sh first"
    exit 1
fi

log_info "Extracting metadata for project: $PROJECT_NAME"

# Extract project description from README
extract_description() {
    local readme_file=""
    
    # Find README file (case-insensitive)
    for file in "$SOURCE_DIR"/README* "$SOURCE_DIR"/readme* "$SOURCE_DIR"/Readme*; do
        if [ -f "$file" ]; then
            readme_file="$file"
            break
        fi
    done
    
    if [ -z "$readme_file" ]; then
        echo "No description available"
        return
    fi
    
    # Extract first paragraph or heading
    local description=""
    
    # Try to get first heading (# Title)
    description=$(grep -m 1 "^# " "$readme_file" 2>/dev/null | sed 's/^# //' || echo "")
    
    # If no heading, try first non-empty line
    if [ -z "$description" ]; then
        description=$(grep -v "^$" "$readme_file" 2>/dev/null | head -n 1 || echo "")
    fi
    
    # Clean up description
    description=$(echo "$description" | sed 's/[*_`]//g' | tr -d '\r' | head -c 200)
    
    if [ -z "$description" ]; then
        echo "No description available"
    else
        echo "$description"
    fi
}

# Extract license information
extract_license() {
    local license_file=""
    
    # Find LICENSE file (case-insensitive)
    for file in "$SOURCE_DIR"/LICENSE* "$SOURCE_DIR"/license* "$SOURCE_DIR"/License* "$SOURCE_DIR"/COPYING*; do
        if [ -f "$file" ]; then
            license_file="$file"
            break
        fi
    done
    
    if [ -z "$license_file" ]; then
        echo "Unknown"
        return
    fi
    
    # Detect common licenses
    local content=$(cat "$license_file" | tr '[:upper:]' '[:lower:]')
    
    if echo "$content" | grep -q "mit license"; then
        echo "MIT"
    elif echo "$content" | grep -q "apache license"; then
        echo "Apache 2.0"
    elif echo "$content" | grep -q "gnu general public license"; then
        if echo "$content" | grep -q "version 3"; then
            echo "GPL-3.0"
        elif echo "$content" | grep -q "version 2"; then
            echo "GPL-2.0"
        else
            echo "GPL"
        fi
    elif echo "$content" | grep -q "bsd.*clause"; then
        if echo "$content" | grep -q "3-clause"; then
            echo "BSD-3-Clause"
        elif echo "$content" | grep -q "2-clause"; then
            echo "BSD-2-Clause"
        else
            echo "BSD"
        fi
    elif echo "$content" | grep -q "creative commons"; then
        echo "CC (Creative Commons)"
    elif echo "$content" | grep -q "cern"; then
        echo "CERN OHL"
    else
        echo "Custom/Other"
    fi
}

# Detect layout type from README or file structure
detect_layout() {
    local readme_file=""
    
    for file in "$SOURCE_DIR"/README* "$SOURCE_DIR"/readme*; do
        if [ -f "$file" ]; then
            readme_file="$file"
            break
        fi
    done
    
    if [ -n "$readme_file" ]; then
        local content=$(cat "$readme_file" | tr '[:upper:]' '[:lower:]')
        
        if echo "$content" | grep -qE "(60%|60 percent|sixty percent)"; then
            echo "60%"
        elif echo "$content" | grep -qE "(65%|65 percent|sixty.?five percent)"; then
            echo "65%"
        elif echo "$content" | grep -qE "(tkl|tenkeyless|80%)"; then
            echo "TKL"
        elif echo "$content" | grep -qE "(40%|40 percent|forty percent)"; then
            echo "40%"
        elif echo "$content" | grep -qE "(macropad|numpad|pad)"; then
            echo "Macropad"
        elif echo "$content" | grep -qE "(ortho|ortholinear)"; then
            echo "Ortholinear"
        elif echo "$content" | grep -qE "(split)"; then
            echo "Split"
        else
            echo "Unknown"
        fi
    else
        echo "Unknown"
    fi
}

# Detect MCU type
detect_mcu() {
    local readme_file=""
    
    for file in "$SOURCE_DIR"/README* "$SOURCE_DIR"/readme*; do
        if [ -f "$file" ]; then
            readme_file="$file"
            break
        fi
    done
    
    if [ -n "$readme_file" ]; then
        local content=$(cat "$readme_file")
        
        if echo "$content" | grep -qiE "atmega32a"; then
            echo "ATmega32A"
        elif echo "$content" | grep -qiE "atmega32u4"; then
            echo "ATmega32U4"
        elif echo "$content" | grep -qiE "atmega328p?"; then
            echo "ATmega328P"
        elif echo "$content" | grep -qiE "pro.?micro"; then
            echo "Pro Micro"
        elif echo "$content" | grep -qiE "elite.?c"; then
            echo "Elite-C"
        elif echo "$content" | grep -qiE "rp2040"; then
            echo "RP2040"
        else
            echo "Unknown"
        fi
    else
        echo "Unknown"
    fi
}

# Detect USB connector type
detect_usb() {
    local readme_file=""
    
    for file in "$SOURCE_DIR"/README* "$SOURCE_DIR"/readme*; do
        if [ -f "$file" ]; then
            readme_file="$file"
            break
        fi
    done
    
    if [ -n "$readme_file" ]; then
        local content=$(cat "$readme_file")
        
        if echo "$content" | grep -qiE "usb.?c|usb type.?c"; then
            echo "USB-C"
        elif echo "$content" | grep -qiE "usb.?mini|mini.?usb"; then
            echo "USB Mini"
        elif echo "$content" | grep -qiE "usb.?micro|micro.?usb"; then
            echo "USB Micro"
        else
            echo "Unknown"
        fi
    else
        echo "Unknown"
    fi
}

# Check for firmware support
check_firmware_support() {
    local firmware_type="$1"
    
    # Check for QMK
    if [ "$firmware_type" == "qmk" ]; then
        if [ -d "$SOURCE_DIR/qmk" ] || [ -d "$SOURCE_DIR/firmware" ] || [ -f "$SOURCE_DIR/rules.mk" ]; then
            echo "Yes"
        else
            echo "Unknown"
        fi
    fi
    
    # Check for VIA
    if [ "$firmware_type" == "via" ]; then
        if find "$SOURCE_DIR" -name "*via*" -o -name "*VIA*" 2>/dev/null | grep -q .; then
            echo "Yes"
        else
            echo "Unknown"
        fi
    fi
    
    # Check for VIAL
    if [ "$firmware_type" == "vial" ]; then
        if find "$SOURCE_DIR" -name "*vial*" -o -name "*VIAL*" 2>/dev/null | grep -q .; then
            echo "Yes"
        else
            echo "Unknown"
        fi
    fi
}

# Check for available file types
check_file_availability() {
    local file_type="$1"
    local project="$2"
    
    case "$file_type" in
        gerber)
            if [ -n "$(find "${PCB_ROOT}/gerbers/${project}" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
        design)
            if [ -n "$(find "${PCB_ROOT}/design-files/${project}" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
        bom)
            if [ -n "$(find "${PCB_ROOT}/boms/${project}" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
        doc)
            if [ -n "$(find "${PCB_ROOT}/docs/build-guides/${project}" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
        3d)
            if [ -n "$(find "${PCB_ROOT}/3d-models" -path "*/${project}/*" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
        dxf)
            if [ -n "$(find "${PCB_ROOT}/cad-drawings" -path "*/${project}/*" -type f 2>/dev/null)" ]; then
                echo "✅"
            else
                echo "❌"
            fi
            ;;
    esac
}

# Extract special features
extract_features() {
    local readme_file=""
    
    for file in "$SOURCE_DIR"/README* "$SOURCE_DIR"/readme*; do
        if [ -f "$file" ]; then
            readme_file="$file"
            break
        fi
    done
    
    if [ -z "$readme_file" ]; then
        echo "None documented"
        return
    fi
    
    local features=()
    local content=$(cat "$readme_file" | tr '[:upper:]' '[:lower:]')
    
    if echo "$content" | grep -qE "(rotary encoder|encoder)"; then
        features+=("Rotary encoder")
    fi
    
    if echo "$content" | grep -qE "(oled|display)"; then
        features+=("OLED display")
    fi
    
    if echo "$content" | grep -qE "(rgb|led|backlight)"; then
        features+=("RGB/LED")
    fi
    
    if echo "$content" | grep -qE "(hot.?swap|hotswap)"; then
        features+=("Hot-swap")
    fi
    
    if echo "$content" | grep -qE "(wireless|bluetooth)"; then
        features+=("Wireless")
    fi
    
    if [ ${#features[@]} -eq 0 ]; then
        echo "None documented"
    else
        printf "%s, " "${features[@]}" | sed 's/, $//'
    fi
}

# Get git revision info
get_revision() {
    cd "$SOURCE_DIR"
    local commit_hash=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local commit_date=$(git log -1 --format=%cd --date=short 2>/dev/null || echo "unknown")
    echo "$commit_hash ($commit_date)"
}

# Generate project README
generate_project_readme() {
    local project="$1"
    local repo_url="$2"
    local output_file="${PCB_ROOT}/docs/build-guides/${project}/README.md"
    
    mkdir -p "$(dirname "$output_file")"
    
    log_info "Generating project README: $output_file"
    
    # Extract metadata
    local description=$(extract_description)
    local license=$(extract_license)
    local layout=$(detect_layout)
    local mcu=$(detect_mcu)
    local usb=$(detect_usb)
    local qmk=$(check_firmware_support "qmk")
    local via=$(check_firmware_support "via")
    local vial=$(check_firmware_support "vial")
    local features=$(extract_features)
    local revision=$(get_revision)
    
    # Check file availability
    local has_gerber=$(check_file_availability "gerber" "$project")
    local has_design=$(check_file_availability "design" "$project")
    local has_bom=$(check_file_availability "bom" "$project")
    local has_doc=$(check_file_availability "doc" "$project")
    local has_3d=$(check_file_availability "3d" "$project")
    local has_dxf=$(check_file_availability "dxf" "$project")
    
    # Generate README content
    # Capitalize first letter of project name
    local project_title="$(echo "${project:0:1}" | tr '[:lower:]' '[:upper:]')${project:1}"
    
    cat > "$output_file" << EOF
# ${project_title}

## Project Information

**Description:** $description

**Repository:** $repo_url

**Layout:** $layout

**MCU:** $mcu

**USB Connector:** $usb

**License:** $license

**Revision:** $revision

## Available Files

- $has_gerber Gerber files
- $has_design KiCad/Eagle design files
- $has_bom Bill of Materials (BOM)
- $has_doc Build guide / Documentation
- $has_3d 3D models (STL/STEP)
- $has_dxf CAD drawings (DXF)

## Firmware Support

- **QMK:** $qmk
- **VIA:** $via
- **VIAL:** $vial

## Special Features

$features

## File Locations

### Manufacturing Files
- **Gerber files:** \`gerbers/${project}/\`
- **BOM:** \`boms/${project}/\`

### Design Files
- **Source files:** \`design-files/${project}/\`
- **Libraries:** \`design-files/${project}/libraries/\`

### 3D Models & Drawings
- **3D models:** \`3d-models/cases/${project}/\` and \`3d-models/plates/${project}/\`
- **CAD drawings:** \`cad-drawings/plates/${project}/\` and \`cad-drawings/cases/${project}/\`

### Firmware
- **QMK configs:** \`firmware/qmk-configs/${project}/\`
- **Flashing guides:** \`firmware/flashing-guides/\`

## Notes

This project was collected from the original repository on $(date +%Y-%m-%d).

For the latest updates and issues, please refer to the original repository.

## Attribution

Original project by the repository maintainers. Please respect the project license when using these files.

EOF

    log_info "Project README generated successfully"
}

# Update repository inventory
update_inventory() {
    local project="$1"
    local repo_url="$2"
    local inventory_file="${PCB_ROOT}/docs/repository_inventory.md"
    
    log_info "Updating repository inventory..."
    
    # Create inventory file if it doesn't exist
    if [ ! -f "$inventory_file" ]; then
        cat > "$inventory_file" << EOF
# Through-Hole Keyboard Repository Inventory

This document catalogs all through-hole keyboard projects collected in this library.

## Projects

EOF
    fi
    
    # Extract metadata
    local description=$(extract_description)
    local license=$(extract_license)
    local layout=$(detect_layout)
    local mcu=$(detect_mcu)
    local usb=$(detect_usb)
    local qmk=$(check_firmware_support "qmk")
    local via=$(check_firmware_support "via")
    local vial=$(check_firmware_support "vial")
    local features=$(extract_features)
    local revision=$(get_revision)
    
    # Check file availability
    local has_gerber=$(check_file_availability "gerber" "$project")
    local has_design=$(check_file_availability "design" "$project")
    local has_bom=$(check_file_availability "bom" "$project")
    local has_doc=$(check_file_availability "doc" "$project")
    local has_3d=$(check_file_availability "3d" "$project")
    local has_dxf=$(check_file_availability "dxf" "$project")
    
    # Capitalize first letter of project name
    local project_title="$(echo "${project:0:1}" | tr '[:lower:]' '[:upper:]')${project:1}"
    
    # Check if project already exists in inventory
    if grep -q "^## ${project_title}" "$inventory_file"; then
        log_warn "Project already exists in inventory, skipping..."
        return
    fi
    
    # Append project entry
    cat >> "$inventory_file" << EOF

## ${project_title}

- **Repository:** $repo_url
- **Layout:** $layout
- **MCU:** $mcu
- **USB:** $usb
- **Available Files:**
  - $has_gerber Gerber files
  - $has_design KiCad/Eagle files
  - $has_bom BOM
  - $has_doc Build guide
  - $has_3d 3D models
  - $has_dxf DXF drawings
- **QMK Support:** $qmk
- **VIA/VIAL Support:** $via / $vial
- **License:** $license
- **Special Features:** $features
- **Revision:** $revision

EOF

    log_info "Repository inventory updated"
}

# Main execution
generate_project_readme "$PROJECT_NAME" "$REPO_URL"
update_inventory "$PROJECT_NAME" "$REPO_URL"

log_info "Metadata extraction complete for project: $PROJECT_NAME"
log_info "Project README: docs/build-guides/${PROJECT_NAME}/README.md"
log_info "Repository inventory: docs/repository_inventory.md"

exit 0
