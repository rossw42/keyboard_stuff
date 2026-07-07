# Ergogen Working Samples

A curated collection of community Ergogen keyboard configs used as reference patterns for the toolkit. These are proven, real-world configurations — when writing a new config, start from the closest sample here.

## Provenance

Collected **October 22, 2025** via a GitHub API survey that found **123 Ergogen repositories** (full list: [`../docs/research/ergogen_repos_list.md`](../docs/research/ergogen_repos_list.md)). Notable star counts at the time: samoklava 379⭐, cephalopoda 232⭐, Kaly 209⭐, corax 131⭐, absolem 127⭐, mantis 117⭐, trochilidae 112⭐.

## Categories

### `minimal/` — small, easy-to-read configs
| Folder | Keyboard | Notes |
|---|---|---|
| `cephalopoda_idiosepius` | Cephalopoda Idiosepius | minimal split family member |
| `tern` | Tern | compact ergo |
| `tiny20` | Tiny20 | 20-key mini |
| `trochilidae_berylline` | Trochilidae Berylline | hummingbird recreation |
| `trochilidae_rufous` | Trochilidae Rufous | hummingbird recreation |

### `split/` — split keyboards
| Folder | Keyboard |
|---|---|
| `archimedes_tux` | Archimedes Tux |
| `cephalopoda_architeuthis` | Cephalopoda Architeuthis |
| `cephalopoda_dosidicus` | Cephalopoda Dosidicus |
| `jonkey` | Jonkey |
| `kaly` | Kaly (209⭐) |
| `nwsplit60` | NWSplit60 |
| `samoklava` | Samoklava (379⭐) |
| `uwb_electronics_club` | UWB Electronics Club board |

### `unibody/` — one-piece ergo boards
| Folder | Keyboard |
|---|---|
| `absolem` | Absolem (the original Ergogen keyboard) — simplified version |
| `mantis` | Mantis (hex-key layout) |
| `travis_ergogen_2024` | Travis's 2024 Ergogen build |

### `advanced/` — feature-rich configs
| Folder | Keyboard |
|---|---|
| `corax56` | Corax56 — PCB-generation variant |

### `tutorial/`
| Folder | Content |
|---|---|
| `chonkv` | ChonkV — used in tutorial walkthroughs |

### `uncategorized/` — pending sorting
Loose configs formerly at the root of this folder. **Some differ from same-named categorized versions — they are NOT confirmed duplicates** (e.g., `absolem.yaml` here is the full 972-line original; `unibody/absolem/config.yaml` is a 173-line simplified version; `corax56.yaml` here is an outlines/case variant vs. the PCB variant in `advanced/`). Sort or diff before deleting anything.

Includes: `absolem.yaml`, `samoklava.yaml`, `config.yaml` (identical to samoklava.yaml), `corax56.yaml`, `corney-island.yaml`, `LambBT.yaml`, `Lintilla.yaml`, `owl.yaml`, `porcupine_6x3.yaml`, `splave-ferris.yml`, `tempest.yaml`, `travis-ergogen-numpad.yml`, `tutorial.yml`, `Wubbo.yaml`, `ai_generated_numpad.yaml` (formerly misnamed `mantis.yaml` — an AI-generated numpad, not the Mantis keyboard).

## Housekeeping notes

- Generated build artifacts (tutorial DXF/JSCAD outputs) and confirmed duplicates were moved to [`../archive/working_samples/`](../archive/working_samples/) during the 2026-07 consolidation.
- This README absorbs the useful content of the former root `COLLECTION_SUMMARY.md`.