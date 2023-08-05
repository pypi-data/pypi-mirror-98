#!/usr/bin/env python3

""" This file contains the GenotypeMultiLocus attributes and methods"""
#
# GenotypeMultiLocus.py $
#
# This file is part of CropMetaPop, a sofware of simulation of crop population.
# Please visit www.cropmetapop.org for details.
#
# Copyright (C) 2017 Anne Miramon (anne.miramon@gmail.com)
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


class GenotypeMultiLocus:
    """This class contains the GenotypeMultiLocus attributes and methods"""
    def __init__(self, listlocusGenotype, frequence=0):
        self.freq = frequence
        self.locusGenotype = listlocusGenotype

    def __repr__(self):
        return "({},{})".format(self.locusGenotype, self.freq)

    def __eq__(self, other):
        return self.locusGenotype == other.locusGenotype

    def __gt__(self, other):
        for locus in self.locusGenotype:
            if self.locusGenotype[locus] < other.locusGenotype[locus]:
                return False
            elif self.locusGenotype[locus] == other.locusGenotype[locus]:
                continue
            else:
                return True

    def setFreq(self, frequencie):
        """Sets the frequency"""
        self.freq = frequencie

    def getFreq(self):
        """Gets the frequency"""
        return self.freq

    def getLocusGenotype(self):
        """Gets the locus genotype"""
        return self.locusGenotype
