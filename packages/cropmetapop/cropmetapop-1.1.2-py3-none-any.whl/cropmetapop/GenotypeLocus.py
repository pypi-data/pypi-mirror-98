#!/usr/bin/env python3

""" This file contains the GenotypeLocus attributes and methods"""
#
# GenotypeLocus.py $
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


class GenotypeLocus:
    """This class contains the attributes and methods of GenotypeLocus"""
    def __init__(self, allele1, allele2):
        self.allele1 = allele1
        self.allele2 = allele2

    def getAll1(self):
        """Gets the first allele"""
        return self.allele1

    def getAll2(self):
        """Gets the second allele"""
        return self.allele2

    def __repr__(self):
        return "({},{})".format(self.allele1, self.allele2)

    def __eq__(self, other):
        if self.allele1 == other.allele1 and self.allele2 == other.allele2:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.allele1 < other.allele1:
            return False
        elif self.allele1 == other.allele1:
            if self.allele2 <= other.allele2:
                return False
            else:
                return True
        else:
            return True
