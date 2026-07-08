"""
Output generators for kbforge.

Each generator takes the shared `Layout` model and produces one artifact:

  ergogen.generate_ergogen_yaml(layout)   -> Ergogen v4 YAML (points, outlines,
                                              plate, PCB, cases)
  ergogen_build.build(yaml_path, out_dir) -> runs a local Ergogen on the config
                                              and renders cases/*.jscad to STL
                                              via `npx @jscad/cli@1`
  scad.generate_scad(layout)              -> standalone OpenSCAD plate & case
  scad.generate_hotswap_layout(layout)    -> hotswap_pcb_generator layout .scad
  stl.render_stls(scad_path, ...)         -> STL files rendered via OpenSCAD CLI
  docs.generate_docs(layout)              -> Markdown documentation
  json_out.generate_layout_json(layout)   -> canonical layout JSON
"""

from . import ergogen, ergogen_build, scad, stl, docs, json_out

__all__ = ["ergogen", "ergogen_build", "scad", "stl", "docs", "json_out"]
