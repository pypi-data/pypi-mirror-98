#!/usr/bin/env python3

""" This file contains the Result of exchange class attributes and methods"""
#
# ResultExchange.py
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

class ResultExchange:

    """
    It's a object which stores the number of individuals that transfered between two populations at a generation in a replicate.
    """

    def __init__(self, rep, num_popFrom, num_popTo, generation, indExchanged):
        self.replicat = rep
        self.popFrom = num_popFrom
        self.popTo = num_popTo
        self.gen = generation
        self.value = indExchanged

    def getReplicat(self):
        """Gets the number of the replicate"""
        return self.replicat

    def getPopFrom(self):
        """Gets the number of the population of origin"""
        return self.popFrom

    def getPopTo(self):
        """Gets the number of the population of destination"""
        return self.popTo

    def getGeneration(self):
        """Gets the generation of exchange"""
        return self.gen

    def getValue(self):
        """Gets the number of exchanged seeds"""
        return self.value
