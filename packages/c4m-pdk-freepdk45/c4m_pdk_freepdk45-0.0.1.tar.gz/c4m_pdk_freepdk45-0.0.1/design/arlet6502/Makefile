export TOP_DIR := $(realpath ../..)
PWD := $(realpath .)

export TOP_CELL := Arlet6502
TOP_CELL_LC = arlet6502

CORIOLIS_PYTHON ?= python2

LOG_DIR := $(PWD)/log
#YOSYS := yosys -m ghdl
export YOSYS := yosys

.PHONY: all
all: pnr
	@echo "All built"
	@grep "Completion Ratio" $(wildcard $(LOG_DIR)/*)

SYNTH_DIR := $(PWD)/synth
SOURCE_FILES := \
  $(PWD)/Arlet6502.v \
  $(PWD)/ALU.v \
  $(PWD)/cpu_syncreset.v \
  $(PWD)/Makefile \
#END SOURCE_FILES
BLIF_FILE := $(SYNTH_DIR)/$(TOP_CELL_LC).blif

.PHONY: synth
synth: $(BLIF_FILE)

export LIBERTY_FILE := $(TOP_DIR)/views/FreePDK45/FlexLib/liberty/FlexLib_nom.lib
$(BLIF_FILE): $(SOURCE_FILES) ./run_yosys.sh | $(SYNTH_DIR) $(LOG_DIR)
	@echo "Synthesizing design for Coriolis"
	@env \
	  BLIF_FILE=$@ VERILOG_OUT=$(SYNTH_DIR)/$(TOP_CELL_LC)synth.v \
	  ./run_yosys.sh | tee $(LOG_DIR)/yosys_synth.log | egrep -e '^[1-9]'


export NDA_DIR := $(TOP_DIR)/coriolis/techno

# Coriolis
PNR_SCRIPT := $(PWD)/pnr.py
PNR_DIR := $(PWD)/pnr
GDS_FILE := $(PWD)/$(TOP_CELL_LC)_pnr.gds

.PHONY: pnr
pnr: $(GDS_FILE)

$(GDS_FILE): $(BLIF_FILE) $(PNR_SCRIPT) | $(PNR_DIR) $(LOG_DIR)
	@echo "Coriolis P&R"
	@cp $(BLIF_FILE) $(PNR_DIR)
	@cd $(PNR_DIR); CELL=$(TOP_CELL_LC) $(CORIOLIS_PYTHON) $(PNR_SCRIPT) | tee $(LOG_DIR)/pnr.log
	@cp $(PNR_DIR)/$(TOP_CELL_LC)_pnr.gds $@

# Misc.
clean::
	@echo "Cleaning up"
	@rm -fr $(SYNTH_DIR) $(PNR_DIR) $(GDS_FILE) $(LOG_DIR)

$(SYNTH_DIR) $(PNR_DIR) $(LOG_DIR):
	@echo "Creating directory $@"
	@mkdir -p $@
