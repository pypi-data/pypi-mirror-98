# V0.0.1

These are the release notes for the tarball release of the [Chips4Makers PDKMaster FreePDK45](https://gitlab.com/Chips4Makers/c4m-pdk-freepdk45) PDK. This tarball release contains the Python package source of the PDK together with the exported EDA flow support files and examples.

## Contents

* `COPYRIGHT.md`, `shortlog.txt`, `LICENSE.md`, `LICENSES/`: Copyright and license information.
* `c4m`, `setup.py`: The Python package of the PDKMaster PDK. Although adviced to be installed from PyPI it can also be installed with:  
    ```console
    % pip install .
    ```
* `coriolis/`: Coriolis flow support files. See `design/arlet6502` for how it can be used.
* `klayout/`: KLayout support files
  * `share/`: directory with text file DRC and LVS decks
  * `bin/`: script for doing batch mode DRC, extraction and LVS.  
  The scripts will find their decks relative to their installation path, so `share/` and `bin/` need to be be installed in the same directory.
  * `tech/`: DRC and circuit extraction as KLayout technology.  
    It can be installed in the following way:
    ```console
    % cp -r klayout/tech/C4M.FreePDK45 ~/.klayout/tech
    ```
* `views/FreePDK45/FlexLib/`: export views of the FlexLib standard cell for FreePDK45.
  * `gds/`: gds files of the cells
  * `spice/`: spice files of the cells
  * `verilog/`, `vhdl/`: behavioral models in Verilog and VHDL of the cells.
  * `liberty/`: liberty files for the cells
* `design/`: example files using the PDKMaster FreePDK45 library.
  * `arlet6502/`: synthesis and place-and-route on Arlet's 6502 core.  
    It contains makefile and scripts to synthesize and P&R the 6502 core. This can be done if all dependencies are installed or through `make_in_docker.sh` that will use a 2.3GB docker image as preloaded environment.  
    The final output `arlet6502_pnr.gds` has also been included in the tarball.
  * `portfolio.ipynb`, `portfolio.html`: Notebook and resulting HTML version of (currently incomplete) portfolio summary of the PDKMaster FreePDK45 PDK.
  * `inverter.ipynb`, `inverter.html`: Notebook and resulting HTML version of a notebook showing how the PDKMaster FreePDK45 can be used for more analog type circuit development using SPICE simulations etc.  
  More details are inside the notebook.

## Changes

This is first public release so contents of the package is all new.
