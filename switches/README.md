# Switch Inventory & Labels

This folder manages the physical keyboard switch collection — inventory tracking,
tray mapping, and printable reference labels.

---

## Folder Structure

```
switches/
├── README.md                    ← this file
│
├── switchbook_upload.csv        ← master inventory (source of truth)
├── switch_inventory_v2.md       ← human-readable inventory summary
│
├── label_design_b.html          ← approved label template (Design B)
├── generate_switch_labels.py    ← label generator script
├── labels/                      ← generated HTML labels (one per switch)
│   ├── invyr_holy_panda.html
│   ├── kailh_box_white.html
│   └── ... (53 total)
│
├── tray_layout.md               ← physical tray slot layout
├── tray_map_v2.md               ← tray map with switch assignments
├── tray_calibration.json        ← calibration data for tray imaging
├── calibrate_tray.py            ← tray calibration script
├── inventory_counter.py         ← switch counting utility
│
├── ebay_switches.md             ← eBay listing notes (sourcing)
├── ebay_switch_reference.md     ← reference data from eBay listings
├── ebay_to_tray_matches.md      ← mapping eBay lots → tray positions
│
├── fromebay1.PNG                ← eBay listing photo
├── fromebay2.webp               ← eBay listing photo
├── IMG_3218.JPG                 ← tray photo
├── IMG_3219.JPG                 ← tray photo
└── IMG_3220.JPG                 ← tray photo
```

---

## Inventory

### Master data: `switchbook_upload.csv`

The canonical switch list. Each row is one switch type with:

| Column | Description |
|---|---|
| Switch Name | Full switch name |
| Type | `CLICKY`, `TACTILE`, `LINEAR`, `SILENT_TACTILE` |
| Technology | `MECHANICAL` for all current entries |
| Manufacturer | OEM manufacturer |
| Actuation Force (g) | Operating force in grams |
| Bottom Out Force (g) | Bottom-out force in grams (often blank) |
| Compatibility | e.g. `MX-style` |
| Stem Shape | e.g. `MX` |
| Notes | Free-text; encodes `Stock: N; Installed: N` counts |

**To update inventory:** edit `switchbook_upload.csv`, then re-run the label
generator (see below). Stock/Installed counts live in the Notes column.

### Human-readable summary: `switch_inventory_v2.md`

Flat table of all switches with type, force, stock, and installed counts.
Derived from the tray map and eBay photos. Update this alongside the CSV
when counts change.

---

## Labels

### Design

**Design B — Outline + Pattern Marker**

- **Label size:** 4″ × 6″ (standard label printer sheet)
- **Content area:** top 3.25″ of the label; bottom 2.75″ intentionally blank
- **Left margin:** 0.18″ offset to compensate for printer edge clipping

**Tag strip** (top, 2″ × 0.5″):
- Left edge pattern encodes switch type (see legend below)
- Switch name in bold
- Type badge: black background, white text
- Vertical dashed cut line at the 2″ mark
- Horizontal dashed cut line below the strip

**Reference card** (below the cut line):
- Large switch name
- Manufacturer
- Type badge (black/white)
- 4-spec grid: Actuation, Bottom Out, Stem, Compatibility
- Notes line (if present in CSV)

**Type → pattern legend:**

| Type | Tag marker pattern |
|---|---|
| Clicky | Solid black bar |
| Tactile | Diagonal hatch (45°) |
| Linear | Horizontal lines |
| Silent Tactile | Dot grid |

### Generating labels

```bash
cd D:\GitHub\keyboard_stuff\switches
python generate_switch_labels.py
```

Output: `labels/<switch-slug>.html` — one file per row in `switchbook_upload.csv`.

The script reads CSS directly from `label_design_b.html`, so any style
changes to the template are automatically reflected on the next run.

### Printing a label

1. Open the desired `labels/<name>.html` in Chrome (or Edge)
2. `Ctrl+P` → **Print**
3. Set paper size to **4″ × 6″** (or the label preset for your printer)
4. **Enable "Background graphics"** in More settings — required for the
   black type badges and pattern markers to print
5. Set margins to **None**
6. Print

### Cutting

After printing:
- Cut along the **horizontal dashed line** to separate the tag strip from the card
- Cut along the **vertical dashed line** to trim the tag to 2″

---

## Tray mapping

| File | Purpose |
|---|---|
| `tray_layout.md` | Physical slot grid for the switch storage tray |
| `tray_map_v2.md` | Which switch lives in each tray slot (row, col) |
| `tray_calibration.json` | Camera/image calibration data for tray positions |
| `calibrate_tray.py` | Script to recalibrate tray position detection |

---

## Reference photos

| File | Contents |
|---|---|
| `fromebay1.PNG` | eBay lot listing photo (used to identify switches) |
| `fromebay2.webp` | eBay lot listing photo |
| `IMG_3218.JPG` | Physical tray — top view |
| `IMG_3219.JPG` | Physical tray — detail |
| `IMG_3220.JPG` | Physical tray — detail |
| `ebay_switches.md` | Notes from eBay sourcing |
| `ebay_switch_reference.md` | Spec reference cross-checked against eBay photos |
| `ebay_to_tray_matches.md` | Maps eBay lot identities to tray positions |
