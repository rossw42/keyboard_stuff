# Manufacturing Operation Sequence
## 60% Wooden Keyboard Case

---

## Top Frame Machining Sequence

### Setup and Preparation
**Estimated Time: 15 minutes**

1. **Stock Inspection and Preparation**
   - Verify stock dimensions: 295mm × 105mm × 6mm (rough)
   - Check for defects, cracks, or excessive grain runout
   - Mark reference edge and face for consistent workholding
   - **Critical**: Ensure stock is flat and parallel within 0.1mm

2. **CNC Machine Setup**
   - Install appropriate tooling (see tool list below)
   - Zero machine on stock corner (X0, Y0 at bottom-left, Z0 on top surface)
   - Secure stock with clamps or vacuum table
   - **Critical**: Ensure stock cannot shift during machining

### Operation 1: Face Milling to Final Thickness
**Tool**: 12mm face mill or surfacing bit  
**Estimated Time: 8 minutes**

1. Face mill top surface to 5.5mm thickness
2. Flip stock, face mill bottom surface to final 5mm thickness
3. Verify thickness with calipers at multiple points (tolerance: ±0.1mm)
4. **Critical**: Maintain parallel surfaces - check with dial indicator

### Operation 2: Perimeter Rough Cut
**Tool**: 6mm end mill (2-flute)  
**Estimated Time: 12 minutes**

1. Cut outer perimeter to 285mm × 95mm (leave 0.5mm stock for finishing)
2. Use climb milling for cleaner edges
3. Multiple passes at 2mm depth of cut
4. **Critical**: Ensure tabs are placed in non-critical areas for easy removal

### Operation 3: PCB Cavity Roughing
**Tool**: 6mm end mill (2-flute)  
**Estimated Time: 18 minutes**

1. Rough out main PCB cavity to 3.5mm depth
2. Leave 0.3mm radial stock and 0.2mm floor stock for finishing
3. Use adaptive clearing or pocketing strategy
4. Stepdown: 1.5mm per pass
5. **Critical**: Monitor chip evacuation - clear chips regularly to prevent recutting

### Operation 4: PCB Cavity Finishing
**Tool**: 6mm end mill (finishing grade, 3-4 flute)  
**Estimated Time: 10 minutes**

1. Finish cavity walls to final dimensions
2. Finish cavity floor to 3.8mm depth
3. Single finishing pass at full depth for floor
4. **Critical**: Verify cavity depth with depth gauge - must be 3.8mm ±0.1mm

### Operation 5: Standoff Pocket Drilling
**Tool**: 4.5mm end mill or drill bit  
**Estimated Time: 5 minutes**

1. Drill 6 standoff pockets to 2mm depth
2. Locations per design file coordinates
3. Use peck drilling cycle to clear chips
4. **Critical**: Verify pocket depth - must be 2mm ±0.05mm for proper standoff seating

### Operation 6: Brass Insert Pilot Holes
**Tool**: 2.5mm drill bit  
**Estimated Time: 4 minutes**

1. Drill 6 pilot holes through remaining 1mm floor thickness
2. Locations centered in standoff pockets
3. Use peck drilling cycle
4. **Critical**: Holes must be perpendicular - check with square if needed

### Operation 7: Perimeter Finishing
**Tool**: 6mm end mill (finishing grade) or 1/4" compression bit  
**Estimated Time: 8 minutes**

1. Finish outer perimeter to final 285mm × 95mm dimensions
2. Single finishing pass at full depth
3. Use climb milling for best surface finish
4. **Critical**: Ensure corners are clean and square

### Operation 8: Tab Removal and Edge Cleanup
**Tool**: Manual (saw, chisel, sandpaper)  
**Estimated Time: 10 minutes**

1. Carefully remove holding tabs with flush-cut saw
2. Sand tab remnants flush with 120 grit sandpaper
3. Lightly break all sharp edges with 220 grit sandpaper
4. **Critical**: Do not over-sand - maintain dimensional accuracy

### Operation 9: Brass Insert Installation
**Tool**: Arbor press or soldering iron (260°C)  
**Estimated Time: 8 minutes**

1. Expand pilot holes to 2.8mm with drill bit
2. Heat brass inserts with soldering iron OR use arbor press
3. Press inserts flush with pocket floor (should sit 2mm below top surface)
4. Allow to cool if heat-installed
5. **Critical**: Inserts must be perpendicular and flush - test with M3 screw

### Top Frame Total Time: **98 minutes (~1.6 hours)**

---

## Bottom Tray Machining Sequence

### Setup and Preparation
**Estimated Time: 15 minutes**

