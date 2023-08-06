# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
include ../Makefile.conf

OUTPUT := \
  portfolio.html \
  inverter.html \
#END OUTPUTS
SOURCE := \
  portfolio.ipynb \
  inverter.ipynb \
#END SOURCE

all: $(OUTPUT) arlet6502

%.html: %.ipynb
	@echo "Generating $@"
	$(JUPYTER_PDKMASTER) nbconvert --to html --execute $<

.PHONY: arlet6502

arlet6502:
	@cd arlet6502; make

.PHONY: clean
clean:
	@rm -fr $(OUTPUT)
	@cd arlet6502; make clean
	@echo "design Spick&span"
