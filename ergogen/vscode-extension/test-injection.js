/**
 * Standalone test of the live-preview footprint injection logic.
 * Simulates what extension.js does: load the global ergogen module,
 * inject footprints from a footprints/ folder, then process a config
 * that references ceoloide/* footprints.
 *
 * Usage: node test-injection.js <path-to-config.yaml>
 * (a `footprints` folder must exist next to the config, as in the CLI convention)
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const configPath = process.argv[2];
if (!configPath) {
  console.error("Usage: node test-injection.js <config.yaml>");
  process.exit(1);
}

// --- resolveErgogenModule (same as extension) ---
const npmRoot = execSync("npm root -g", { encoding: "utf8", shell: true }).trim();
const ergogenPath = path.join(npmRoot, "ergogen");
const ergogen = require(ergogenPath);
console.log(`Loaded ergogen v${ergogen.version} from ${ergogenPath}`);

// --- findFootprintsDir (same as extension) ---
function findFootprintsDir(startDir) {
  let dir = startDir;
  for (let i = 0; i < 4; i++) {
    const candidate = path.join(dir, "footprints");
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
      return candidate;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

// --- getFootprintSources (same as extension; library path via env or default) ---
const CEOLOIDE_LIB = process.env.CEOLOIDE_LIB || "D:\\GitHub2\\ergogen-footprints";

function getFootprintSources(documentPath) {
  const sources = [];
  const local = findFootprintsDir(path.dirname(documentPath));
  if (local) sources.push({ dir: local, prefix: "" });
  if (fs.existsSync(CEOLOIDE_LIB)) {
    sources.push({ dir: CEOLOIDE_LIB, prefix: "ceoloide" });
  }
  return sources;
}

// --- injectCustomFootprints (same as extension) ---
function injectCustomFootprints(documentPath) {
  const sources = getFootprintSources(documentPath);
  if (sources.length === 0) {
    console.log("No footprint sources found");
    return 0;
  }

  let makerjs = null;
  try {
    makerjs = require(require.resolve("makerjs", { paths: [ergogenPath] }));
  } catch (e) {}

  const fakeRequire = (name) => {
    if (name.endsWith("package.json")) return { version: ergogen.version };
    if (name === "makerjs" && makerjs) return makerjs;
    throw new Error(`Unknown dependency "${name}"`);
  };

  let injected = 0;
  const walk = (dir, prefix) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === ".git" || entry.name === "node_modules") continue;
        walk(full, prefix ? `${prefix}/${entry.name}` : entry.name);
      } else if (entry.name.endsWith(".js")) {
        const name = (prefix ? `${prefix}/` : "") + entry.name.split(".")[0];
        try {
          const text = fs.readFileSync(full, "utf8");
          const parsed = new Function(
            "require",
            "const module = {};\n\n" + text + "\n\nreturn module.exports;"
          )(fakeRequire);
          ergogen.inject("footprint", name, parsed);
          injected++;
        } catch (e) {
          console.warn(`  ⚠ ${name}: ${e.message}`);
        }
      }
    }
  };
  for (const source of sources) {
    walk(source.dir, source.prefix);
  }
  console.log(
    `Injected ${injected} custom footprints from: ` +
      sources.map((s) => `${s.dir}${s.prefix ? ` as "${s.prefix}/*"` : ""}`).join(", ")
  );
  return injected;
}

// --- run ---
(async () => {
  injectCustomFootprints(path.resolve(configPath));
  const raw = fs.readFileSync(configPath, "utf8");
  try {
    const results = await ergogen.process(raw, true, (s) => console.log("  " + s));
    console.log("\n✅ process() succeeded");
    console.log("  demo svg:", results.demo && results.demo.svg ? "yes" : "no");
    console.log("  outlines:", Object.keys(results.outlines || {}).join(", "));
    console.log("  pcbs:", Object.keys(results.pcbs || {}).join(", "));
  } catch (e) {
    console.error("\n❌ process() failed:", e.message);
    process.exit(1);
  }
})();