1. **Stock Inspection and Preparation**
   - Verify stock dimensions: 295mm × 105mm × 20mm (rough)
   - Check for defects, cracks, or excessive grain runout
   - Mark reference edge and face
   - **Critical**: Ensure stock is flat and parallel within 0.1mm

2. **CNC Machine Setup**
   - Install appropriate tooling
   - Zero machine on stock corner (X0, Y0 at bottom-left, Z0 on top surface)
   - Secure stock with clamps
   - **Critical**: Use adequate clamping - this is a deep pocket operation

### Operation 1: Face Milling to Final Thickness
**Tool**: 12mm face mill or surfacing bit  
**Estimated Time: 10 minutes**

1. Face mill top surface to 16mm thickness
2. Flip stock, face mill bottom surface to final 15mm thickness
3. Verify thickness with calipers (tolerance: ±0.1mm)
4. **Critical**: Maintain parallel surfaces

### Operation 2: Perimeter Rough Cut
**Tool**: 6mm end mill (2-flute)  
**Estimated Time: 12 minutes**

1. Cut outer perimeter to 285mm × 95mm (leave 0.5mm stock for finishing)
2. Use climb milling
3. Multiple passes at 2mm depth of cut
4. **Critical**: Ensure tabs are placed in corners for stability

### Operation 3: Main Cavity Roughing
**Tool**: 6mm end mill (2-flute)  
**Estimated Time: 35 minutes**

1. Rough out main cavity to 12.5mm depth
2. Leave 0.3mm radial stock and 0.2mm floor stock for finishing
3. Use adaptive clearing strategy
4. Stepdown: 2mm per pass (6-7 passes total)
5. **Critical**: This is the longest operation - monitor tool wear and chip evacuation
6. **Critical**: Check machine temperature - allow cooldown if needed

### Operation 4: Main Cavity Finishing
**Tool**: 6mm end mill (finishing grade, 3-4 flute)  
**Estimated Time: 12 minutes**

1. Finish cavity walls to final dimensions
2. Finish cavity floor to 13mm depth (leaving 2mm floor thickness)
3. Single finishing pass for walls
4. **Critical**: Verify floor thickness - must be 2mm ±0.1mm

### Operation 5: Corner Radius Cleanup (if needed)
**Tool**: 3mm ball end mill  
**Estimated Time: 5 minutes**

1. Clean up internal corners if tighter radius is desired
2. Blend into cavity walls smoothly
3. **Note**: Optional operation depending on design preference

### Operation 6: Mounting Hole Drilling
**Tool**: 3.2mm drill bit  
**Estimated Time: 4 minutes**

1. Drill 6 mounting holes through 2mm floor
2. Locations per design file coordinates
3. Use peck drilling cycle
4. **Critical**: Holes must align with brass inserts in top frame - verify coordinates

### Operation 7: Countersink for Flat Head Screws
**Tool**: 6mm 90° countersink bit  
**Estimated Time: 5 minutes**

1. Countersink all 6 mounting holes from bottom surface
2. Depth: screw head should sit flush or 0.2mm below surface
3. Test fit with M3 flat head screw
4. **Critical**: Do not over-countersink - screw must engage threads properly

### Operation 8: Perimeter Finishing
**Tool**: 6mm end mill (finishing grade)  
**Estimated Time: 8 minutes**

1. Finish outer perimeter to final 285mm × 95mm dimensions
2. Single finishing pass at full depth
3. Use climb milling
4. **Critical**: Ensure edges are clean and perpendicular to bottom surface

### Operation 9: Tab Removal and Edge Cleanup
**Tool**: Manual (saw, chisel, sandpaper)  
**Estimated Time: 10 minutes**

1. Carefully remove holding tabs with flush-cut saw
2. Sand tab remnants flush with 120 grit sandpaper
3. Lightly break all sharp edges with 220 grit sandpaper
4. **Critical**: Do not over-sand - maintain dimensional accuracy

### Bottom Tray Total Time: **116 minutes (~1.9 hours)**

---

## Tool List

| Tool | Type | Diameter | Purpose | Notes |
|------|------|----------|---------|-------|
| Face Mill | Surfacing | 12mm+ | Face milling operations | Can substitute with large surfacing bit |
| End Mill | 2-flute, roughing | 6mm | Roughing operations | Upcut or compression |
| End Mill | 3-4 flute, finishing | 6mm | Finishing operations | Compression bit preferred for wood |
| End Mill | 2-flute | 4.5mm | Standoff pockets | Can use drill bit instead |
| Drill Bit | Twist drill | 2.5mm | Brass insert pilot holes | HSS or carbide |
| Drill Bit | Twist drill | 2.8mm | Brass insert final holes | HSS or carbide |
| Drill Bit | Twist drill | 3.2mm | Bottom tray mounting holes | HSS or carbide |
| Countersink | 90° | 6mm | Flat head screw countersinks | Adjustable depth preferred |
| Ball End Mill | 2-flute | 3mm | Corner radius cleanup (optional) | For aesthetic corners |

