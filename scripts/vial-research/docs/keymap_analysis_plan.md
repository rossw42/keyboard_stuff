# Complete Keymap Analysis Plan: keyboard.json → vial.json Patterns

## Objective

Analyze ALL keyboard.json ↔ vial.json pairs from `vial_keyboard_pairs.csv` to understand exact conversion patterns and generate comprehensive findings for the final document.

## Methodology

### Phase 1: Establish Reading Order (Row by Row, All Keyboards)
- Read each CSV row sequentially 
- For each pair: read keyboard.json layout structure, compare with vial.json keymap format
- Build comprehensive side-by-side analysis for ALL keyboards

### Phase 2: Categorize Format Types
- Simple string entries (`"0,0"`)
- Wrapped single-key entries `[{"x": N, "y": M}, "r,c"]`
- Wide/key-offset entries `[{"x": 0.5, "y": 0}, "r,c"]`  
- Multi-key rows with color/separator properties
- Complex layouts (Boston-style with escape sequences)

### Phase 3: Extract Mapping Rules for Each Keyboard Type
- Standard key at column C → what x value?
- Row offset (keyboard.json "y" field) → vial.json y calculation
- Wide keys (w property) → what pattern emerges?
- Color properties → always preserved or conditional?

### Phase 4: Document Brand/Keyboard-Specific Conventions
- Which brands use which format?
- Are there consistent rules per manufacturer?
- Exceptions vs patterns

## Reading Order

We'll read keyboards in CSV order, examining each pair thoroughly:

1. **Start:** `D:\GitHub2\vial-qmk\keyboards\alpha` (already have baseline)
2. Continue with alps64 → arisu → a_dux → boston
3. Work through all remaining keyboards systematically

For each keyboard we examine, document:
- CSV line number
- Keyboard.json layout properties found (matrix coords, x/y/w fields)
- vial.json keymap pattern used in real file
- Whether our simple approach works or needs full wrapping
- Notes on exceptions/unusual formatting

## Deliverables

After analyzing all keyboards, produce:
1. **Comprehensive findings document** - patterns across ALL keyboard types
2. **Coordinate calculation rules** - how x/y derived from keyboard.json data
3. **Wide key pattern rules** - when and where w=0.5 vs plain strings used
4. **Brand-specific conventions list** - format preferences per manufacturer
5. **Lossy mapping documentation** - what metadata gets stripped/preserved

---

## Reading Plan Summary

Total keyboards in CSV: ~385+ pairs (multiple sublayouts for some brands)

We'll process systematically, starting with first batch:

### BATCH 1: First Row of CSV
- **Line 2:** alpha keyboard (already examined as baseline)
- **Line 3:** alps64 keyboard  
- **Line 4:** arisu keyboard
- etc.

For each keyboard, we'll produce findings for ALL keyboards in that batch before moving on.

---

## Analysis Template (Will be completed per keyboard)

**CSV Line: X** - Keyboard Name: [NAME]

### keyboard.json properties found:
- Layout entries count: X keys
- Key structure sample: [{"matrix": ["row", "col"], "x": 0, "y": 0, "label": "key"}]
- Wide keys present? Yes/No - list which keys have "w" property
- Coordinate system in use: standard (x=0) or wide (x=0.5)?

### vial.json keymap pattern:
- Total rows: XX entries in final array
- Entry formats used:
  * Simple string: "__" entries total
  * Wrapped coords: __ entries like [{"x": ...}, "r,c"]
  * Multi-key rows (separators): __ rows with multiple keys per array
- Coordinate calculation rule observed

### Pattern classification:
[ ] Type A - All wrapped single-key entries
[ ] Type B - Mix of plain strings and wrapped offsets  
[ ] Type C - Complex multi-key rows
[ ] Type D - Simple format (all plain strings, no wrapping)

### Key mappings derived:
- Standard key at column 0 → x=0 in vial.json? Yes/No
- Wide/off-center keys have x=0.5? Which ones exactly?
- Row index "y" from keyboard.json preserved or recalculated?

---

Let's begin with the first batch of keyboards to establish patterns across multiple boards.
