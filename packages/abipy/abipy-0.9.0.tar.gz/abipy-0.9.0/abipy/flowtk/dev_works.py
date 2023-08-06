# coding: utf-8
"""Work subclasses related to GS calculations."""
#import json

from .works import Work
#from abipy.core.structure import Structure


class CompareGsTasksWork(Work):
    """
    A work made of different GsTasks. Each task perform a GS calculation
    for the same system but different options for the GS solver.
    """

    def on_all_ok(self):
        """
        This method is called when all tasks reach S_OK. It reads the energies
        and the volumes from the GSR file, computes the EOS and produce a
        JSON file `eos_data.json` in outdata.
        """
        self.getnwrite_eosdata()
        return dict(returncode=0, message="EOS computed and file written")
