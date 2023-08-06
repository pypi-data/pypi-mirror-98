# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
import os
import CRL

from helpers import setNdaTopDir

ndadir = os.environ["NDA_TOP"]
setNdaTopDir(ndadir)

from NDA.node45 import freepdk45_c4m as freepdk45

freepdk45.setup()

viewsdir = os.environ["VIEWS_DIR"]

for setup in freepdk45.__lib_setups__:
    lib = setup()
    gdsdir = "{}/{}/gds".format(viewsdir, lib.getName())
    olddir = os.curdir
    os.chdir(gdsdir)
    for cell in lib.getCells():
        CRL.Gds.save(cell)
    os.chdir(olddir)

print("GDS files written")