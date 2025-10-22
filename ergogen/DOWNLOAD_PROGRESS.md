# Ergogen Config Download Progress

*Started: October 22, 2025*

## Successfully Downloaded

### 1. Absolem ✅
- **Repo**: https://github.com/mrzealot/absolem
- **File**: absolem.yaml
- **Location**: `working_samples/absolem/config.yaml`
- **Category**: Unibody, Original Ergogen keyboard
- **Features**: Multi-zone, thumb cluster, multiple switch support (MX/Alps/Choc)

### 2. Samoklava ✅
- **Repo**: https://github.com/soundmonster/samoklava
- **File**: config.yaml
- **Location**: `working_samples/samoklava/config.yaml`
- **Category**: Split keyboard
- **Features**: Choc hotswap, 3x5+3 layout, TRRS, battery support

## Pending Download

### High Priority (Top 10 by stars)

3. **Cephalopoda** (232⭐)
   - Multiple variants in subdirectories
   - Path: `Idiosepius thailandicus/choc/` or `/chocmini/`
   - Need to explore subdirectories

4. **Kaly** (209⭐)
   - Path: Need to check `KalyPCB/` or `Layout/` directories
   - 42-key split keyboard

5. **Corax** (131⭐)
   - Path: `corax56/ergogen/` directory
   - Wireless, scrollwheels, advanced features

6. **Mantis** (117⭐)
   - Hex layout keyboard
   - Need to find config location

7. **Trochilidae** (112⭐)
   - Path: `berylline/berylline.yml` ✅ Found
   - Also has `rufous/` variant
   - Hummingbird recreation

8. **Ergogen-footprints** (101⭐)
   - This is a footprint library, not a keyboard
   - Skip for keyboard collection

9. **Tern** (truncated in API)
   - 30-key minimal keyboard
   - Need to check repo

10. **kb_think_corney** (34⭐ from page 2)
    - Corne/Crkbd clone with trackpoint
    - Ergogen v4

### Medium Priority (Page 2)

11. **archimedes-tux** (31⭐)
12. **jonkey** (30⭐)
13. **quokka** (28⭐) - Split ortholinear for small hands
14. **Tiny20** (27⭐) - 20-key compact
15. **chonkv** (26⭐) - 58-key Choc, FlatFootFox tutorial keyboard!

## File Naming Patterns Found

- `config.yaml` - Most common
- `*.yml` - Some use .yml extension
- `ergogen/config.yaml` - In subdirectory
- Named after keyboard: `berylline.yml`, `absolem.yaml`

## Directory Structures Found

1. **Root level config**: samoklava, absolem
2. **Subdirectory per variant**: cephalopoda, trochilidae, corax
3. **ergogen/ subfolder**: corax56/ergogen/

## Next Steps

1. Download configs from subdirectories
2. Organize by category:
   - `working_samples/split/` - Split keyboards
   - `working_samples/unibody/` - Single piece
   - `working_samples/minimal/` - 30 keys or less
   - `working_samples/advanced/` - Special features
3. Create README for each with metadata
4. Test in ergogen.xyz

## API Limits

- GitHub API: 60 requests/hour unauthenticated
- Raw file downloads: No limit
- Current usage: ~15 requests so far

