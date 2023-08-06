#!/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
import os
from os.path import dirname, relpath, basename
from textwrap import dedent
from xml.etree.ElementTree import ElementTree

from pdkmaster.io.export.klayout import Generator
from c4m.pdk import freepdk45

drcfile = os.environ["KLAYOUT_DRC_FILE"]
drcscript = os.environ["KLAYOUT_DRC_SCRIPT"]
extractfile = os.environ["KLAYOUT_EXTRACT_FILE"]
extractscript = os.environ["KLAYOUT_EXTRACT_SCRIPT"]
lvsfile = os.environ["KLAYOUT_LVS_FILE"]
lvsscript = os.environ["KLAYOUT_LVS_SCRIPT"]
lydrcfile = os.environ["KLAYOUT_DRC_LYDRC_FILE"]
lyextractfile = os.environ["KLAYOUT_EXTRACT_LYLVS_FILE"]
lytfile = os.environ["KLAYOUT_LYT_FILE"]

expo = Generator(freepdk45.tech, export_name=f"C4M.{freepdk45.tech.name}")()
with open(drcfile, "w") as f:
    f.write(expo["drc"])
with open(drcscript, "w") as f:
    relfile = f"{relpath(dirname(drcfile), dirname(drcscript))}/{basename(drcfile)}"
    f.write(dedent(f"""
        #!/bin/sh
        d=`dirname $0`
        deck=`realpath $d/{relfile}`

        if [ $# -ne 2 ]
        then
            echo "Usage `basename $0` input report"
            exit 20
        fi

        export SOURCE_FILE=$1 REPORT_FILE=$2
        klayout -b -r ${{deck}}
    """[1:]))
with open(extractfile, "w") as f:
    f.write(expo["extract"])
with open(extractscript, "w") as f:
    relfile = f"{relpath(dirname(extractfile), dirname(extractscript))}/{basename(extractfile)}"
    f.write(dedent(f"""
        #!/bin/sh
        d=`dirname $0`
        deck=`realpath $d/{relfile}`

        if [ $# -ne 2 ]
        then
            echo "Usage `basename $0` input spice_out"
            exit 20
        fi

        export SOURCE_FILE=$1 SPICE_FILE=$2
        klayout -b -r ${{deck}}
    """[1:]))
with open(lvsfile, "w") as f:
    f.write(expo["lvs"])
with open(lvsscript, "w") as f:
    relfile = f"{relpath(dirname(lvsfile), dirname(lvsscript))}/{basename(lvsfile)}"
    f.write(dedent(f"""
        #!/bin/sh
        d=`dirname $0`
        deck=`realpath $d/{relfile}`

        if [ $# -ne 3 ]
        then
            echo "Usage `basename $0` gds spice report"
            exit 20
        fi

        export SOURCE_FILE=`realpath $1` SPICE_FILE=`realpath $2` REPORT_FILE=$3
        klayout -b -r ${{deck}}
    """[1:]))
et = ElementTree(expo["ly_drc"])
et.write(lydrcfile, encoding="utf-8", xml_declaration=True)
et = ElementTree(expo["ly_extract"])
et.write(lyextractfile, encoding="utf-8", xml_declaration=True)
et = ElementTree(expo["ly_tech"])
et.write(lytfile, encoding="utf-8", xml_declaration=True)

print("klayout files exported")
