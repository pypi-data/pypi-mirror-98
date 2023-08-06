# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
export PWD := $(realpath .)
SCRIPTS_DIR := $(PWD)/scripts
TMP_DIR := $(PWD)/tmp

# Runtime environment has to be configured in Makefile.conf.
# Need for changes in this file should be reported upstream.
include Makefile.conf

SITE_PACKAGES_DIR := $(shell $(PYTHON_PDKMASTER) -c "import site; print(site.getsitepackages()[0])")
# Directories that need to be created before other targets
MKDIRS := $(TMP_DIR)
# Files and directories that are removed during clean
RMFILES := $(TMP_DIR)

###

.PHONY: all
all: install coriolis klayout spice gds verilog vhdl liberty

# Verification is not done by default, it should only be used to discover bugs
.PHONY: verif
verif: drc lvs

###

export C4M_INST_DIR := $(SITE_PACKAGES_DIR)/c4m/pdk/freepdk45
PYFILES := $(shell find c4m -name '*.py' -o -name '*.spi')

.PHONY: install
install: $(C4M_INST_DIR)

$(C4M_INST_DIR): $(PYFILES) MANIFEST.in
	@echo "Installing python package"
	@$(PIP_PDKMASTER) install $(PIP_PDKMASTER_INSTOPTS) .

###

export VIEWS_DIR := $(PWD)/views/FreePDK45
export VERIFICATION_DIR := $(PWD)/verification
RMFILES += $(VIEWS_DIR)

# Extract and store some paths and other makefile variables
# in include makefiles.
# Caching these values in include files avoids having to run
# several python commands on each make run.

export PDKMASTER_MAKEFILE := $(PWD)/Makefile.pdkmaster
RMFILES += $(PDKMASTER_MAKEFILE)
$(PDKMASTER_MAKEFILE): $(SCRIPTS_DIR)/gen_pdkmaster_makefile.py
	@echo "Generating pdkmaster support files"
	@$(PYTHON_PDKMASTER) $<

export FLEXCELL_MAKEFILE := $(PWD)/Makefile.flexcell
RMFILES += $(FLEXCELL_MAKEFILE)
$(FLEXCELL_MAKEFILE): $(SCRIPTS_DIR)/gen_flexcell_makefile.py
	@echo "Generating flexcell support files"
	@$(PYTHON_PDKMASTER) $<

export LIBS_MAKEFILE := $(PWD)/Makefile.libs
RMFILES += $(LIBS_MAKEFILE)
$(LIBS_MAKEFILE): $(SCRIPTS_DIR)/gen_libs_makefile.py
	@echo "Generating libs support files"
	@$(PYTHON_PDKMASTER) $<

-include $(PDKMASTER_MAKEFILE)
-include $(FLEXCELL_MAKEFILE)
-include $(LIBS_MAKEFILE)

###

CORIOLIS_DIR := $(PWD)/coriolis
RMFILES += $(CORIOLIS_DIR)
export NDA_TOP := $(CORIOLIS_DIR)/techno
export CORIOLIS_TECH_DIR := $(NDA_TOP)/etc/coriolis2/NDA/node45/freepdk45_c4m
CORIOLIS_INIT_FILES := \
	$(NDA_TOP)/etc/coriolis2/NDA/__init__.py \
	$(NDA_TOP)/etc/coriolis2/NDA/node45/__init__.py \
# CORIOLIS_INIT_FILES end
CORIOLIS_GEN_FILES := \
  $(CORIOLIS_TECH_DIR)/__init__.py \
  $(CORIOLIS_TECH_DIR)/techno.py \
  $(addprefix $(CORIOLIS_TECH_DIR)/,$(addsuffix .py,$(LIB_NAMES))) \
# CORIOLIS_GEN_FILES end
CORIOLIS_EXPORT_SCRIPT := $(SCRIPTS_DIR)/export_coriolis.py

.PHONY: coriolis
coriolis: $(CORIOLIS_GEN_FILES)
$(CORIOLIS_GEN_FILES): | $(CORIOLIS_TECH_DIR) $(CORIOLIS_INIT_FILES)
MKDIRS += $(CORIOLIS_TECH_DIR)
$(CORIOLIS_INIT_FILES): | $(CORIOLIS_TECH_DIR)
	@touch $@
$(CORIOLIS_GEN_FILES): $(C4M_INST_DIR) $(PDKMASTER_PATH) $(FLEXCELL_PATH)
$(CORIOLIS_GEN_FILES): $(CORIOLIS_EXPORT_SCRIPT)
	@echo "Generating coriolis files"
	@$(PYTHON_PDKMASTER) $(CORIOLIS_EXPORT_SCRIPT)

