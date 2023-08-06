# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from c4m.flexcell.library import Library

from .pdkmaster import tech, cktfab, layoutfab

__all__ = ["flexlib"]

prims = tech.primitives
flexlib = Library(lambda_=0.02).convert2pdkmaster("FlexLib",
    tech=tech, cktfab=cktfab, layoutfab=layoutfab,
    nmos=prims.nmos_vtg, pmos=prims.pmos_vtg,
    nimplant=prims.nimplant, pimplant=prims.pimplant,
)
