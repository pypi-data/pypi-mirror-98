#!/bin/sh
$YOSYS <<EOF
read_liberty -lib -ignore_miss_dir -setattr blackbox ${LIBERTY_FILE}

read_verilog ${TOP_CELL}.v

# High-level synthesis
synth -flatten -top ${TOP_CELL}

# Map register flops
dfflibmap -liberty ${LIBERTY_FILE}
opt

# Map combinatorial cells, standard script
abc -liberty ${LIBERTY_FILE} -script +strash;scorr;ifraig;retime,{D};strash;dch,-f;map,-M,1,{D}
setundef -zero

clean -purge
write_blif ${BLIF_FILE}
write_verilog ${VERILOG_OUT}
stat
EOF

