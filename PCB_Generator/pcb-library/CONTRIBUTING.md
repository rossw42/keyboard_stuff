# Contributing to Through-Hole Keyboard Library

Thank you for your interest in contributing! This document provides guidelines for contributing to the Through-Hole Keyboard PCB Design Resource Library.

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Adding New Projects](#adding-new-projects)
3. [Improving Documentation](#improving-documentation)
4. [Updating Files](#updating-files)
5. [Contribution Guidelines](#contribution-guidelines)
6. [Submission Process](#submission-process)
7. [Code of Conduct](#code-of-conduct)

---

## Ways to Contribute

We welcome various types of contributions:

### High Priority
- Missing BOMs for existing projects
- Build guides with photos and detailed steps
- Tested component alternatives and substitutions
- Regional sourcing information (vendors, part numbers)
- Firmware configuration examples and guides

### Medium Priority
- Additional 3D printable cases and accessories
- Plate design variations (different materials, layouts)
- Design templates for new layouts
- Translation of documentation to other languages
- Design pattern documentation

### Low Priority
- Aesthetic improvements to documentation
- Minor documentation tweaks and clarifications
- Link updates and maintenance

---

## Adding New Projects

### Eligibility Requirements

Before suggesting a project, ensure it meets these criteria:

1. **Through-Hole Focus:**
   - Must use primarily through-hole components
   - Some SMD components acceptable (USB connectors, etc.)
   - MCU should be through-hole or socketed (DIP, Pro Micro)

2. **Open Source:**
   - Must have open-source license
   - Acceptable licenses: MIT, GPL, CC-BY-SA, CERN OHL
   - License must allow redistribution

3. **Publicly Available:**
   - Design files must be publicly accessible
   - Repository should be active or archived (not deleted)
   - Files should be complete and buildable

4. **Buildable Design:**
   - Not just concept or render
   - Should have been built successfully
   - Components should be sourceable

### Information to Gather

When proposing a new project, collect:

**Basic Information:**
- Project name
- Repository URL
- License type
- Creator/maintainer name
- Latest revision/version

**Technical Details:**
- Layout (60%, 65%, TKL, 40%, macropad, etc.)
- Form factor and dimensions
- MCU type (ATmega328P, ATmega32A, Pro Micro, etc.)
- USB connector type
- Key count

**Available Files:**
- [ ] Gerber files (PCB)
- [ ] Gerber files (plate)
- [ ] KiCad design files
- [ ] Eagle design files
- [ ] BOM (Bill of Materials)
- [ ] Build guide
- [ ] 3D models (STL, STEP)
- [ ] CAD drawings (DXF, SVG)
- [ ] Firmware configuration

**Firmware Support:**
- QMK support (yes/no, keyboard path)
- VIA support (yes/no)
- VIAL support (yes/no)
- ZMK support (yes/no, for wireless)

**Special Features:**
- Rotary encoders
- OLED display
- RGB/LED support
- Wireless capability
- Hotswap sockets
- Split keyboard
- Other unique features

### Submission Method

**Option 1: GitHub Issue**
1. Open a new issue
2. Use "New Project Suggestion" template
3. Fill in all required information
4. Include links to files
5. Add any special notes

**Option 2: Pull Request**
1. Fork the repository
2. Add project files to appropriate directories
3. Update documentation (catalogs, indexes)
4. Submit pull request with description

---

## Improving Documentation

### Types of Documentation Improvements

**Build Guides:**
- Add missing steps or clarifications
- Include photos of assembly process
- Document common mistakes and solutions
- Add troubleshooting sections
- Improve formatting and readability

**Technical Documentation:**
- Fix errors or outdated information
- Add missing specifications
- Clarify technical details
- Add diagrams or illustrations
- Cross-reference related documents

**Component Information:**
- Add alternative part numbers
- Update vendor information
- Add regional sourcing options
- Document component substitutions
- Include datasheets or specifications

**Translations:**
- Translate existing documentation
- Maintain formatting and structure
- Keep technical terms consistent
- Note translation date and version

### Documentation Standards

**Markdown Format:**
- Use standard Markdown syntax
- Include table of contents for long documents
- Use headers hierarchically (H1 → H2 → H3)
- Add code blocks for commands or code
- Use tables for structured data

**Writing Style:**
- Clear and concise language
- Step-by-step instructions
- Active voice preferred
- Define technical terms
- Include examples where helpful

**Images:**
- Use descriptive filenames
- Compress to reasonable size (< 500KB)
- Use PNG for screenshots, JPG for photos
- Include alt text for accessibility
- Store in appropriate directory

**Links:**
- Use relative links for internal documents
- Use absolute URLs for external resources
- Check links work before submitting
- Update broken links when found

---

## Updating Files

### File Types to Update

**Gerber Files:**
- New PCB revisions
- Corrected manufacturing files
- Alternative plate designs
- Updated board outlines

**Design Files:**
- New KiCad/Eagle versions
- Fixed schematics or layouts
- Updated component libraries
- Improved routing or placement

**3D Models:**
- New case designs
- Improved printability
- Alternative mounting options
- Accessory designs

**CAD Drawings:**
- Updated plate DXF files
- New case layer designs
- Corrected dimensions
- Alternative layouts

**BOMs:**
- Updated part numbers
- Alternative components
- Regional vendor information
- Corrected quantities

**Firmware:**
- New QMK configurations
- VIA/VIAL support files
- Updated keymaps
- Flashing instructions

### File Verification

Before submitting updated files:

1. **Verify Source:**
   - Confirm files are from official repository
   - Check file modification dates
   - Verify version/revision numbers
   - Compare with previous version

2. **Test Files:**
   - Open design files in appropriate software
   - Verify Gerber files with viewer
   - Check 3D models for errors
   - Test firmware if possible

3. **Document Changes:**
   - Note what was updated and why
   - Include version numbers
   - Reference original source
   - Add any warnings or notes

---

## Contribution Guidelines

### File Organization

**Directory Structure:**
```
PCB/
├── gerbers/[project-name]/
│   ├── pcb/
│   └── plate/
├── design-files/[project-name]/
│   ├── kicad/
│   ├── eagle/
│   └── libraries/
├── 3d-models/
│   ├── cases/[project-name]/
│   ├── plates/[project-name]/
│   └── accessories/
├── cad-drawings/
│   ├── plates/[project-name]/
│   ├── cases/[project-name]/
│   └── covers/
├── boms/[project-name]/
├── docs/build-guides/[project-name]/
└── firmware/
    ├── qmk-configs/[project-name]/
    └── flashing-guides/[mcu-type]/
```

**Naming Conventions:**
- Use lowercase with hyphens: `plaid-pad`, `kbic65`
- Be consistent across all directories
- Use descriptive filenames
- Include version numbers when applicable

**File Formats:**
- Gerbers: ZIP archive
- Design files: Native format + ZIP backup
- 3D models: STL (printing), STEP (CAD)
- CAD drawings: DXF (preferred), SVG (acceptable)
- Documentation: Markdown (preferred), PDF (complex layouts)
- BOMs: CSV format

### Documentation Requirements

**Project README:**
Each project directory should include README.md with:
- Project name and description
- Original repository link
- License information
- Build difficulty level
- Special requirements or notes
- Known issues or limitations

**Build Guides:**
Should include:
- Required tools and materials
- Component list with quantities
- Step-by-step assembly instructions
- Photos or diagrams
- Troubleshooting section
- Firmware flashing instructions

**BOMs:**
Should include columns:
- Component name/description
- Value/specification
- Footprint/package
- Quantity
- Vendor part numbers
- Notes or alternatives

### Quality Standards

**Completeness:**
- Include all necessary files
- Don't omit critical information
- Provide context and explanations
- Link to additional resources

**Accuracy:**
- Verify technical information
- Test instructions when possible
- Double-check part numbers
- Confirm compatibility

**Clarity:**
- Use clear, simple language
- Define technical terms
- Provide examples
- Include visual aids

**Attribution:**
- Credit original creators
- Link to source repositories
- Respect licenses
- Acknowledge contributors

---

## Submission Process

### Step-by-Step Guide

1. **Prepare Your Contribution**
   - Gather all necessary files
   - Organize according to directory structure
   - Write or update documentation
   - Test everything works

2. **Fork Repository** (if using pull request)
   - Fork on GitHub
   - Clone to local machine
   - Create new branch for your changes
   - Use descriptive branch name

3. **Make Changes**
   - Add or update files
   - Follow naming conventions
   - Update catalogs and indexes
   - Write clear commit messages

4. **Test Locally**
   - Verify file integrity
   - Check links work
   - Preview Markdown rendering
   - Ensure nothing is broken

5. **Submit Contribution**
   - Push changes to your fork
   - Create pull request
   - Fill in PR template
   - Provide clear description

6. **Respond to Feedback**
   - Monitor PR for comments
   - Make requested changes
   - Answer questions
   - Be patient and respectful

### Pull Request Guidelines

**Title:**
- Clear and descriptive
- Include project name if applicable
- Use action verbs (Add, Update, Fix)

**Description:**
- Explain what was changed and why
- Reference related issues
- List files added/modified
- Note any breaking changes

**Checklist:**
- [ ] Files organized correctly
- [ ] Documentation updated
- [ ] Catalogs/indexes updated
- [ ] Links verified
- [ ] Commit messages clear
- [ ] No unnecessary files included
- [ ] License information included
- [ ] Original creators credited

### Review Process

**What to Expect:**
1. Initial review within 1-2 weeks
2. Feedback or questions from maintainers
3. Possible requests for changes
4. Approval and merge
5. Acknowledgment in changelog

**Common Feedback:**
- File organization issues
- Missing documentation
- Incomplete information
- Formatting problems
- License concerns

---

## Code of Conduct

### Our Standards

**Be Respectful:**
- Treat everyone with respect
- Welcome diverse perspectives
- Be patient with newcomers
- Assume good intentions

**Be Constructive:**
- Provide helpful feedback
- Suggest improvements
- Share knowledge
- Help others learn

**Be Honest:**
- Give credit where due
- Admit mistakes
- Correct errors promptly
- Be transparent

**Be Responsible:**
- Respect licenses
- Verify information
- Test contributions
- Follow guidelines

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Publishing others' private information
- Plagiarism or license violations
- Spam or off-topic content

### Enforcement

Violations of code of conduct may result in:
1. Warning from maintainers
2. Temporary ban from contributing
3. Permanent ban from project

Report violations to project maintainers.

---

## Getting Help

### Questions About Contributing

**Before Asking:**
- Read this guide thoroughly
- Check existing issues and PRs
- Review similar contributions
- Search documentation

**Where to Ask:**
- Open a GitHub issue with "Question" label
- Check project discussions
- Review FAQ in documentation

### Technical Questions

**Project-Specific:**
- Refer to original repository
- Check project build guide
- Review project documentation

**General Through-Hole Keyboards:**
- r/MechanicalKeyboards on Reddit
- 40% Keyboards Discord
- QMK Discord
- Keyboard design forums

---

## Recognition

### Contributors

All contributors will be:
- Listed in project acknowledgments
- Credited in relevant documentation
- Mentioned in changelog for significant contributions
- Thanked publicly for their help

### Types of Contributions Recognized

- Code and file contributions
- Documentation improvements
- Bug reports and fixes
- Feature suggestions
- Community support
- Translations
- Testing and verification

---

## Additional Resources

### For New Contributors

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

### For Keyboard Designers

- [KiCad Documentation](https://docs.kicad.org/)
- [QMK Documentation](https://docs.qmk.fm/)
- [PCB Design Guide](docs/design_patterns.md)
- [GH60 Specifications](docs/gh60_pcb_specifications.md)

### For Builders

- [Manufacturing Guide](docs/manufacturing_guide.md)
- [Component Sourcing Guide](docs/component_sourcing_guide.md)
- [Build Guides](docs/build-guides/)

---

## Contact

**Project Maintainers:**
- See repository contributors list
- Open GitHub issue for questions
- Check project discussions

**Original Project Creators:**
- Refer to individual project repositories
- Links in [PROJECT_CATALOG.md](PROJECT_CATALOG.md)
- Credits in [docs/repository_inventory.md](docs/repository_inventory.md)

---

**Thank you for contributing to the Through-Hole Keyboard Library!**

Your contributions help the mechanical keyboard community build amazing custom keyboards with through-hole components.
