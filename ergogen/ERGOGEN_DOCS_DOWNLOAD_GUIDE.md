# Ergogen Documentation Download & Setup Guide

**Source:** ChatGPT Conversation - RTX 5070 Ollama Models  
**Topic:** Best practices for mirroring Ergogen docs offline and integrating with QMK/Vial workflow

---

## Overview

This guide covers downloading a full offline mirror of [https://docs.ergogen.xyz/](https://docs.ergogen.xyz/) and integrating it into your keyboard development workflow.

---

## Initial Approach: Three Main Options

### Option 1 (Best): wget Full Mirror (Recommended)

Standard approach for static documentation sites:

```bash
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  https://docs.ergogen.xyz/
```

**What each flag does:**
- `--mirror` → recursive crawl of the whole site
- `--page-requisites` → downloads CSS, JS, images
- `--convert-links` → makes it work offline
- `--adjust-extension` → fixes `.html` extensions
- `--no-parent` → prevents crawling outside the docs site

**Output structure:**
```
docs.ergogen.xyz/
├── index.html
├── getting-started/
├── components/
└── assets/
```

Then open `docs.ergogen.xyz/index.html` offline in your browser.

---

### Option 2: Limit Crawl Depth (Safer)

Docs sites sometimes explode into infinite-ish crawling (tags, search pages, etc.).

```bash
wget \
  --mirror \
  --level=3 \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  https://docs.ergogen.xyz/
```

This avoids pulling junk pages like:
- Search queries
- Infinite tag pages
- Anchors

---

### Option 3: HTTrack (More Modern & Robust)

If wget misses pages due to JS routing:

**Command-line:**
```bash
httrack https://docs.ergogen.xyz/ -O ./ergogen-docs
```

**HTTrack advantages:**
- Complex link crawling
- Retry logic
- Handles weird documentation structures

**GUI Method:**
1. Install: [https://www.httrack.com](https://www.httrack.com)
2. New Project → `https://docs.ergogen.xyz/` → Start

---

## Important Reality Check

**Ergogen docs are:**
- Mostly static Markdown-rendered pages
- Minimal JS navigation complexity

**Therefore:**
- ✅ `wget` is enough
- ❌ You do NOT need Playwright / headless browser scraping

---

## Windows PowerShell Issues & Fixes

### The Problem

PowerShell's `wget` is **NOT GNU wget**—it's an alias for `Invoke-WebRequest`:

```
wget --mirror --convert-links ... 
→ Error: "A positional parameter cannot be found that accepts argument '--convert-links'"
```

So flags like `--mirror`, `--convert-links`, etc. don't exist in PowerShell's version.

---

### Fix Option 1 (BEST): Install Real wget via WSL

**Install WSL first, then:**

```bash
sudo apt update
sudo apt install wget
```

**Verify:**
```bash
wget --version
# Should show: GNU Wget 1.21+
```

Then your original command works exactly:
```bash
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  https://docs.ergogen.xyz/
```

This is the **cleanest + most reliable solution**.

---

### Fix Option 2: Use Real wget on Windows (Git Bash)

If you have Git installed:

1. Open: **Git Bash**
2. Run the same command

Git Bash includes GNU wget in many installs (or you can install via MSYS2).

**Note:** Some MSYS builds are stripped versions that lack `--adjust-extension`, so WSL is preferred.

---

### Fix Option 3: Use PowerShell Equivalent (NOT Recommended)

```powershell
Invoke-WebRequest https://docs.ergogen.xyz/ -OutFile index.html
```

**Problems:**
- No recursion
- No link rewriting
- No assets handling
- Basically useless for docs mirroring

---

### Fix Option 4: HTTrack on Windows

The least painful path for Windows without WSL:

1. Install: [https://www.httrack.com](https://www.httrack.com)
2. Run: New Project → `https://docs.ergogen.xyz/` → Start

It handles Windows quirks better and doesn't require flag debugging.

---

## The Better Dev Setup: WSL Environment

Given you're building QMK + Vial + Ergogen + KiCad workflows, standardize on **WSL**.

**Why?**
- Real `wget` ✓
- Git tooling consistency ✓
- Python tooling for Ergogen scripts ✓
- Same environment as most keyboard devs ✓
- No Windows/MSYS edge cases ✓

---

## After Download: Converting to Markdown

**Important:** Don't just feed raw HTML to your AI model.

### Convert HTML to Clean Markdown

```bash
pandoc file.html -t markdown -o file.md
```

Or batch convert all files.

**Result structure:**
```
keyboard-context/
└── ergogen-docs-md/
    ├── index.md
    ├── getting-started.md
    ├── components.md
    └── ...
```

This is what Continue + Qwen will actually understand well.

---

## Best Workflow for Your Setup

For QMK / Vial / Ergogen stack:

```
1. git clone qmk_firmware
2. git clone vial-qmk
3. wget ergogen docs (or HTTrack)
4. Convert HTML → Markdown
5. Open everything in VS Code workspace
6. Continue + Qwen reads across all folders
```

---

## Key Insights

### What You Do NOT Need

- ❌ Embeddings
- ❌ RAG pipelines
- ❌ Vector databases

**Why?** Because Ergogen docs are:
- Small
- Structured
- Deterministic

👉 **Treat them like source code, not a knowledge base**

---

### Current Environment Comparison

| Environment | wget Type | Problem |
|---|---|---|
| PowerShell | Invoke-WebRequest | No recursion / no flags |
| Git Bash | MSYS minimal wget | Missing `--adjust-extension` |
| **WSL (Recommended)** | **GNU wget** | **None—correct tool** |

---

## Next Steps (Recommended)

Once you download the docs, the real value comes from processing them:

1. **Convert docs → clean markdown**
   - Strip navigation junk
   - Build `ergogen-cheatsheet.md`

2. **Create AI-optimized documentation**
   - Augment `AI_CONTEXT.md` in your workspace
   - Build searchable local knowledge base
   - Create Continue "workspace-optimized docs"

3. **Feed to Continue/Qwen**
   - This step matters more than the download itself

---

## Quick Reference Commands

### WSL Ubuntu Setup
```bash
# Install dependencies
sudo apt update
sudo apt install wget

# Download Ergogen docs
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  https://docs.ergogen.xyz/

# Batch convert to markdown (requires pandoc)
sudo apt install pandoc
for file in docs.ergogen.xyz/**/*.html; do
  pandoc "$file" -t markdown -o "${file%.html}.md"
done
```

### HTTrack (Windows)
```bash
httrack https://docs.ergogen.xyz/ -O ./ergogen-docs
```

---

## Summary

**For keyboard dev + QMK + Vial + Ergogen:**

1. ✅ Use **WSL** for proper tooling
2. ✅ Mirror with `wget` or HTTrack
3. ✅ Convert to Markdown
4. ✅ Create AI-optimized cheat sheets
5. ✅ Integrate into your VS Code workspace

This gives Continue + Qwen the best context to work with your keyboard firmware projects.
