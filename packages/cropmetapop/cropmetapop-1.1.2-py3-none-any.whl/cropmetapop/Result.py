#!/usr/bin/env python3

""" This file contains the Result class attributes and methods"""
#
# Result.py
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

from cropmetapop.ResultGenoMono import ResultGenoMono
from cropmetapop.ResultGenoMulti import ResultGenoMulti
from cropmetapop.ResultHaplotype import ResultHaplotype
from cropmetapop.ResultExchange import ResultExchange


class Result:

    """
    It's an object which stores all results.
    """

    def __init__(self):
        self.step = 1
        self.folder = None
        self.folderTime = 1
        self.listResultGenoMono = []
        self.multi = False
        self.listResultGenoMulti = []
        self.haplo = False
        self.listResultHaplotype = []
        self.exchange = False
        self.listResultExchangeColonisation = []
        self.listResultExchangeMigration = []

    def getStep(self):
        """Gets every how much steps we should record"""
        return self.step

    def setStep(self, step):
        """Sets avery how much steps we should record"""
        self.step = step

    def getFolder(self):
        """Gets the name of the folder to record to"""
        return self.folder

    def setFolder(self, nameFolder):
        """Sets the name of the folder to record to"""
        self.folder = nameFolder

    def getFolderTime(self):
        """Gets if we should record with time in folder name"""
        return self.folderTime

    def setFolderTime(self, time):
        """Sets if we should record with time in folder name"""
        self.folderTime = time

    def addResultGenoMono(self, rep, nameSubPop, nameLocus, genotype, generation, value):
        """
        Create a instance of ResultGenoMono and adds it at the list listResultGenoMono
        """
        result = ResultGenoMono(rep, nameSubPop, nameLocus, genotype, generation, value)
        self.listResultGenoMono.append(result)

    def getResultGenoMono(self):
        """Gets the result for GenotypeMonoLocus"""
        return self.listResultGenoMono

    def getMulti(self):
        """Gets multi attribute"""
        return self.multi

    def setMulti(self):
        """Sets Multi attribute"""
        self.multi = True

    def addResultGenoMulti(self, rep, nameSubPop, genoMulti, generation, value):
        """
        Create a instance of ResultGenoMulti and adds it at the list listResultGenoMulti
        """
        result = ResultGenoMulti(rep, nameSubPop, genoMulti, generation, value)
        self.listResultGenoMulti.append(result)

    def getResultGenoMulti(self):
        """Gets the result for GenotypeMultiLocus"""
        return  self.listResultGenoMulti

    def getHaplo(self):
        """Gets haplo attribute"""
        return self.haplo

    def setHaplo(self):
        """Sets haplo attribute"""
        self.haplo = True

    def addResultHaplotype(self, rep, nameSubPop, haplo, generation, value):
        """
        Create a instance of ResultHaplotype and adds it at the list list listResultHaplotype
        """
        result = ResultHaplotype(rep, nameSubPop, haplo, generation, value)
        self.listResultHaplotype.append(result)

    def getResultHaplotype(self):
        """Gets the result for Haplotypes"""
        return self.listResultHaplotype

    def getExchange(self):
        """Gets exchange attribute"""
        return self.exchange

    def setExchange(self):
        """Sets exchange attribute"""
        self.exchange = True

    def addResultExchange(self, typeExhange, rep, namePopFrom, namePopTo, generation, indExchanged):
        """
        Create a instance of ResultExchange and adds it at the list corresponding to the type of exchange.
        """
        result = ResultExchange(rep, namePopFrom, namePopTo, generation, indExchanged)
        if typeExhange == "Colonization":
            self.listResultExchangeColonisation.append(result)
        else:
            self.listResultExchangeMigration.append(result)

    def getResultExchangeMigration(self):
        """Gets results for migration"""
        return self.listResultExchangeMigration

    def getResultExchangeColonisation(self):
        """Gets results for colonization"""
        return self.listResultExchangeColonisation
