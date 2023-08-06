#!/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
import os

from c4m.pdk import freepdk45

viewsdir = os.environ["VIEWS_DIR"]
for lib in freepdk45.__libs__:
    spicedir = f"{viewsdir}/{lib.name}/spice"
    with open(f"{spicedir}/{lib.name}.spi", "w") as f_lib:
        f_lib.write(f"* {lib.name}\n")
        for cell in lib.cells:
            pyspicesubckt = freepdk45.pyspicefab.new_pyspicesubcircuit(circuit=cell.circuit)
            s = f"* {cell.name}\n" + str(pyspicesubckt)
            f_lib.write("\n" + s)
            with open(f"{spicedir}/{cell.name}.spi", "w") as f_cell:
                f_cell.write(s)
print("Spice exported")
