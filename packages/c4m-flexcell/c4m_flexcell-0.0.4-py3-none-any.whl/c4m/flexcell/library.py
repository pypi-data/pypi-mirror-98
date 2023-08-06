# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from textwrap import dedent
import os

from pdkmaster.technology import primitive as prm
from pdkmaster.design.library import StdCellLibrary, RoutingGauge

from ._cells import _cells, _oldcells
from .stdcell import _StdCellConverter

__all__ = ["Library"]

class Library:
    def __init__(self, lambda_=0.09):
        self.lambda_ = lambda_
        self.cells = {cell.name: cell for cell in _cells}
        self.oldcells = {cell.name: cell for cell in _oldcells}

    def __getitem__(self, key):
        return self.cells[key]

    @staticmethod
    def write_python(filename=os.path.dirname(__file__)+"/_cells_new.py"):
        with open(filename, "w") as f:
            f.write(dedent("""
                from c4m.flexcell.stdcell import StdCell, Wire, Via, Device

                _cells = [
                """
            ).strip() + "\n")

            for cell in _cells:
                f.write(cell.python_code(level=1))

            f.write("]\n")

    def write_spice(self, dirname=None):
        if dirname is None:
            raise ValueError("Please provide directory to write spice netlists to")

        for cell in _cells:
            with open(dirname + os.sep + cell.name + ".sp", "w") as f:
                f.write("* Spice netlist of {}\n\n".format(cell.name))
                f.write(cell.spice_netlist(lambda_=self.lambda_))

    def convert2pdkmaster(self, name, *,
        tech, cktfab=None, layoutfab=None, nmos, pmos,
        l=None, old=False, nimplant=None, pimplant=None,
    ):
        vias = tuple(tech.primitives.tt_iter_type(prm.Via))
        via1 = vias[1]
        assert (
            (len(via1.bottom) == 1) and (len(via1.top) == 1)
        ), "Unsupported interconnect config"

        firstmetal = via1.top[0]
        topmetal = vias[-1].top[0]

        lib = StdCellLibrary(
            name, tech=tech, cktfab=cktfab, layoutfab=layoutfab,
            global_nets=("vdd", "vss"),
            routinggauge=RoutingGauge(
                tech=tech,
                bottom=firstmetal, bottom_direction="horizontal",
                top=topmetal,
            ),
            pingrid_pitch=20*self.lambda_, row_height=200*self.lambda_,
        )

        converter = _StdCellConverter(
            pdklib=lib, nmos=nmos, pmos=pmos, l=l, lambda_=self.lambda_,
            nimplant=nimplant, pimplant=pimplant,
        )
        for cell in (_oldcells if old else _cells):
            converter(cell)

        return lib