---

## Feeds and Speeds Recommendations

**Material**: Hardwood (Walnut, Maple, Cherry)  
**Machine**: Desktop CNC (Shapeoko, X-Carve, or similar)

| Operation | Tool | RPM | Feed Rate | Plunge Rate | DOC |
|-----------|------|-----|-----------|-------------|-----|
| Face Milling | 12mm face mill | 18,000 | 1500 mm/min | 500 mm/min | 0.5mm |
| Roughing | 6mm end mill | 18,000 | 1200 mm/min | 400 mm/min | 2mm |
| Finishing | 6mm end mill | 20,000 | 1500 mm/min | 500 mm/min | Full depth |
| Drilling | 2.5-3.2mm drill | 12,000 | 300 mm/min | 200 mm/min | Peck 2mm |
| Countersinking | 6mm countersink | 10,000 | 200 mm/min | 100 mm/min | 0.5mm |

**Notes:**
- Adjust feeds/speeds based on your specific machine capabilities
- Harder woods (Maple) may require 10-20% slower feed rates
- Listen to the machine - adjust if hearing excessive noise or chatter
- Use dust collection throughout all operations

---

## Critical Operations Requiring Extra Care

### 1. Main Cavity Roughing (Bottom Tray - Operation 3)
**Why Critical**: Deepest cut, longest operation, highest tool load
- **Risk**: Tool breakage, excessive heat buildup, poor surface finish
- **Mitigation**: 
  - Monitor chip evacuation constantly
  - Pause operation if chips accumulate
  - Check tool condition after every 2-3 passes
  - Allow machine to cool if steppers feel hot
  - Consider breaking into multiple programs if machine struggles

### 2. Brass Insert Installation (Top Frame - Operation 9)
**Why Critical**: Permanent installation, affects assembly quality
- **Risk**: Crooked inserts, damaged threads, inserts too deep/shallow
- **Mitigation**:
  - Use alignment jig or guide for perpendicularity
  - Test technique on scrap wood first
  - Install slowly and check alignment frequently
  - If using heat, maintain consistent temperature (260°C)
  - Test each insert with M3 screw before proceeding

### 3. Floor Thickness Verification (Both Parts)
**Why Critical**: Affects structural integrity and screw engagement
- **Risk**: Floor too thin (breakage), floor too thick (screws don't reach)
- **Mitigation**:
  - Measure floor thickness at multiple points with calipers
  - Use depth gauge to verify cavity depths
  - Top frame: 1mm floor under standoff pockets
  - Bottom tray: 2mm floor thickness
  - Stop and adjust toolpath if out of tolerance

### 4. Hole Alignment Between Parts
**Why Critical**: Parts must align for assembly
- **Risk**: Misaligned holes prevent case assembly
- **Mitigation**:
  - Use same zero reference point for both parts
  - Verify coordinates in CAM software before machining
  - Test fit parts before finishing operations
  - If misaligned, can slightly enlarge holes (last resort)

### 5. Tab Removal
**Why Critical**: Easy to damage finished part during removal
- **Risk**: Tear-out, splintering, dimensional errors
- **Mitigation**:
  - Use sharp flush-cut saw
  - Cut from both sides if possible
  - Support part during cutting
  - Sand carefully with backing block
  - Work slowly - rushing causes mistakes

---

## Quality Checkpoints During Machining

- [ ] After face milling: Verify thickness and parallelism
- [ ] After perimeter rough: Check overall dimensions
- [ ] After cavity roughing: Verify depth with gauge
- [ ] After cavity finishing: Check floor thickness
- [ ] After drilling: Verify hole locations and depths
- [ ] After brass insert installation: Test thread engagement
- [ ] After tab removal: Check for damage or tear-out
- [ ] Final inspection: Dimensional check per QC checklist

---

## Estimated Total Manufacturing Time

| Component | Machining Time | Manual Operations | Total |
|-----------|----------------|-------------------|-------|
| Top Frame | 75 minutes | 23 minutes | 98 minutes |
| Bottom Tray | 91 minutes | 25 minutes | 116 minutes |
| **Total per Case** | **166 minutes** | **48 minutes** | **214 minutes (~3.6 hours)** |

**Notes:**
- Times assume experienced operator and properly tuned machine
- First-time production may take 50-100% longer
- Does not include setup time, tool changes, or finishing operations
- Add 30-60 minutes for sanding and finishing preparation