###

export KLAYOUT_DIR := $(PWD)/klayout
RMFILES += $(KLAYOUT_DIR)
KLAYOUT_TECH_DIR := $(KLAYOUT_DIR)/tech/C4M.FreePDK45
export KLAYOUT_LYT_FILE := $(KLAYOUT_TECH_DIR)/C4M.FreePDK45.lyt
KLAYOUT_DRC_DIR := $(KLAYOUT_TECH_DIR)/drc
export KLAYOUT_DRC_LYDRC_FILE := $(KLAYOUT_DRC_DIR)/DRC.lydrc
KLAYOUT_LVS_DIR := $(KLAYOUT_TECH_DIR)/lvs
export KLAYOUT_EXTRACT_LYLVS_FILE := $(KLAYOUT_LVS_DIR)/Extract.lylvs
KLAYOUT_LVS_DIR := $(KLAYOUT_TECH_DIR)/lvs
KLAYOUT_SHARE_DIR := $(KLAYOUT_DIR)/share/klayout/
KLAYOUT_BIN_DIR := $(KLAYOUT_DIR)/bin
export KLAYOUT_DRC_FILE := $(KLAYOUT_SHARE_DIR)/FreePDK45.drc
export KLAYOUT_DRC_SCRIPT := $(KLAYOUT_BIN_DIR)/drc_FreePDK45
export KLAYOUT_EXTRACT_FILE := $(KLAYOUT_SHARE_DIR)/FreePDK45_extract.lvs
export KLAYOUT_EXTRACT_SCRIPT := $(KLAYOUT_BIN_DIR)/extract_FreePDK45
export KLAYOUT_LVS_FILE := $(KLAYOUT_SHARE_DIR)/FreePDK45.lvs
export KLAYOUT_LVS_SCRIPT := $(KLAYOUT_BIN_DIR)/lvs_FreePDK45
KLAYOUT_FILES := \
  $(KLAYOUT_DRC_FILE) $(KLAYOUT_DRC_SCRIPT) \
  $(KLAYOUT_LVS_FILE) $(KLAYOUT_LVS_SCRIPT) \
  $(KLAYOUT_EXTRACT_FILE) $(KLAYOUT_EXTRACT_SCRIPT) \
  $(KLAYOUT_DRC_LYDRC_FILE) \
  $(KLAYOUT_EXTRACT_LYLVS_FILE) \
# KLAYOUT_FILES end
KLAYOUT_EXPORT_SCRIPT := $(SCRIPTS_DIR)/export_klayout.py

.PHONY: klayout
klayout: $(KLAYOUT_FILES)
$(KLAYOUT_FILES): | $(KLAYOUT_DRC_DIR) $(KLAYOUT_LVS_DIR) $(KLAYOUT_SHARE_DIR) $(KLAYOUT_BIN_DIR)
$(KLAYOUT_FILES): | $(KLAYOUT_BIN_DIR)
MKDIRS += $(KLAYOUT_DRC_DIR) $(KLAYOUT_LVS_DIR) $(KLAYOUT_SHARE_DIR) $(KLAYOUT_BIN_DIR)
$(KLAYOUT_FILES): $(PDKMASTER_PATH) $(C4M_INST_DIR)
$(KLAYOUT_FILES): $(KLAYOUT_EXPORT_SCRIPT)
	@echo "Generating klayout files"
	@$(PYTHON_PDKMASTER) $(KLAYOUT_EXPORT_SCRIPT)
	@chmod +x $(KLAYOUT_DRC_SCRIPT) $(KLAYOUT_EXTRACT_SCRIPT) $(KLAYOUT_LVS_SCRIPT)

###

SPICE_EXPORT_SCRIPT := $(SCRIPTS_DIR)/export_spice.py

.PHONY: spice
spice: $(SPICE_FILES)
$(SPICE_FILES): | $(SPICE_DIRS)
$(SPICE_FILES): $(PDKMASTER_PATH) $(C4M_INST_DIR) 
$(SPICE_FILES): $(SPICE_EXPORT_SCRIPT)
	@echo "Generating spice files"
	@$(PYTHON_PDKMASTER) $(SPICE_EXPORT_SCRIPT)

###

GDS_EXPORT_SCRIPT := $(SCRIPTS_DIR)/export_gds.py

.PHONY: gds
gds: $(GDS_FILES)
$(GDS_FILES): | $(GDS_DIRS)
$(GDS_FILES): $(CORIOLIS_GEN_FILES) $(PDKMASTER_PATH) $(C4M_INST_DIR)
$(GDS_FILES): $(GDS_EXPORT_SCRIPT)
	@echo "Generating gds files"
	@$(PYTHON_CORIOLIS) $(GDS_EXPORT_SCRIPT)

