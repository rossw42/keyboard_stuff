"""
generate_switch_labels.py
=========================
Generates one Design-B HTML label per switch from switchbook_upload.csv.

Usage:
    python generate_switch_labels.py

Output:
    labels/<slug>.html   (one file per switch, 54 total)

CSS is extracted live from label_design_b.html (the approved template),
so any tweak to that file is automatically picked up on the next run.
"""
import csv, pathlib, re, unicodedata

BASE     = pathlib.Path(__file__).parent
CSV_IN   = BASE / "switchbook_upload.csv"
TEMPLATE = BASE / "label_design_b.html"
OUT_DIR  = BASE / "labels"

# ── type lookup ───────────────────────────────────────────────────────────────
TYPE_MAP = {
    "CLICKY":         ("clicky",  "Clicky"),
    "TACTILE":        ("tactile", "Tactile"),
    "LINEAR":         ("linear",  "Linear"),
    "SILENT_TACTILE": ("silent",  "Silent Tactile"),
    "SILENT":         ("silent",  "Silent"),
}
TYPE_DESC = {
    "clicky":  "Audible click, tactile bump",
    "tactile": "Tactile bump, no click",
    "linear":  "Smooth linear, no bump",
    "silent":  "Dampened, quiet keystroke",
}

# ── helpers ───────────────────────────────────────────────────────────────────
def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s-]", "", t.lower().strip())
    return re.sub(r"[\s_-]+", "_", t)[:80]

def sv(val):
    v = val.strip()
    return v if v else "&#8212;"

def wrap(name):
    for sep in [" / ", " x ", " X "]:
        if sep in name:
            p = name.split(sep, 1)
            return p[0].strip() + "<br>" + p[1].strip()
    w = name.split()
    if len(w) >= 3:
        m = len(w) // 2
        return " ".join(w[:m]) + "<br>" + " ".join(w[m:])
    return name

def extract_css(html):
    """Pull the text between the first <style> and </style> tags."""
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""

# ── HTML builder ──────────────────────────────────────────────────────────────
def render(row, css):
    name       = row["Switch Name"].strip()
    mfr        = row["Manufacturer"].strip()
    raw_type   = row["Type"].strip().upper()
    actuation  = sv(row.get("Actuation Force (g)", ""))
    bottom_out = sv(row.get("Bottom Out Force (g)", ""))
    stem       = sv(row.get("Stem Shape", ""))
    compat     = sv(row.get("Compatibility", ""))
    notes_raw  = row.get("Notes", "").strip()

    mc, tl = TYPE_MAP.get(raw_type, ("tactile", raw_type.title() or "Unknown"))
    td     = TYPE_DESC.get(mc, "MX-compatible")

    notes = re.sub(r"Stock:\s*\S+;?\s*",      "", notes_raw, flags=re.IGNORECASE)
    notes = re.sub(r"Installed:\s*\S+\.?\s*", "", notes,     flags=re.IGNORECASE)
    notes = notes.strip(". ").strip()

    if actuation  != "&#8212;" and not actuation.endswith("g"):  actuation  += " g"
    if bottom_out != "&#8212;" and not bottom_out.endswith("g"): bottom_out += " g"

    notes_row = ('\n    <div class="c-notes">' + notes + "</div>") if notes else ""

    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="UTF-8">',
        "<title>" + name + "</title>",
        "<style>",
        css,
        "</style>",
        "</head>",
        "<body>",
        '<div class="sheet">',
        "",
        '  <div class="tag">',
        '    <div class="t-marker ' + mc + '"></div>',
        '    <span class="t-name">' + name + "</span>",
        '    <span class="t-type">' + tl  + "</span>",
        "  </div>",
        "",
        '  <div class="cut-v"></div>',
        '  <span class="cut-v-label">&#9988;</span>',
        '  <div class="cut-h"></div>',
        '  <span class="cut-h-label">&#9988; cut</span>',
        "",
        '  <div class="card">',
        '    <div class="c-head">',
        '      <div class="c-name">' + wrap(name) + "</div>",
        '      <div class="c-mfr">'  + mfr        + "</div>",
        "    </div>",
        '    <div class="c-type-row">',
        '      <span class="c-type-box">'  + tl + "</span>",
        '      <span class="c-type-desc">' + td + "</span>",
        "    </div>",
        '    <div class="c-specs-grid">',
        '      <div><div class="s-label">Actuation</div>'   + '<div class="s-val">' + actuation  + "</div></div>",
        '      <div><div class="s-label">Bottom Out</div>'  + '<div class="s-val">' + bottom_out + "</div></div>",
        '      <div><div class="s-label">Stem</div>'        + '<div class="s-val">' + stem       + "</div></div>",
        '      <div><div class="s-label">Compatibility</div>' + '<div class="s-val">' + compat   + "</div></div>",
        "    </div>" + notes_row,
        "  </div>",
        "",
        "</div>",
        "</body>",
        "</html>",
    ]
    return "\n".join(lines)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(exist_ok=True)

    css = extract_css(TEMPLATE.read_text(encoding="utf-8"))
    if not css:
        raise RuntimeError("Could not extract CSS from " + str(TEMPLATE))
    print("CSS extracted from template: " + str(len(css)) + " chars")

    with open(CSV_IN, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    count = 0
    for row in rows:
        name = row.get("Switch Name", "").strip()
        if not name:
            continue
        out = OUT_DIR / (slugify(name) + ".html")
        out.write_text(render(row, css), encoding="utf-8")
        print("  " + out.name)
        count += 1

    print("\nDone: " + str(count) + " labels -> " + str(OUT_DIR))

if __name__ == "__main__":
    main()

