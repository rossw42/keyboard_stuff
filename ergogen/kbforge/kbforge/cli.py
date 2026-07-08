"""
kbforge CLI.

Convert a KLE JSON layout into downstream artifacts.

Two-step workflow:

    # Step 1 — generate the Ergogen config, docs and canonical JSON:
    python -m kbforge board.json -o out/

    # Step 2 — review/edit out/<name>.ergogen.yaml, then run Ergogen on it
    # (also renders the case .jscad models to STL via @jscad/cli):
    python -m kbforge out/<name>.ergogen.yaml -o out/

Formats:
    ergogen  -> <name>.ergogen.yaml   (points+outlines+plate+pcb+cases; run
                                       it through Ergogen with step 2 above
                                       once you're happy with it)
    docs     -> <name>.md             (build docs: matrix, BOM, instructions)
    json     -> <name>.layout.json    (canonical intermediate model)
    scad     -> <name>.scad           (standalone OpenSCAD plate & case,
                                       independent of Ergogen)
    stl      -> <name>.plate.stl / .bottom.stl / .walls.stl
                                      (rendered from the .scad via OpenSCAD;
                                       alternative to the Ergogen case STLs)
    hotswap  -> <name>.hotswap.scad   (hotswap_pcb_generator layout file)

Default formats: ergogen docs json. Use `-f all` for everything.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .kle_parser import KLEParseError, parse_kle_file
from .generators import docs as docs_gen
from .generators import ergogen as ergogen_gen
from .generators import json_out as json_gen
from .generators import ergogen_build
from .generators import scad as scad_gen
from .generators import stl as stl_gen
from .generators import converter_scad as converter_gen

ALL_FORMATS = ("ergogen", "scad", "stl", "hotswap", "docs", "json", "converter")
DEFAULT_FORMATS = ("ergogen", "docs", "json")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kbforge",
        description="Convert a KLE JSON layout into Ergogen, OpenSCAD, "
                    "hotswap-PCB and documentation outputs. Pass a generated "
                    ".ergogen.yaml instead to run Ergogen on it (build step).",
        epilog="Example: python -m kbforge examples/numpad.json -o out/  "
               "then: python -m kbforge out/numpad.ergogen.yaml -o out/",
    )
    parser.add_argument("input",
                        help="Input KLE JSON file, or a generated "
                             ".ergogen.yaml to build with Ergogen")
    parser.add_argument("-o", "--out-dir", default=None,
                        help="Output directory (default: alongside input)")
    parser.add_argument("-n", "--name", default=None,
                        help="Base name for outputs (default: from KLE "
                             "metadata or input filename)")
    parser.add_argument("-f", "--formats", nargs="+",
                        choices=ALL_FORMATS + ("all",),
                        default=list(DEFAULT_FORMATS), metavar="FMT",
                        help=f"Formats to generate: {', '.join(ALL_FORMATS)}, all "
                             f"(default: {' '.join(DEFAULT_FORMATS)})")
    parser.add_argument("-u", "--unit", type=float, default=19.05,
                        help="Key unit size in mm (default: 19.05)")
    parser.add_argument("--switch-cutout", type=float, default=None,
                        metavar="MM",
                        help="Plate cutout size for normal keys in mm "
                             "(default: 14.0 MX; use 13.8 for Choc)")
    parser.add_argument("--converter-keys", nargs="+", default=None,
                        metavar="SPEC",
                        help="Mark keys as PG1350->PG1425 switch-converter "
                             "positions: 'all', matrix refs like r0c3, or "
                             "key labels (case-insensitive). Converter keys "
                             "get a 15.2mm plate opening and a PG1425 PCB "
                             "footprint; add '-f converter' for the "
                             "printable adapter panel / integrated plate.")
    parser.add_argument("-b", "--build", action="store_true",
                        help="(deprecated for KLE JSON inputs — the build is "
                             "now a separate step) Pass the generated "
                             ".ergogen.yaml as the input to run Ergogen on it "
                             "and render the case .jscad models to STL "
                             "(needs Node.js; uses `ergogen` or `npx ergogen` "
                             "plus `npx @jscad/cli@1`)")
    parser.add_argument("--footprints", default=None, metavar="DIR",
                        help="Local clone of ceoloide/ergogen-footprints to "
                             "copy into the build (default: ERGOGEN_FOOTPRINTS "
                             "env var, else cloned from GitHub on first build)")
    parser.add_argument("--openscad", default=None, metavar="EXE",
                        help="Path to the OpenSCAD executable used for the "
                             "stl format (default: auto-detect from PATH, "
                             "OPENSCAD_PATH, or common install locations)")
    parser.add_argument("--stl-parts", nargs="+", default=list(stl_gen.DEFAULT_PARTS),
                        choices=("plate", "bottom", "walls", "all"), metavar="PART",
                        help="Case parts to render as STL: plate bottom walls all "
                             "(default: plate bottom walls)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress the summary output")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    return parser


def run_ergogen_build(yaml_path: Path, args: argparse.Namespace) -> int:
    """Build step: run Ergogen on an existing (reviewed) .ergogen.yaml."""
    if not yaml_path.is_file():
        print(f"error: config not found: {yaml_path}", file=sys.stderr)
        return 1
    out_dir = Path(args.out_dir) if args.out_dir else yaml_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        outputs = ergogen_build.build(
            ergogen_yaml=yaml_path,
            out_dir=out_dir,
            footprints=args.footprints,
            quiet=args.quiet,
        )
    except ergogen_build.ErgogenNotFound as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ergogen_build.ErgogenBuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not args.quiet:
        for path in outputs:
            print(f"  wrote {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if "all" in args.formats:
        args.formats = list(ALL_FORMATS)

    input_path = Path(args.input)

    # Build step: a .ergogen.yaml input runs Ergogen instead of generating.
    if input_path.suffix.lower() in (".yaml", ".yml"):
        return run_ergogen_build(input_path, args)

    try:
        layout = parse_kle_file(str(input_path), name=args.name or "")
    except KLEParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    layout.unit = args.unit
    if not layout.name or layout.name == "keyboard":
        layout.name = args.name or input_path.stem

    if args.converter_keys:
        marked = layout.mark_converters(args.converter_keys)
        if marked == 0:
            print("warning: --converter-keys matched no keys "
                  f"(specs: {' '.join(args.converter_keys)})", file=sys.stderr)

    ergogen_options = {}
    if args.switch_cutout is not None:
        ergogen_options["switch_cutout"] = args.switch_cutout

    slug = docs_gen._slug(layout.name)
    out_dir = Path(args.out_dir) if args.out_dir else input_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    filenames = {
        "ergogen": f"{slug}.ergogen.yaml",
        "scad": f"{slug}.scad",
        "hotswap": f"{slug}.hotswap.scad",
        "converter": f"{slug}.converter.scad",
        "docs": f"{slug}.md",
        "json": f"{slug}.layout.json",
    }

    written: list[Path] = []

    def write(kind: str, content: str) -> None:
        path = out_dir / filenames[kind]
        path.write_text(content, encoding="utf-8")
        written.append(path)

    if "ergogen" in args.formats:
        write("ergogen", ergogen_gen.generate_ergogen_yaml(layout, ergogen_options))
    if "scad" in args.formats or "stl" in args.formats:
        # stl rendering needs the .scad on disk, so scad is implied by stl
        write("scad", scad_gen.generate_scad(layout))
    if "hotswap" in args.formats:
        write("hotswap", scad_gen.generate_hotswap_layout(layout))
    if "converter" in args.formats:
        if layout.converters:
            conv_opts = {}
            if args.switch_cutout is not None:
                conv_opts["switch_cutout"] = args.switch_cutout
            write("converter", converter_gen.generate_converter_scad(layout, conv_opts))
        else:
            print("warning: skipping converter output — no keys marked "
                  "(use --converter-keys)", file=sys.stderr)
    if "json" in args.formats:
        write("json", json_gen.generate_layout_json(layout))
    if "docs" in args.formats:
        # docs last so it can reference the actual filenames generated
        write("docs", docs_gen.generate_docs(layout, outputs=filenames))

    if args.build:
        print("note: --build no longer runs Ergogen during generation. "
              "Review the generated .ergogen.yaml first, then build it with:\n"
              f"  python -m kbforge {out_dir / filenames['ergogen']} -o {out_dir}",
              file=sys.stderr)

    if "stl" in args.formats:
        try:
            written.extend(stl_gen.render_stls(
                scad_path=out_dir / filenames["scad"],
                out_dir=out_dir,
                base_name=slug,
                parts=args.stl_parts,
                openscad=args.openscad,
                quiet=args.quiet,
            ))
        except stl_gen.OpenSCADNotFound as exc:
            print(f"warning: skipping STL output — {exc}", file=sys.stderr)
        except stl_gen.STLRenderError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if not args.quiet:
        stats = layout.stats()
        print(f"{layout.name}: {stats['switch_count']} switches, "
              f"matrix {stats['matrix_rows']}x{stats['matrix_cols']}, "
              f"{stats['size_mm'][0]} x {stats['size_mm'][1]} mm"
              + (f", {stats['stabilized_keys']} stabilized" if stats['stabilized_keys'] else "")
              + (f", {stats['converter_keys']} converter" if stats.get('converter_keys') else ""))
        for path in written:
            print(f"  wrote {path}")
        if "ergogen" in args.formats:
            print(f"\nNext: review/edit {out_dir / filenames['ergogen']}, "
                  f"then run Ergogen on it (also renders case STLs):")
            print(f"  python -m kbforge {out_dir / filenames['ergogen']} -o {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())