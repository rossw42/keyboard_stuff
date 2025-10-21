# PCB Design Guides - Overview

Comprehensive collection of PCB design guides for keyboard projects, integrating best practices from the community.

---

## Available Guides

### 📘 [PCB Design Guide](PCB_DESIGN_GUIDE.md)
**Complete guide for wired keyboard PCB design**

**Topics Covered:**
- Prerequisites (KiCad, libraries, version control)
- Design workflow
- Component selection (MCUs, USB, diodes, switches)
- Circuit design (USB protection, MCU support, switch matrix)
- PCB layout (layer stack, placement, routing)
- Manufacturing (specifications, Gerber export)
- Testing & validation
- Common issues & solutions

**Best For:**
- First-time PCB designers
- Through-hole keyboard projects
- QMK-based designs
- Learning PCB fundamentals

**Based On:**
- ai03's PCB Design Guide
- Community best practices
- Proven through-hole designs

---

### 📻 [Wireless PCB Design Guide](WIRELESS_PCB_DESIGN.md)
**Advanced guide for wireless keyboard PCBs**

**Topics Covered:**
- nRF52840 module selection
- Battery management (TP4056, BQ24075)
- Power switching circuits
- Voltage sensing for battery reporting
- LED underglow with power control
- RF design considerations
- ZMK firmware configuration
- Wireless-specific testing

**Best For:**
- Advanced designers
- Wireless/Bluetooth keyboards
- ZMK firmware projects
- Low-power designs

**Based On:**
- ebastler's ZMK Design Guide v3
- nRF52840 best practices
- Proven wireless implementations

---

### ✅ [PCB Design Checklist](PCB_DESIGN_CHECKLIST.md)
**Step-by-step checklist for PCB projects**

**Sections:**
- Pre-design phase
- Schematic design
- PCB layout
- Pre-manufacturing
- Post-manufacturing
- Common mistakes to avoid

**Best For:**
- Ensuring nothing is missed
- Quality control
- First-time designers
- Project reviews

**Use Case:**
- Print and check off items as you work
- Review before manufacturing
- Catch common mistakes early

---

## Quick Start

### New to PCB Design?
1. Read [PCB Design Guide](PCB_DESIGN_GUIDE.md) - Start here!
2. Follow ai03's guide: https://wiki.ai03.com/books/pcb-design
3. Use [PCB Design Checklist](PCB_DESIGN_CHECKLIST.md) as you work
4. Reference library designs in `../design-files/`

### Designing Wireless?
1. Read [PCB Design Guide](PCB_DESIGN_GUIDE.md) first (fundamentals)
2. Then read [Wireless PCB Design Guide](WIRELESS_PCB_DESIGN.md)
3. Study ebastler's guide: https://github.com/ebastler/zmk-designguide
4. Use [PCB Design Checklist](PCB_DESIGN_CHECKLIST.md) (includes wireless items)

### Need Quick Reference?
- Jump to [PCB Design Checklist](PCB_DESIGN_CHECKLIST.md)
- Use as a checklist while working
- Review before sending to manufacturing

---

## Guide Comparison

| Feature | PCB Design Guide | Wireless Guide | Checklist |
|---------|-----------------|----------------|-----------|
| **Level** | Beginner-Intermediate | Advanced | All Levels |
| **Length** | Comprehensive | Detailed | Quick Reference |
| **Focus** | Wired keyboards | Wireless keyboards | All projects |
| **Firmware** | QMK | ZMK | Both |
| **Format** | Tutorial | Technical Reference | Checklist |

---

## Key Topics by Guide

### PCB Design Guide
- ✅ KiCad setup and workflow
- ✅ Component selection for through-hole
- ✅ USB-C protection circuits
- ✅ ATmega328P/32A circuits
- ✅ Switch matrix design
- ✅ PCB layout best practices
- ✅ Manufacturing specifications
- ✅ Testing procedures

### Wireless PCB Design Guide
- ✅ nRF52840 module selection
- ✅ Battery management ICs
- ✅ LiPo/Li-Ion battery selection
- ✅ Charging circuits (simple & advanced)
- ✅ Power switching
- ✅ Battery voltage sensing
- ✅ RF/antenna considerations
- ✅ ZMK firmware configuration
- ✅ Low-power design

### PCB Design Checklist
- ✅ Pre-design requirements
- ✅ Schematic review items
- ✅ Layout review items
- ✅ Pre-manufacturing checks
- ✅ Testing procedures
- ✅ Common mistakes list

---

## External Resources

### Essential Reading
- **ai03 PCB Guide**: https://wiki.ai03.com/books/pcb-design
  - Original comprehensive guide
  - Great for beginners
  - Step-by-step tutorials

- **ebastler ZMK Guide**: https://github.com/ebastler/zmk-designguide
  - Wireless design authority
  - nRF52840 focus
  - Advanced topics

- **QMK Documentation**: https://docs.qmk.fm/
  - Firmware reference
  - Configuration guide
  - Feature documentation

- **ZMK Documentation**: https://zmkfirmware.dev/
  - Wireless firmware
  - Power profiler
  - Device tree configuration

### Component Resources
- **marbastlib**: https://github.com/ebastler/marbastlib
  - KiCad library for keyboards
  - Tested footprints
  - Symbol library

- **KiCad Libraries**: https://kicad.github.io/
  - Official KiCad libraries
  - Standard components
  - 3D models

### Community
- **Keyboard Atelier Discord**: https://discord.gg/b7vwhHS
  - Designer community
  - Technical support
  - Design reviews

- **QMK Discord**: https://discord.gg/qmk
  - Firmware support
  - Configuration help

- **ZMK Discord**: https://zmk.dev/community/discord/invite
  - Wireless keyboard community
  - ZMK firmware support

---

## Contributing

Found an error or want to improve these guides?

1. **Report Issues:**
   - Open an issue in the repository
   - Describe the problem clearly
   - Suggest corrections

2. **Submit Improvements:**
   - Fork the repository
   - Make your changes
   - Submit a pull request
   - Explain your improvements

3. **Share Knowledge:**
   - Document your designs
   - Share lessons learned
   - Help others in the community

---

## Credits

These guides integrate knowledge from:
- **ai03** - Original PCB design guide
- **ebastler** - ZMK wireless design guide
- **nicell** - nice!nano and ZMK development
- **Keyboard community** - Collective knowledge and testing

---

## License

These guides are provided as educational resources. Individual designs and code may have their own licenses. Always check the license of any design you use or modify.

---

## Version History

**v1.0 - October 20, 2025**
- Initial release
- PCB Design Guide (comprehensive)
- Wireless PCB Design Guide (advanced)
- PCB Design Checklist (quick reference)
- Integrated ai03 and ebastler guides
- Added community resources

---

**Questions? Check the guides or ask in the community Discord servers!**

**Last Updated:** October 20, 2025
