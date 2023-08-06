# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
import os

from pdkmaster import _util
from pdkmaster.io.export import pyspice

__all__ = ["pyspicefab", "pyspice_factory"]


class _PySpiceFactory(pyspice.PySpiceFactory):
    def new_pyspicecircuit(self, **kwargs):
        corner = kwargs["corner"]
        if isinstance(corner, str) or (not _util.is_iterable(corner)):
            corner = (corner,)
        return super().new_pyspicecircuit(**kwargs)


pyspicefab = pyspice_factory = _PySpiceFactory(
    libfile=os.path.dirname(__file__)+"/freepdk45.spi",
    corners=("NOM", "FF", "SS",),
    conflicts={
        "NOM": ("FF", "SS"),
        "FF": ("NOM", "SS"),
        "SS": ("NOM", "FF"),
    },
)
