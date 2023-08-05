#!/usr/bin/env python3

""" This file contains the Fitness attributes and methods"""
#
# Fitness.py $
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


class Fitness:
    """This class contains the attributes and methods for the Fitness"""

    def __init__(self, marker, genotype, value):
        self.marker = marker
        self.genotype = genotype
        self.value = value

    def getMarker(self):
        """Gets the marker"""
        return self.marker

    def getGenotype(self):
        """Gets the genotype"""
        return self.genotype

    def getValue(self):
        """Gets the value of fitness"""
        return self.value
