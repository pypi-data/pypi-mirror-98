#!/bin/sh
# File name is $(VERIFICATION_DIR)/__lib__/drc/__cell__.lvs.out
cell=$(basename $1 .lvs.out)
lib=$(basename $(dirname $(dirname $1)))
gds_file=$VIEWS_DIR/$lib/gds/$cell.gds
spice_file=$VIEWS_DIR/$lib/spice/$cell.spi

$KLAYOUT_DIR/bin/lvs_FreePDK45 $gds_file $spice_file $1
