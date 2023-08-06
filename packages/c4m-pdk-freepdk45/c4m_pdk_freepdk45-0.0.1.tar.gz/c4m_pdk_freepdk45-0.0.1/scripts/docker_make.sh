#!/bin/sh
echo "The FreePDK45 PDKMaster PDK is already installed in docker image"
make coriolis klayout spice gds verilog vhdl
echo "liberty file generation currently does not work in docker"
echo "Copying premade files"
cp -r .reserve/liberty views/FreePDK45/FlexLib/
make drc
echo "Currenlty LVS for cells without bulk/well contacts fails"
make -k lvs
