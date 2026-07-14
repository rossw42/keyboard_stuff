
## 🖼️ Gallery view — is it possible?


Researched whether this README could show little thumbnail photos next to each keyboard, HHKB-collector-Instagram-style. Short answer: **yes, GitHub-flavored markdown supports images inside table cells**, no plugins needed — `| ![alt](url) |` renders as a real thumbnail right in a pipe-table cell, and inline HTML like `<img src="..." width="80">` also renders, which is the easiest way to control thumbnail size. The reliable hotlink pattern is `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path-to-image>` — most keyboard repos already have a photo committed somewhere (README banner, `/images` folder, KiCad render export), so no image hosting is needed.

What GitHub markdown does **not** support: CSS, `<style>` blocks, or `<picture>`/responsive-art-direction tags (they get stripped), and there's no built-in "masonry" or lightbox gallery widget — you just get whatever a plain HTML `<table>` or grid of images looks like when GitHub sanitizes the HTML.

Practical recommendation for this file specifically: it's not worth converting the whole research README into an image gallery — most of these repos don't have a photo of a *finished build* (many are just PCB/KiCad projects, several boards are unbuilt concepts), and pulling 100+ external images into one README would make it slow to load and easy to break (dead links when a repo renames a branch or moves an image). A better fit would be a **separate, smaller `gallery.md`** (or a `<details>`-collapsed section at the bottom of this file) containing only the boards that are actually built (i.e. rows where "Built" = `[x]`), each with one `<img src="..." width="200">` thumbnail linking back to its row here. That keeps this file lean and turns the "Built" column into a natural gate for what earns a spot in the gallery.


