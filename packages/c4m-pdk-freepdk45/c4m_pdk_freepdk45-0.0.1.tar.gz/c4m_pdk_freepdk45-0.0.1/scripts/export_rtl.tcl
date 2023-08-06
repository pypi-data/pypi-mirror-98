# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
set lang $::env(RTL_LANG)

avt_config simToolModel hspice
avt_LoadFile $::env(C4M_INST_DIR)/freepdk45_nom.spi spice
avt_config avtVddName "vdd"
avt_config avtVssName "vss"
avt_config yagNoSupply "yes"
if {$lang == "verilog"} {
    avt_config avtOutputBehaviorFormat "vlg"
    set map {spice verilog .spi .v}
    set suffix v
    set comment "//"
} elseif {$lang == "vhdl"} {
    avt_config avtOutputBehaviorFormat "vhd"
    set map {spice vhdl .spi .vhdl}
    set suffix vhd
    set comment "--"
} else {
    puts "Unrecognized RTL language $lang"
    exit 20
}

foreach spice_file $::env(SPICE_FILES) {
    avt_LoadFile $spice_file spice
    set rtl_file [string map $map $spice_file]
    set cell [string map {.spi ""} [file tail $spice_file]]
    if {[string match "sff1*" $cell]} {
        inf_SetFigureName $cell
        inf_MarkSignal sff_m "FLIPFLOP+MASTER"
        inf_MarkSignal sff_s SLAVE
    }
    set out_file "$cell.$suffix"
    yagle $cell
    if [file exists $out_file] {
        file copy -force $out_file $rtl_file
    } else {
        set f [open $rtl_file w]
        puts $f "$comment no model for $cell"
    }
}

puts "$lang files generated"
