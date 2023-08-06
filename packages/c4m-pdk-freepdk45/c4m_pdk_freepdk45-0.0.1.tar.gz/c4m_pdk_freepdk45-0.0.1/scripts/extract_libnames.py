# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from c4m.pdk.freepdk45 import __libs__

for lib in __libs__:
    print(lib.name)
