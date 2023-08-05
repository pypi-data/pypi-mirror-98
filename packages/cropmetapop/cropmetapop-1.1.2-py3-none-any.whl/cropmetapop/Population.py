#!/usr/bin/env python3

""" This file contains the Population attributes and methods"""
#
# Population.py
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


from cropmetapop.GenotypeMultiLocus import GenotypeMultiLocus
from cropmetapop.FreqAll import FreqAll
from cropmetapop.Fitness import Fitness


class Population:

    """
     C'est une population
    """

    def __init__(self):
        self.initSize = 0
        self.carryingCapacity = 0

        self.initialisation = []
        self.valeurSelectives = []

        self.optimum = 1
        self.rateExtinction = 0
        self.rateReplace = 0
        self.col_keepRate = 0.5
        self.migr_keepRate = 0.5


    def addGenotype(self, listGenotypeLocus, frequency):

        """
        Add multi locus genotype frequencies

        :param listGenotypeLocus: list of allele for each marker.
        :type num_marker: list<GenotypeLocus>
        :param frequency: frequency of the multi-locus genotype
        :type frequency: Double
        """

        newGenotype = GenotypeMultiLocus(listGenotypeLocus, frequency)
        self.initialisation.append(newGenotype)

    def addFreqAllele(self, num_marker, frequencies):

        """
        Add allelic frequencies for a marker

        :param num_marker: number of the marker
        :type num_marker: int
        :param frequencies: frequencies of different alleles
        :type genotype: list<Double>
        """

        newFreqAll = FreqAll(num_marker, frequencies)
        self.initialisation.append(newFreqAll)

    def addFitness(self, locus, genotype, value):

        """
        Add a fitness for a genotype for a locus

        :param locus: locus
        :type locus: Locus
        :param genotype: genotype
        :type genotype: genotypeMono
        :param value:
        :type value: Double
        """

        newFitness = Fitness(locus, genotype, value)
        self.valeurSelectives.append(newFitness)

    def freqOneMarker(self, num_marker):
        """Gets the frequency of a marker"""
        for initAllele in self.initialisation:
            if initAllele.getMarker() == num_marker:
                return initAllele.getFrequencies()

    def setInitSize(self, initSize):
        """Sets the initialization size"""
        self.initSize = initSize

    def getInitSize(self):
        """Gets the initialization size"""
        return self.initSize

    def setCarryingCapacity(self, carryingCapacity):
        """Sets the carrying capacity"""
        self.carryingCapacity = carryingCapacity

    def getCarryingCapacity(self):
        """Gets the carrying capacity"""
        return self.carryingCapacity

    def getInitialisation(self):
        """Gets initialization"""
        return self.initialisation

    def getValeurSelectives(self):
        """Gets the selective values"""
        return self.valeurSelectives

    def setOptimum(self, optimum):
        """Sets the optimum of the population"""
        self.optimum = optimum

    def getOptimum(self):
        """Gets the optimum of the population"""
        return self.optimum

    def setRateExtinction(self, rateExtinction):
        """Sets the extinction rate"""
        self.rateExtinction = rateExtinction

    def getRateExtinction(self):
        """Gets the extinction rate"""
        return self.rateExtinction

    def setRateReplace(self, rateReplace):
        """Sets the replacement rate"""
        self.rateReplace = rateReplace

    def getRateReplace(self):
        """Gets the replacement rate"""
        return self.rateReplace

    def setColKeepRate(self, keepRate):
        """Sets the colonization rate"""
        self.col_keepRate = keepRate

    def getColKeepRate(self):
        """Gets the colonization rate"""
        return self.col_keepRate

    def setMigrKeepRate(self, keepRate):
        """Sets the migration rate"""
        self.migr_keepRate = keepRate

    def getMigrKeepRate(self):
        """Gets the migration rate"""
        return self.migr_keepRate