###

RTL_EXPORT_SCRIPT := $(SCRIPTS_DIR)/export_rtl.tcl

.PHONY: verilog vhdl
ifeq ($(strip $(AVT_SHELL)),)
verilog:
	@echo "No verilog generation due to lack of avt_shell"
vhdl:
	@echo "No vhdl generation due to lack of avt_shell"
else
verilog: $(VERILOG_FILES)
vhdl: $(VHDL_FILES)
$(VERILOG_FILES) $(VHDL_FILES): | $(TMP_DIR)
$(VERILOG_FILES): RTL_LANG := verilog
$(VHDL_FILES): RTL_LANG := vhdl
$(VERILOG_FILES) $(VHDL_FILES): $(RTL_EXPORT_SCRIPT)
	@echo "Generating $(RTL_LANG) files"
	@cd $(TMP_DIR); env RTL_LANG=$(RTL_LANG) $(AVT_SHELL) $(RTL_EXPORT_SCRIPT)
endif

###

LIBERTY_GEN_SCRIPT := $(SCRIPTS_DIR)/gen_liberty.tcl
LIBERTY_FIX_SCRIPT := $(SCRIPTS_DIR)/fix_lib.py

.PHONY: liberty
ifeq ($(strip $(AVT_SHELL)),)
liberty:
	@echo "No liberty generation due to lack of avt_shell"
else
liberty: $(LIBERTY_FILES)
$(LIBERTY_FILES) : $(VIEWS_DIR)/%.lib : $(LIBERTY_GEN_SCRIPT) $(LIBERTY_FIX_SCRIPT)
	@echo "Generating liberty for library $(LIB)"
	@cd $(TMP_DIR);\
	 env OUT=$(notdir $@) LIB=$(LIB) CORNER=$(CORNER) \
	     $(AVT_SHELL) $(LIBERTY_GEN_SCRIPT); \
	 $(PYTHON_CORIOLIS) $(LIBERTY_FIX_SCRIPT) $(notdir $@) $@
endif

###

.PHONY: design
design: $(C4M_INST_DIR) $(CORIOLIS_FILES) $(LIBERTY_FILES)
	@cd design; make

###

TARBALL_NAME := c4m-pdk-freepdk45_$(shell date +%Y%m%d).tar.xz
TARBALL := $(PWD)/$(TARBALL_NAME)
TARBALL_RELEASE := $(PWD)/releases/$(TARBALL_NAME)

SHORTLOG := $(PWD)/pack/shortlog.txt
RMFILES += $(TARBALL) $(SHORTLOG)

.PHONY: pack release
pack: $(TARBALL)
release: $(TARBALL_RELEASE)

TARBALL_SRCS := \
  $(CORIOLIS_GEN_FILES) \
  $(KLAYOUT_FILES) \
  $(SPICE_FILES) \
  $(GDS_FILES) \
  $(VERILOG_FILES) \
  $(VHDL_FILES) \
  $(LIBERTY_FILES) \
  $(SHORTLOG) \
  design
$(TARBALL): $(TARBALL_SRCS)
	@echo "Packing up"
	@cd pack; tar cJf $@ --dereference \
	     --exclude=.gitignore \
		 --exclude=__pycache__ --exclude='*.pyc' --exclude=.ipynb_checkpoints \
		 --exclude=bsim4v5.out --exclude=synth --exclude=pnr --exclude=log \
		 .

$(SHORTLOG): $(PWD)/.git/index
	@echo "Generating shortlog"
	@git shortlog -e > $@

$(TARBALL_RELEASE): $(TARBALL)
	@echo "Copying release file"
	@cp $< $@

###

DRC_SCRIPT = $(SCRIPTS_DIR)/do_drc.sh
LVS_SCRIPT = $(SCRIPTS_DIR)/do_lvs.sh

drc: $(DRC_FILES)
$(DRC_FILES): $(KLAYOUT_FILES) $(DRC_SCRIPT)
$(DRC_FILES) : $(VERIFICATION_DIR)/%.drc.out :
	@echo "DRC of $(notdir $*)"
	@$(DRC_SCRIPT) $@

lvs: $(LVS_FILES)
$(LVS_FILES): $(KLAYOUT_FILES) $(LVS_SCRIPT)
$(LVS_FILES) : $(VERIFICATION_DIR)/%.lvs.out :
	@echo "LVS of $(notdir $*)"
	@$(LVS_SCRIPT) $@

###

.PHONY: clean
clean:
	@rm -fr $(RMFILES)
	@cd design; make clean
	@echo "Spick&Span"

$(MKDIRS):
	@mkdir -p $@
