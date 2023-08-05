#!/usr/bin/env python3

""" This file contains the Result of Genotype MultiLocus class attributes and methods"""
#
# ResultGenoMulti.py
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

class ResultGenoMulti:

    """
    It's a object which stores the number of individuals with a specific genotype in a replicate, in a population at a generation.
    """

    def __init__(self, rep, num_subPop, genoMulti, generation, value):
        self.replicat = rep
        self.subPop = num_subPop
        self.genotypeMulti = genoMulti
        self.gen = generation
        self.value = value

    def __repr__(self):
        return "<GenotypeMulti(rep={}, subPop={}, genotypeMulti={}, gen={})>".format(self.replicat, self.subPop, self.genotypeMulti.getLocusGenotype(), self.gen)

    def getReplicat(self):
        """Gets the number of the replicate"""
        return self.replicat

    def getSubPop(self):
        """Gets the number of the population"""
        return self.subPop

    def getGenoMulti(self):
        """Gets the Genotype MultiLocus"""
        return self.genotypeMulti

    def getGeneration(self):
        """Gets the generation"""
        return self.gen

    def getValue(self):
        """Gets the number of individuals with this genotype"""
        return self.value
