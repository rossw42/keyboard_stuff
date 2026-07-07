# TODO — KLE_SCAD_Ergogen

Date: 2026-06-14

This file captures short-term tasks and quick commands to exercise and maintain the `kle-scad-ergogen` converter located in this folder.

## Quick checklist

- [ ] Run smoke test locally: `npm install` then `npm test`
- [ ] Add `engines.node` to `package.json` (specify supported Node version)
- [ ] Add CI workflow (GitHub Actions) to run `npm ci` + `npm test` on push
- [ ] Add unit tests for `src/` modules (kleParser, coordinateTransform, ergogenGenerator)
- [ ] Add CONTRIBUTING.md and basic developer notes
- [ ] Consider `npm audit` and dependency refresh (update `@ijprest/kle-serial`, `commander`, `js-yaml` if needed)
- [ ] Optional: add TypeScript types or migrate to ESM (longer-term)

## Smoke test (copy/paste)

```bash
cd "D:\GitHub\keyboard_stuff\KLE_SCAD_Ergogen"
npm install
npm test
```

If you prefer reproducible installs in CI or dev machines, use:

```bash
npm ci
npm test
```

## Notes

- CLI entry point: `index.js` (also provides a `kle-to-ergogen` bin) 
- Examples: check the `examples/` and `test_40percent.*` files
- Output: YAML files are generated next to input KLE files by default

## Where to look

- Code: `src/` — parser and generator modules
- Entry: `index.js`
- Config: `package.json`, `package-lock.json`

---

If you want, I can run the smoke test now, or add a minimal GitHub Actions workflow and open a PR in this repo. What would you like next?