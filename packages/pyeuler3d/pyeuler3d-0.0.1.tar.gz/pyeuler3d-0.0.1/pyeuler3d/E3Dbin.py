from pathlib import Path
from pye3d import optPath
from pye3d.config import config
import subprocess

"""
Contain Paths to E3D executables and methods to call them. Will consider that the binaries
are on your path by default.
"""


class E3Dbin:
    def __init__(
        self,
        prePath: optPath = None,
        solverPath: optPath = None,
        postPath: optPath = None,
    ) -> None:

        if prePath:
            self.prePath = Path(prePath)
        else:
            self.prePath = Path("E3D_PRE")

        if solverPath:
            self.solverPath = Path(solverPath)
        else:
            self.solverPath = Path("E3D_Solver")

        if postPath:
            self.postPath = Path(postPath)
        else:
            self.postPath = Path("E3D_POST")

    def callPRE(self, config: config, logPath: optPath = None):
        if logPath:
            logPath = Path(logPath)

        subprocess.run([str(self.prePath)])