# PCB Manufacturing Guide

A comprehensive guide for ordering through-hole keyboard PCBs from manufacturers.

## Table of Contents

- [Quick Start](#quick-start)
- [PCB Specifications](#pcb-specifications)
- [Recommended Manufacturers](#recommended-manufacturers)
- [Ordering Process](#ordering-process)
- [Common Settings](#common-settings)
- [Cost Estimation](#cost-estimation)
- [Quality Control](#quality-control)
- [Common Pitfalls](#common-pitfalls)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### For First-Time Orders

1. **Choose your project** from the `gerbers/` directory
2. **Download the Gerber ZIP file** (do not extract)
3. **Select a manufacturer** (see [Recommended Manufacturers](#recommended-manufacturers))
4. **Upload Gerber file** to manufacturer's website
5. **Configure settings** using [Common Settings](#common-settings)
6. **Review and order** (start with 5 PCBs for prototyping)

### Typical Lead Times

- **Production:** 2-5 days
- **Shipping (Standard):** 7-15 days
- **Shipping (Express):** 3-7 days
- **Total:** 10-20 days typical

---

## PCB Specifications

### Standard Through-Hole Keyboard PCB

Most through-hole keyboard PCBs use these specifications:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Layers** | 2 | Standard for keyboards |
| **Thickness** | 1.6mm | Standard PCB thickness |
| **Material** | FR4 | Standard PCB material |
| **Surface Finish** | HASL or ENIG | HASL cheaper, ENIG better |
| **Copper Weight** | 1 oz (35 µm) | Standard |
| **Solder Mask Color** | Green | Other colors available |
| **Silkscreen Color** | White | Standard on green |
| **Min Trace/Space** | 6/6 mil | 0.15mm |
| **Min Drill Size** | 0.3mm | For vias |

### Through-Hole Specific Requirements

- **Larger holes** for component leads (typically 0.8-1.0mm)
- **Plated through-holes** required for all component holes
- **Adequate pad size** for hand soldering (2-3mm diameter typical)
- **Clear silkscreen** for component identification

---

## Recommended Manufacturers

### JLCPCB (China)

**Best for:** Budget builds, quick turnaround

- **Website:** https://jlcpcb.com
- **Minimum Order:** 5 PCBs
- **Pricing:** $2 for 5 PCBs (100×100mm, basic specs)
- **Lead Time:** 2-3 days production + shipping
- **Shipping:** DHL, FedEx, or standard post
- **Pros:**
  - Very low cost
  - Fast production
  - Good quality for price
  - Easy online ordering
- **Cons:**
  - Shipping can be expensive for small orders
  - Customer service can be slow

**Recommended Settings:**
- Surface Finish: HASL (lead-free)
- Solder Mask: Green (cheapest)
- Silkscreen: White
- Remove Order Number: Yes (small fee)

### PCBWay (China)

**Best for:** Better quality, more options

- **Website:** https://www.pcbway.com
- **Minimum Order:** 5 PCBs
- **Pricing:** $5 for 5 PCBs (100×100mm, basic specs)
- **Lead Time:** 3-5 days production + shipping
- **Shipping:** DHL, FedEx, or standard post
- **Pros:**
  - Good quality control
  - More color options
  - Better customer service
  - Assembly services available
- **Cons:**
  - Slightly more expensive than JLCPCB
  - Longer lead times

**Recommended Settings:**
- Surface Finish: ENIG (better for through-hole)
- Solder Mask: Any color
- Silkscreen: White or Black
- Remove Order Number: Yes (included)

### OSH Park (USA)

**Best for:** US-based, premium quality

- **Website:** https://oshpark.com
- **Minimum Order:** 3 PCBs
- **Pricing:** $5 per square inch (3 boards)
- **Lead Time:** 12-20 days total
- **Shipping:** USPS (included in price)
- **Pros:**
  - US-based (faster for US customers)
  - Excellent quality
  - Purple PCBs (distinctive)
  - ENIG finish standard
  - Free shipping
- **Cons:**
  - More expensive
  - Longer lead times
  - Limited customization

**Recommended Settings:**
- All settings are standard (no customization needed)
- Purple solder mask with ENIG finish

### Elecrow (China)

**Best for:** Larger orders, assembly services

- **Website:** https://www.elecrow.com
- **Minimum Order:** 5 PCBs
- **Pricing:** $4.90 for 5 PCBs (100×100mm)
- **Lead Time:** 3-5 days production + shipping
- **Shipping:** DHL, FedEx, or standard post
- **Pros:**
  - Competitive pricing
  - Good for larger orders
  - Assembly services
  - Acrylic cutting services
- **Cons:**
  - Less popular than JLCPCB/PCBWay
  - Fewer reviews available

---

## Ordering Process

### Step-by-Step Guide

#### 1. Prepare Your Files

- Locate Gerber ZIP file in `gerbers/[project]/pcb/`
- **Do not extract** the ZIP file
- Verify file size (typically 100KB - 5MB)

#### 2. Create Account

- Sign up on manufacturer's website
- Verify email address
- Add shipping address

#### 3. Upload Gerber File

- Click "Quote Now" or "Instant Quote"
- Upload Gerber ZIP file
- Wait for automatic detection (10-30 seconds)

#### 4. Review Detected Settings

Manufacturer will auto-detect:
- PCB dimensions
- Layer count
- Number of holes
- Minimum trace width

**Verify these match project specifications!**

#### 5. Configure Options

Select the following settings:

**Required Settings:**
- **Quantity:** 5 (minimum for most manufacturers)
- **Layers:** 2
- **Thickness:** 1.6mm
- **Surface Finish:** HASL (lead-free) or ENIG
- **Copper Weight:** 1 oz
- **Solder Mask:** Green (or your preference)
- **Silkscreen:** White (or your preference)

**Optional Settings:**
- **Remove Order Number:** Yes (recommended)
- **Gold Fingers:** No
- **Castellated Holes:** No
- **Edge Connector:** No

#### 6. Review and Order

- Check total price (PCB + shipping)
- Review lead time
- Add to cart
- Select shipping method
- Complete payment

#### 7. Track Order

- Manufacturer will review files (1-2 hours)
- Production begins after approval
- Track shipment via provided tracking number

---

## Common Settings

### Standard Configuration

Use these settings for most through-hole keyboard PCBs:

```
Layers: 2
Dimensions: Auto-detected
Quantity: 5
Thickness: 1.6mm
Material: FR4-Standard TG 135-140
Surface Finish: HASL (Lead-Free) or ENIG
Copper Weight: 1 oz
Solder Mask: Green
Silkscreen: White
Min Track/Spacing: 6/6 mil
Min Hole Size: 0.3mm
Remove Order Number: Yes
```

### Budget Configuration

Minimize cost with these settings:

```
Layers: 2
Quantity: 5 (minimum)
Thickness: 1.6mm
Surface Finish: HASL (Lead-Free)
Copper Weight: 1 oz
Solder Mask: Green (cheapest)
Silkscreen: White
Remove Order Number: No (save $1-2)
Shipping: Standard (not express)
```

**Estimated Cost:** $2-5 + shipping

### Premium Configuration

Best quality for final builds:

```
Layers: 2
Quantity: 10-20
Thickness: 1.6mm
Surface Finish: ENIG (gold plating)
Copper Weight: 1 oz
Solder Mask: Black or custom color
Silkscreen: White or Gold
Remove Order Number: Yes
Shipping: Express (DHL/FedEx)
```

**Estimated Cost:** $20-50 + shipping

---

## Cost Estimation

### Price Breakdown

**PCB Manufacturing:**
- 5 PCBs (100×100mm): $2-5
- 10 PCBs: $10-15
- 20 PCBs: $20-30

**Size Multipliers:**
- 100×100mm: Base price
- 200×100mm: 2× base price
- 300×100mm: 3× base price

**Options:**
- ENIG finish: +$5-10
- Custom colors: +$5-15
- Remove order number: +$1-2

**Shipping:**
- Standard (15-20 days): $5-10
- Express (5-7 days): $15-30

### Example Costs

**60% Keyboard PCB (285×95mm):**
- JLCPCB: $8-12 (5 PCBs) + shipping
- PCBWay: $15-20 (5 PCBs) + shipping
- OSH Park: $45-60 (3 PCBs, shipping included)

**Macropad PCB (100×100mm):**
- JLCPCB: $2-5 (5 PCBs) + shipping
- PCBWay: $5-8 (5 PCBs) + shipping
- OSH Park: $15-20 (3 PCBs, shipping included)

### Money-Saving Tips

1. **Order in batches** - Combine multiple projects to save on shipping
2. **Use standard colors** - Green solder mask is cheapest
3. **Skip order number removal** - Save $1-2 if you don't mind the number
4. **Standard shipping** - Save $10-20 if not urgent
5. **Group orders** - Split costs with friends
6. **Wait for sales** - Manufacturers often have promotions

---

## Quality Control

### What to Check When PCBs Arrive

#### Visual Inspection

- [ ] **Solder mask** - No scratches or missing areas
- [ ] **Silkscreen** - Clear and readable
- [ ] **Holes** - All drilled, correct size
- [ ] **Edges** - Clean cuts, no burrs
- [ ] **Surface** - No contamination or oxidation

#### Dimensional Check

- [ ] **Overall size** - Measure with calipers
- [ ] **Mounting holes** - Check positions (±0.1mm)
- [ ] **USB cutout** - Verify size and position
- [ ] **Thickness** - Should be 1.6mm ±0.1mm

#### Electrical Test

- [ ] **Continuity** - Test traces with multimeter
- [ ] **Isolation** - Verify no shorts between traces
- [ ] **Plating** - Check through-hole plating quality

### Common Defects

**Minor (Acceptable):**
- Small silkscreen imperfections
- Slight color variation
- Minor edge roughness

**Major (Contact Manufacturer):**
- Missing holes
- Incorrect dimensions
- Shorts between traces
- Missing copper layers
- Damaged solder mask

---

## Common Pitfalls

### File Issues

**Problem:** Gerber files not detected correctly

**Solution:**
- Ensure ZIP file contains all layers
- Check file naming convention
- Use manufacturer's Gerber viewer to verify

**Problem:** Wrong dimensions detected

**Solution:**
- Manually enter correct dimensions
- Check if outline layer is included
- Verify units (mm vs inches)

### Specification Issues

**Problem:** PCB too thin/thick

**Solution:**
- Always specify 1.6mm for keyboards
- Thinner PCBs (1.2mm) may flex
- Thicker PCBs (2.0mm) may not fit cases

**Problem:** Wrong surface finish

**Solution:**
- HASL is fine for through-hole
- ENIG better for fine-pitch components
- Avoid OSP for hand soldering

### Ordering Issues

**Problem:** High shipping costs

**Solution:**
- Order multiple projects together
- Use standard shipping if not urgent
- Consider local manufacturers for small orders

**Problem:** Long lead times

**Solution:**
- Order early (allow 3-4 weeks)
- Use express shipping if needed
- Check manufacturer's current lead times

---

## Troubleshooting

### PCB Doesn't Fit Case

**Possible Causes:**
- PCB dimensions incorrect
- Mounting holes misaligned
- USB cutout wrong size

**Solutions:**
- Verify dimensions against specifications
- Check mounting hole positions with calipers
- File or sand edges if slightly oversized
- Modify case if PCB is correct

### Components Don't Fit

**Possible Causes:**
- Holes too small
- Pads too small
- Wrong footprint

**Solutions:**
- Verify hole sizes (should be 0.8-1.0mm for most components)
- Drill out holes if slightly small
- Check component datasheet for correct footprint

### Soldering Issues

**Possible Causes:**
- Poor surface finish
- Contaminated pads
- Insufficient pad size

**Solutions:**
- Clean pads with isopropyl alcohol
- Use flux for difficult joints
- Increase soldering iron temperature (350-400°C)
- Consider ENIG finish for next order

### Electrical Issues

**Possible Causes:**
- Manufacturing defect
- Design error
- Assembly error

**Solutions:**
- Test continuity with multimeter
- Check for shorts between traces
- Verify component orientation
- Contact manufacturer if PCB defect

---

## Additional Resources

### Gerber Viewers

- **Online:** https://www.pcbway.com/project/OnlineGerberViewer.html
- **Software:** KiCad, gerbv, ViewMate

### PCB Calculators

- **Trace Width:** https://www.4pcb.com/trace-width-calculator.html
- **Via Size:** https://www.4pcb.com/via-calculator.html
- **Cost Estimator:** Use manufacturer's instant quote

### Community Resources

- **r/PrintedCircuitBoard** - PCB manufacturing advice
- **r/MechanicalKeyboards** - Keyboard-specific help
- **EEVblog Forum** - General PCB discussion

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-16 | Initial release |

---

## License

This guide is provided as-is for educational purposes. Always verify specifications with your PCB manufacturer before ordering.
