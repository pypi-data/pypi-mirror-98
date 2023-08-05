#!/usr/bin/env python3

""" This file contains the Locus attributes and methods"""
#
# Locus.py
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

from cropmetapop.GenotypeLocus import GenotypeLocus


class Locus:
    """This class contains the attributes and methods of Locus"""
    def __init__(self):
        self.nb_alleles = 2
        self.genotypesLocus = []

        self.rateMutation = 0
        self.chromosome = ''
        self.distance = None
        self.selected = False

    def setAlleles(self, nb_alleles):
        """Sets the alleles of a locus"""
        self.nb_alleles = nb_alleles
        for allele1 in range(nb_alleles):
            for allele2 in range(nb_alleles):
                genotype = GenotypeLocus(allele1, allele2)
                self.genotypesLocus.append(genotype)

    def getAlleles(self):
        """Gets the alleles of a locus"""
        return self.nb_alleles

    def getGenotypes(self):
        """Gets the genotype of a locus"""
        return self.genotypesLocus

    def setSelected(self):
        """Sets if the locus is selected or not"""
        self.selected = True

    def getSelected(self):
        """Gets if the locus is selected or not"""
        return self.selected

    def setChrom(self, nameChromosome):
        """Sets where the locus is on the chromosome(s)"""
        self.chromosome = nameChromosome

    def getChrom(self):
        """Gets where the locus is on the chromosome(s)"""
        return self.chromosome

    def setDistance(self, distance):
        """Sets the distance of the locus"""
        self.distance = distance

    def getDistance(self):
        """Gets the distance of the locus"""
        return self.distance

    def setRateMutation(self, rate):
        """Sets the rate of mutation of the locus"""
        self.rateMutation = rate

    def getRateMutation(self):
        """Gets the rate of mutation of the locus"""
        return self.rateMutation
