# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
set viewsdir $::env(VIEWS_DIR)
set out $::env(OUT)
set lib $::env(LIB)
set cells $::env(${lib}_CELLS)
set corner $::env(CORNER)

avt_config simToolModel hspice
avt_config avtVddName "vdd"
avt_config avtVssName "vss"
avt_config tasBefig yes
avt_config tmaDriveCapaout yes
avt_config avtPowerCalculation yes
avt_config simSlope 20e-12
if {$corner == "nom"} {
    avt_config simPowerSupply 1.0
    avt_config simTemperature 25
    avt_LoadFile $::env(C4M_INST_DIR)/freepdk45_nom.spi spice
    avt_config tmaLibraryName ${lib}_nom
} elseif {$corner == "fast"} {
    avt_config simPowerSupply 1.1
    avt_config simTemperature -20
    avt_LoadFile $::env(C4M_INST_DIR)/freepdk45_ff.spi spice
    avt_config tmaLibraryName ${lib}_ff
} elseif {$corner == "slow"} {
    avt_config simPowerSupply 0.9
    avt_config simTemperature 85
    avt_LoadFile $::env(C4M_INST_DIR)/freepdk45_ss.spi spice
    avt_config tmaLibraryName ${lib}_ss
} else {
    puts "Unsupported corner"
    exit 20
}

avt_LoadFile $viewsdir/$lib/spice/$lib.spi spice

foreach cell $cells {
    set verilogfile $viewsdir/$lib/verilog/$cell.v

    if {[string match "sff1*" $cell]} {
        # TODO: make these settings configurable
        set beh_fig NULL
        inf_SetFigureName $cell
        inf_MarkSignal sff_m "FLIPFLOP+MASTER"
        inf_MarkSignal sff_s SLAVE
        create_clock -period 3000 ck
    } elseif {[string match "*latch*" $cell]} {
        set beh_fig NULL
    } else {
        set beh_fig [avt_LoadBehavior $verilogfile verilog]
    }
    set tma_fig [tma_abstract [hitas $cell] $beh_fig]

    lappend tma_list $tma_fig
    lappend beh_list $beh_fig
}

lib_drivefile $tma_list $beh_list $out max

puts "liberty file generated for $lib"
