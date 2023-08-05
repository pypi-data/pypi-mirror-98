#!/usr/bin/env python3

""" This file contains the Metapopulation attributes and methods"""
#
# MetaPop.py
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

import math

from cropmetapop.Population import Population
from cropmetapop.Locus import Locus


class MetaPop:
    """ This is the class of the Meta Population"""
    def __init__(self):
        self.pops = []
        self.loci = []

        self.byFreq = True
        self.selfing = 0
        self.fecundity = 1

        self.networkColonisation = 0
        self.networkMigration = 0

    def addPop(self, pop):

        """
        Add a population in the metapopulation.
        """

        self.pops.append(pop)

    def addMarker(self, locus):

        """
        Add a marker in the population.

        """

        self.loci.append(locus)

    def lociSelected(self):

        """
        Return the selected markers.
        """

        lociSelect = []
        for num_marker, marker in enumerate(self.loci):
            if marker.getSelected():
                lociSelect.append(num_marker)
        return lociSelect

    def calcRecombinaison(self):

        """
        Calculated the recombinaison rate in function of distance between markers.
        """

        rateRecombinaison = []
        for idxLocus in range(len(self.loci) -1):
            chromLoc = self.loci[idxLocus].getChrom()
            chromNextLoc = self.loci[idxLocus+1].getChrom()
            if chromLoc == chromNextLoc:
                distance = self.loci[idxLocus].getDistance()
                distanceNext = self.loci[idxLocus+1].getDistance()
                if distance is None and distanceNext is None:
                    rateRecombinaison.append(0.5)
                else:
                    distanceBetweenLoci = distanceNext-distance
                    #formule de haldane
                    rate = 0.5*(1-math.exp(-2*distanceBetweenLoci))
                    rateRecombinaison.append(rate)
            else:
                rateRecombinaison.append(0.5)
        return rateRecombinaison

    def getPops(self):
        """Gets the populations of the metapop"""
        return self.pops

    def getMarkers(self):
        """Gets the markers"""
        return self.loci

    def setByFreq(self):
        """Sets the parameter byFreq"""
        self.byFreq = False

    def getByFreq(self):
        """Gets the parameter byFreq"""
        return self.byFreq

    def setSelfing(self, selfing):
        """Set the selfing rate"""
        self.selfing = selfing

    def getSelfing(self):
        """Gets the selfing rate"""
        return self.selfing

    def setFecundity(self, number):
        """Sets the fecundity"""
        self.fecundity = number

    def getFecundity(self):
        """Gets the fecundity"""
        return self.fecundity

    def setNetworkColonisation(self, matrix):
        """Sets the colonization matrix"""
        self.networkColonisation = matrix

    def getNetworkColonisation(self):
        """Gets the colonization matrix"""
        return self.networkColonisation

    def setNetworkMigration(self, matrix):
        """Sets the migration matrix"""
        self.networkMigration = matrix

    def getNetworkMigration(self):
        """Gets the migration matrix"""
        return self.networkMigration
