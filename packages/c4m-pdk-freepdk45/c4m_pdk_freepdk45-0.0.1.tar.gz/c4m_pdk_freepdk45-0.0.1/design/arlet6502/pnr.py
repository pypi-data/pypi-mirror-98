import os
import CRL, Hurricane as Hur, Katana, Etesian, Anabatic, Cfg
from helpers import u, l, setNdaTopDir
from helpers.overlay import CfgCache

ndadir = os.environ["NDA_DIR"]
setNdaTopDir(ndadir)

from NDA.node45 import freepdk45_c4m as tech

tech.setup()
tech.FlexLib_setup()

print("Coriolis tech initialized")

from plugins.cts.clocktree import HTree, computeAbutmentBox
from plugins.chip.configuration import ChipConf

af = CRL.AllianceFramework.get()
env = af.getEnvironment()
print(env.getPrint())

with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
    cfg.anabatic.topRoutingLayer = 'metal6'

env.setCLOCK('clk')

# P&R
cell_name = os.environ["CELL"]

# Core block
cell = CRL.Blif.load(cell_name)
cell.setName(cell_name + "_pnr")
af.saveCell(cell, CRL.Catalog.State.Logical)


# # Place-and-route
chipconf = ChipConf( {}, cell, None )

cellGauge = af.getCellGauge()
spaceMargin = Cfg.getParamPercentage('etesian.spaceMargin').asPercentage()/100.0
aspectRatio = Cfg.getParamPercentage('etesian.aspectRatio').asPercentage()/100.0
bb = computeAbutmentBox(cell, spaceMargin, aspectRatio, cellGauge)

et = Etesian.EtesianEngine.create(cell)
ht = HTree.create(chipconf, cell, None, bb)
et.place()
ht.connectLeaf()
ht.route()
et.destroy()

kat = Katana.KatanaEngine.create(cell)
kat.digitalInit()
kat.runGlobalRouter(Katana.Flags.NoFlags)
kat.loadGlobalRouting(Anabatic.EngineLoadGrByNet)
kat.layerAssign(Anabatic.EngineNoNetLayerAssign)
kat.runNegociate(Katana.Flags.NoFlags)
route_success = kat.isDetailedRoutingSuccess()
kat.finalizeLayout()
kat.destroy()

af.saveCell(cell, CRL.Catalog.State.Logical|CRL.Catalog.State.Physical)
CRL.Gds.save(cell)

assert route_success
