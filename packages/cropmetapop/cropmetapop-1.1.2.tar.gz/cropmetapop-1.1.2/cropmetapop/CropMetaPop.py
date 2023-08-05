#!/usr/bin/env python3

#
# This file is part of CropMetaPop, a sofware of simulation of crop population.
# Please visit www.cropmetapop.org for details.
#
# Copyright (C) 2017 Anne Miramon (anne.miramon@gmail.com)
#
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

""" This file is the main launcher of CropMetaPop"""

#import __future__
#import os
# import sys
import time

from cropmetapop.Reader import Reader
from cropmetapop.Simu import Simu
from cropmetapop.Result import Result
from cropmetapop.Writer import Writer

class CropMetaPop:

    def __init__(self, path):
        self.settingFile = path # sys.argv[1]
        self.mySimu = Simu()
        self.myResult = Result()
        self.myWriter = Writer()
        
        listTime = {'init':time.time(), 'beforeRun':0, 'afterRun':0, 'afterWriteFile':0}

        # Reading of setting of file
        print("\nReading the settings file")
        myReader = Reader(self.settingFile, self.myResult, self.mySimu, self.myWriter)
        self.metaPop = myReader.metaPop

        # Run of simulation
        print("Run of simulation")
        listTime['beforeRun'] = time.time()
        self.mySimu.create_Simulation(self.metaPop, self.myResult)
        listTime['afterRun'] = time.time()
        print("End of the simulation")

        # Create of result files
        print("Writing of results file")
        self.myWriter.createFileResult(self.myResult, self.metaPop, self.mySimu, listTime)


if __name__ == "__main__":
    i = CropMetaPop()
