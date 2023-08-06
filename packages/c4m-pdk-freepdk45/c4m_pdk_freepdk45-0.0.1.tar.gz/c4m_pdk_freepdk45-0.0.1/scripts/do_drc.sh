#!/bin/sh
# File name is $(VERIFICATION_DIR)/__lib__/drc/__cell__.drc.out
cell=$(basename $1 .drc.out)
lib=$(basename $(dirname $(dirname $1)))
gds_file=$VIEWS_DIR/$lib/gds/$cell.gds

$KLAYOUT_DIR/bin/drc_FreePDK45 $gds_file $1
