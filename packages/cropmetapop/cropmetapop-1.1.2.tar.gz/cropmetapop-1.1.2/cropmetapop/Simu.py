#!/usr/bin/env python3

""" This file contains the Simulation class attributes and methods"""
#
# Simu.py
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

import random
import math
import numpy

import simuPOP as simu

from cropmetapop.GenotypeMultiLocus import GenotypeMultiLocus
from cropmetapop.GenotypeLocus import GenotypeLocus
from cropmetapop.ProgressBar import ProgressBar

class Simu:

    """
    This class contains all the attributes and methods of Simu
    """

    def __init__(self):
        # Main settings
        self.metaPop = None
        self.result = None

        self.col_modelExchange = 'excess'
        self.migr_modelExchange = 'excess'

        self.col_FromOne = 0
        self.migr_FromOne = 0
        self.migrOutCarr = 0

        self.generations = 1
        self.replicat = 1
        self.seed = None

        self.finalGeneration = None

    def getGenerations(self):
        """Gets the generation"""
        return self.generations

    def setGenerations(self, gen):
        """Sets the generation"""
        self.generations = gen

    def getSeed(self):
        """Gets the seed of the simulation"""
        return self.seed

    def setSeed(self, seed):
        """Sets the seed of the simulation"""
        self.seed = seed

    def getReplicate(self):
        """Gets the replicate amount"""
        return self.replicat

    def setReplicate(self, replicat):
        """Sets the replicate amount"""
        self.replicat = replicat

    def setColModel(self, model):
        """Sets the colonization model"""
        self.col_modelExchange = model

    def getColModel(self):
        """Gets the colonization model"""
        return  self.col_modelExchange

    def setMigrModel(self, model):
        """Sets the migration model"""
        self.migr_modelExchange = model

    def getMigrModel(self):
        """Gets the migration model"""
        return self.migr_modelExchange

    def setCol_FromOne(self):
        """Sets the col_FromOne attribute to 1"""
        self.col_FromOne = 1

    def setMigr_FromOne(self):
        """Sets the migr_FromOne attribute to 1"""
        self.migr_FromOne = 1

    def setMigrCarrying(self, carrying):
        """Sets the migration maximal amount"""
        self.migrOutCarr = carrying

    def getFinalGeneration(self):
        """Gets the final generation"""
        return self.finalGeneration

    #
    # Simulation
    #

    def create_Simulation(self, metaPop, result):

        """
        This function creates the population of simuPOP and launches the evolution.
        """

        self.metaPop = metaPop
        self.result = result
        self.progress = ProgressBar(self.generations, 60, "Progress")
        simu.setOptions(seed=self.seed)


        self.finalGeneration = [0 for i in range(self.replicat)]

        self.initOps = self.create_InitOps()
        self.preOps = self.create_PreOps()
        self.mating = self.create_Mating()
        self.postOps = self.create_PostOps()
        self.finalOps = self.create_FinaltOps()

        popSize = []
        for pop in self.metaPop.getPops():
            popSize.append(pop.initSize)

        lociChrom = {}
        for marker in self.metaPop.getMarkers():
            if marker.getChrom() in lociChrom:
                lociChrom[marker.getChrom()] += 1
            else:
                lociChrom[marker.getChrom()] = 1
        lociChrom = list(lociChrom.values())


        meta_Population = simu.Population(size=popSize, loci=lociChrom, infoFields=['migrate_to', 'fitness', 'subPop'])
        simulation = simu.Simulator(meta_Population, rep=self.replicat)
        simulation.evolve(initOps=self.initOps, preOps=self.preOps, matingScheme=self.mating, postOps=self.postOps, finalOps=self.finalOps, gen=self.generations)

        return 0

    def create_InitOps(self):

        """
        This function allows to create a list with all operators that initialize the genotype of individuals according to their population
        """

        # Initialization of allele/genotype frequency
        initOps = []
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            if self.metaPop.getByFreq():
                # If the initialization is allele frequency
                for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                    initOps.append(simu.InitGenotype(freq=pop.freqOneMarker(num_marker), loci=num_marker, subPops=num_pop))
            else:
                # If the initialization is genotype frequency.
                genotypes = []
                genotypesList = []
                genotypesFreq = []
                for genotypeMulti in pop.getInitialisation():
                    oneGenotype = []
                    for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                        oneGenotype.append(genotypeMulti.locusGenotype[num_marker].getAll1())
                    for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                        oneGenotype.append(genotypeMulti.locusGenotype[num_marker].getAll2())

                    genotypesList.append(oneGenotype)
                    genotypesFreq.append(genotypeMulti.getFreq())

                # We create the list of the highest frequency genotypes
                genotypesListIndex = range(len(genotypesList))
                if pop.getInitSize() != 0:
                    genotypesIndex = numpy.random.choice(genotypesListIndex, pop.getInitSize(), replace=True, p=genotypesFreq)
                for index in genotypesIndex:
                    if pop.getInitSize() != 0:
                        genotypes.append(genotypesList[index])

                random.shuffle(genotypes)
                geno = []
                for elem in genotypes:
                    for e in elem:
                        geno.append(e)
                if self.metaPop.getPops()[num_pop].getInitSize() > 0:
                    initOps.append(simu.InitGenotype(genotype=geno, subPops=num_pop))

        return initOps

    def create_PreOps(self):

        """
        This function allows to create a list of all operators that are applied on the populations at each generation before the reproduction
        """

        preOps = []
        # Operator that calculate the size of different population
        preOps.append(simu.Stat(popSize=True))
        # Operator that
        preOps.append(simu.PyOperator(func=self.infoSubPop))
        # Calculates the fitness for each individual
        preOps.append(simu.PySelector(func=self.calculFitness, loci=self.metaPop.lociSelected()))
        # Calculates the mean fitness of each population
        preOps.append(simu.Stat(meanOfInfo='fitness', vars=['meanOfInfo_sp']))
        # Extinction test on each population
        preOps.append(simu.PyOperator(func=self.extinctionOrNot))
        # Calculates seed potential created by the population
        preOps.append(simu.PyOperator(func=self.calculPotentialSeed))
        # Calculates the effectives concerned by colonization
        preOps.append(simu.PyOperator(func=self.calculColonisation))
        # Calculates the effectives concerned by migration
        preOps.append(simu.PyOperator(func=self.calculMigration))
        # Result
        preOps.append(simu.Stat(genoFreq=range(len(self.metaPop.getMarkers())), vars=['genoNum_sp']))
        preOps.append(simu.Stat(haploFreq=range(len(self.metaPop.getMarkers())), vars=['haploNum_sp'], step=self.result.getStep()))

        preOps.append(simu.PyOperator(func=self.createResultGenotypeMono, step=self.result.getStep()))
        if self.result.getMulti():
            preOps.append(simu.PyOperator(func=self.createResultGenotypeMulti, step=self.result.getStep()))
        if self.result.getHaplo():
            preOps.append(simu.PyOperator(func=self.createResultHaplotype, step=self.result.getStep()))
        if self.result.getExchange():
            preOps.append(simu.PyOperator(func=self.createResultExchange, step=self.result.getStep()))

        return preOps

    def create_Mating(self):
        """This method is responsible of the mating in the simulation"""

        mating = simu.HeteroMating([
            simu.SelfMating(ops=[simu.Recombinator(rates=self.metaPop.calcRecombinaison(), loci=range(len(self.metaPop.getMarkers())-1))], weight=self.metaPop.getSelfing()),
            simu.HermaphroditicMating(ops=[simu.Recombinator(rates=self.metaPop.calcRecombinaison(), loci=range(len(self.metaPop.getMarkers())-1))], weight=1-self.metaPop.getSelfing())], subPopSize=self.reproduction)

        return mating

    def create_PostOps(self):
        """
        This function allows to create a list of all operators that are applied on the populations at each generation before the reproduction
        """

        postOps = []
        #
        for num_marker, marker in enumerate(self.metaPop.getMarkers()):
            postOps.append(simu.KAlleleMutator(k=marker.getAlleles(), rates=marker.getRateMutation(), loci=num_marker))
        # Store the size of population
        postOps.append(simu.Stat(popSize=True))
        # Stop the simulation if all populations are extinct
        postOps.append(simu.TerminateIf('max(subPopSize) == 0'))
        # Apply the colonisation
        postOps.append(simu.PyOperator(func=self.applyColonisation))
        # Apply the migration
        postOps.append(simu.PyOperator(func=self.applyMigration))

        return postOps


    def create_FinaltOps(self):
        """Create the finalOps attribute"""
        finalOps = []

        return finalOps

    #
    # Function in pre-ops
    #

    def infoSubPop(self, pop):
        """
        Give the number of this subPop each individuals
        """
        self.progress.update(pop.vars()['gen']+1)
        self.finalGeneration[pop.vars()['rep']] = pop.vars()['gen']
        for subPop in range(len(self.metaPop.getPops())):
            for ind in pop.individuals(subPop=subPop):
                ind.setInfo(subPop, 'subPop')
        return True

    def fitnessForLocus(self, num_marker, allele1, allele2, subPop):
        """
        Search the fitness for the genotype of this marker
        """
        subPop = self.metaPop.getPops()[int(subPop)]
        markNb = []
        i = 0
        while i < len(subPop.getValeurSelectives()):
            nbAll = subPop.getValeurSelectives()[i].getMarker().getAlleles()
            nbComb = int(2* nbAll * ((nbAll+1)/2))
            for j in range(0, nbComb):
                markNb.append(i)
            i += 1
        for index, fitness in enumerate(subPop.getValeurSelectives()):
            if markNb[index] == num_marker:
                if fitness.getGenotype().getAll1() == allele1 and fitness.getGenotype().getAll2() == allele2:
                    return fitness.getValue()

        return subPop.getOptimum()

    def calculFitness(self, pop, geno, subPop):
        """
        Calculate the fitness for each individuals
        """
        population = self.metaPop.getPops()[int(subPop)]
        individualFitness = 0
        if len(geno) == 0:
            return 1

        for position, num_marker in enumerate(self.metaPop.lociSelected()):
            individualFitness += self.fitnessForLocus(num_marker, geno[position*2], geno[position*2+1], subPop)
        individualFitness /= len(self.metaPop.lociSelected())

        individualFitnessInPopulation = math.exp(-0.5*pow((individualFitness - population.getOptimum()), 2))

        return individualFitnessInPopulation


    def extinctionOrNot(self, pop):
        """
        Determination of the patch whose population will be extinguished
        """
        dataInSimulation = pop.vars()

        extinction = []
        for num_subPop, subPop in enumerate(self.metaPop.getPops()):
            if  pop.subPopSize(num_subPop) == 0:
                extinction.append(0)
            else:
                ext = random.random()
                if ext < subPop.getRateExtinction():
                    extinction.append(0)
                else:
                    extinction.append(1)

        dataInSimulation['extinction'] = extinction
        return True

    def calculPotentialSeed(self, pop):
        """
        Calculate the number of potential offsprings
        """
        dataInSimulation = pop.vars()
        extinction = dataInSimulation['extinction']
        numberSeed = []
        for num_subPop, subPop in enumerate(self.metaPop.getPops()):
            originalSize = pop.subPopSize(num_subPop)
            if extinction[num_subPop] == 0:
                numberOfSeed = 0
            else:
                meanOfFitness = dataInSimulation['subPop'][num_subPop]["meanOfInfo"]["fitness"]
                numberOfSeed = originalSize * self.metaPop.getFecundity() * meanOfFitness

            numberSeed.append(numberOfSeed)
        dataInSimulation['numberOfSeed'] = numberSeed
        return True

    def calculColonisation(self, pop):
        """
        Calculate the exchanges of seed between populations for the colonisation
        """
        dataInSimulation = pop.vars()
        numberOfSubPop = len(self.metaPop.getPops())

        # If not Colonization
        if self.metaPop.getNetworkColonisation() == 0:
            matrix = []
            for numPopFrom in range(numberOfSubPop):
                line = [0 for i in range(numberOfSubPop)]
                matrix.append(line)
            dataInSimulation['colonisation'] = matrix
            return True

        # If Colonization
        matrix = []
        if self.col_modelExchange == 'excess':
            matrix = self.colonization_with_excess(pop)
        elif self.col_modelExchange == 'friendly':
            matrix = self.colonization_with_friendly(pop)

        dataInSimulation['colonisation'] = matrix
        return True


    def colonization_with_excess(self, pop):
        """
        Calculate the exchanges of seed between populations for the colonisation with the model of exchange *excess*
        """
        dataInSimulation = pop.vars()
        numberOfSeed = dataInSimulation['numberOfSeed']
        extinction = dataInSimulation['extinction']
        numberOfSubPop = len(self.metaPop.getPops())

        matrixOfExchange = []
        for numPopFrom, popFrom in enumerate(self.metaPop.getPops()):
            if numberOfSeed[numPopFrom] < popFrom.getCarryingCapacity() or extinction[numPopFrom] == 0:
                line = [0 for i in range(numberOfSubPop)]

            else:
                line = []
                for numPopTo in range(numberOfSubPop):
                    if extinction[numPopTo] != 0:
                        line.append(0)
                    else:
                        rateCol = self.metaPop.getNetworkColonisation()[numPopFrom][numPopTo]
                        if rateCol > random.random():
                            line.append(1)
                        else:
                            line.append(0)

            matrixOfExchange.append(line)

        if self.col_FromOne:
            for num_PopTo in range(numberOfSubPop):
                listPopFrom = [matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)]
                numberOfExchangeTo = sum(listPopFrom)
                if numberOfExchangeTo > 1:
                    i = random.random()
                    num_PopFrom_Apply = int(i/(1.0/numberOfExchangeTo))
                    num_PopFrom_With1 = 0
                    for num_PopFrom in range(numberOfSubPop):
                        if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                            if num_PopFrom_With1 == num_PopFrom_Apply:
                                pass
                            else:
                                matrixOfExchange[num_PopFrom][num_PopTo] = 0
                            num_PopFrom_With1 += 1

        matrix = []
        for numPopFrom in range(numberOfSubPop):
            line = []
            numberOfExchangeFrom = sum(matrixOfExchange[numPopFrom])
            if numberOfExchangeFrom == 0:
                maxOfExchangeFrom = 0
            else:
                maxOfExchangeFrom = int((numberOfSeed[numPopFrom] - pop.subPopSize(numPopFrom)) / numberOfExchangeFrom)

            for numPopTo in range(numberOfSubPop):
                popTo = self.metaPop.getPops()[numPopTo]
                if matrixOfExchange[numPopFrom][numPopTo] == 1:
                    numberOfExchangeTo = sum([matrixOfExchange[i][numPopTo] for i in range(numberOfSubPop)])
                    maxOfExchangeTo = int(popTo.getCarryingCapacity() / numberOfExchangeTo)
                    line.append(min(maxOfExchangeTo, maxOfExchangeFrom))
                else:
                    line.append(0)

            matrix.append(line)
        return matrix


    def colonization_with_friendly(self, pop):
        """
        Calculate the exchanges of seed between population for the colonisation with the model of exchange *friendly*
        """
        dataInSimulation = pop.vars()
        numberOfSeed = dataInSimulation['numberOfSeed']
        extinction = dataInSimulation['extinction']
        numberOfSubPop = len(self.metaPop.getPops())

        matrixOfExchange = []
        for numPopFrom in range(numberOfSubPop):
            popFrom = self.metaPop.getPops()[numPopFrom]
            if extinction[numPopFrom] == 0:
                line = [0 for i in range(numberOfSubPop)]

            else:
                line = []
                for numPopTo in range(numberOfSubPop):
                    if extinction[numPopTo] != 0:
                        line.append(0)
                    else:
                        rateCol = self.metaPop.getNetworkColonisation()[numPopFrom][numPopTo]
                        if rateCol > random.random():
                            line.append(1)
                        else:
                            line.append(0)

            matrixOfExchange.append(line)

        if self.col_FromOne:
            for num_PopTo in range(numberOfSubPop):
                listPopFrom = [matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)]
                numberOfExchangeTo = sum(listPopFrom)
                if numberOfExchangeTo > 1:
                    i = random.random()
                    num_PopFrom_Apply = int(i/(1.0/numberOfExchangeTo))
                    num_PopFrom_With1 = 0
                    for num_PopFrom in range(numberOfSubPop):
                        if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                            if num_PopFrom_With1 == num_PopFrom_Apply:
                                pass
                            else:
                                matrixOfExchange[num_PopFrom][num_PopTo] = 0
                            num_PopFrom_With1 += 1

        matrix = []
        for numPopFrom in range(numberOfSubPop):
            line = []
            numberOfExchangeFrom = sum(matrixOfExchange[numPopFrom])
            if numberOfExchangeFrom == 0:
                maxOfExchangeFrom = 0
            else:
                maxOfExchangeFrom = int((numberOfSeed[numPopFrom] - popFrom.getColKeepRate()*popFrom.getCarryingCapacity()) / numberOfExchangeFrom)

            for numPopTo in range(numberOfSubPop):
                popTo = self.metaPop.getPops()[numPopTo]
                if matrixOfExchange[numPopFrom][numPopTo] == 1:
                    numberOfExchangeTo = sum([matrixOfExchange[i][numPopTo] for i in range(numberOfSubPop)])
                    maxOfExchangeTo = int(popTo.getCarryingCapacity() / numberOfExchangeTo)
                    line.append(min(maxOfExchangeTo, maxOfExchangeFrom))
                else:
                    line.append(0)

            matrix.append(line)

        return matrix

    def calculMigration(self, pop):
        """
        Calculate the exchanges of seed between populations for the migration
        """

        dataInSimulation = pop.vars()
        numberOfSubPop = len(self.metaPop.getPops())

        # If not Migration
        if self.metaPop.getNetworkMigration() == 0:
            matrix = []
            for popFrom in range(numberOfSubPop):
                line = [0 for i in range(numberOfSubPop)]
                matrix.append(line)

            dataInSimulation['migration'] = matrix
            return True

        # If Migration
        matrix = []
        if self.migr_modelExchange == 'excess':
            matrix = self.migration_with_excess(pop)
        elif self.migr_modelExchange == 'friendly':
            matrix = self.migration_with_friendly(pop)

        dataInSimulation['migration'] = matrix
        return True

    def migration_with_excess(self, pop):
        """This method define the migration with excess"""

        dataInSimulation = pop.vars()
        numberOfSeed = dataInSimulation['numberOfSeed']
        extinction = dataInSimulation['extinction']
        colonisation = dataInSimulation['colonisation']
        numberOfSubPop = len(self.metaPop.getPops())

        # Who
        matrixOfExchange = []
        for num_PopFrom, popFrom in enumerate(self.metaPop.getPops()):
            line = []
            colonisationOrNot = sum(colonisation[num_PopFrom])
            if extinction[num_PopFrom] == 0 or numberOfSeed[num_PopFrom] < popFrom.getCarryingCapacity() or colonisationOrNot != 0:
                line = [0 for i in range(numberOfSubPop)]

            else:
                line = []
                for num_PopTo, popTo in enumerate(self.metaPop.getPops()):
                    #colonisationOrNot = sum(colonisation[num_PopTo])
                    if extinction[num_PopTo] == 0 or colonisationOrNot != 0:
                        line.append(0)
                    elif numberOfSeed[num_PopTo] < popTo.getCarryingCapacity() and self.migrOutCarr == 0:
                        line.append(0)
                    elif numberOfSeed[num_PopTo] < popTo.getCarryingCapacity() and self.migrOutCarr == 1:
                        rate = self.metaPop.getNetworkMigration()[num_PopFrom][num_PopTo]
                        if rate > random.random():
                            line.append(1)
                        else:
                            line.append(0)
                    else:
                        if self.metaPop.getNetworkMigration()[num_PopFrom][num_PopTo] > random.random():
                            line.append(1)
                        else:
                            line.append(0)

            matrixOfExchange.append(line)

        if self.migr_FromOne:
            for num_PopTo in range(numberOfSubPop):
                listPopFrom = [matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)]
                numberOfExchangeTo = sum(listPopFrom)
                if numberOfExchangeTo > 1:
                    i = random.random()
                    num_PopFrom_Apply = int(i/(1.0/numberOfExchangeTo))
                    num_PopFrom_With1 = 0
                    for num_PopFrom, PopFrom in enumerate(matrixOfExchange):
                        if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                            if num_PopFrom_With1 == num_PopFrom_Apply:
                                pass
                            else:
                                matrixOfExchange[num_PopFrom][num_PopTo] = 0
                            num_PopFrom_With1 += 1


        # How much
        matrix = []
        for num_PopFrom, popFrom in enumerate(self.metaPop.getPops()):
            line = []
            numberOfExchangeFrom = sum(matrixOfExchange[num_PopFrom])
            if numberOfExchangeFrom == 0:
                maxOfExchangeFrom = 0
            else:
                maxOfExchangeFrom = int((numberOfSeed[num_PopFrom] - pop.subPopSize(num_PopFrom))/ numberOfExchangeFrom)
            for num_PopTo, popTo in enumerate(self.metaPop.getPops()):
                if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                    # nombre de don recu
                    numberOfExchangeTo = sum([matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)])
                    if numberOfExchangeTo == 0:
                        maxOfExchangeTo = 0
                    else:
                        if numberOfSeed[num_PopTo] < popTo.getCarryingCapacity():
                            maxOfExchangeTo = (popTo.getCarryingCapacity() - numberOfSeed[num_PopTo])/numberOfExchangeTo
                        else:
                            maxOfExchangeTo = int((popTo.getRateReplace() * popTo.getCarryingCapacity()) / numberOfExchangeTo)
                    line.append(min(maxOfExchangeTo, maxOfExchangeFrom))
                else:
                    line.append(0)

            matrix.append(line)

        return matrix

    def migration_with_friendly(self, pop):
        """This method defines the migration when there is no excess of seeds"""

        dataInSimulation = pop.vars()
        numberOfSeed = dataInSimulation['numberOfSeed']
        extinction = dataInSimulation['extinction']
        colonisation = dataInSimulation['colonisation']
        numberOfSubPop = len(self.metaPop.getPops())

        # Who
        matrixOfExchange = []
        for num_PopFrom, popFrom in enumerate(self.metaPop.getPops()):
            line = []
            colonisationOrNot = sum(colonisation[num_PopFrom])
            if extinction[num_PopFrom] == 0 or colonisationOrNot != 0:
                line = [0 for i in range(numberOfSubPop)]

            else:
                line = []
                for num_PopTo, popTo in enumerate(self.metaPop.getPops()):
                    colonisationOrNot = sum(colonisation[num_PopTo])
                    if extinction[num_PopTo] == 0 or colonisationOrNot != 0:
                        line.append(0)
                    elif numberOfSeed[num_PopTo] < popTo.getCarryingCapacity() and self.migrOutCarr == 0:
                        line.append(0)
                    elif numberOfSeed[num_PopTo] < popTo.getCarryingCapacity() and self.migrOutCarr == 1:
                        rate = self.metaPop.getNetworkMigration()[num_PopFrom][num_PopTo]
                        if rate > random.random():
                            line.append(1)
                        else:
                            line.append(0)
                    else:
                        if self.metaPop.getNetworkMigration()[num_PopFrom][num_PopTo] > random.random():
                            line.append(1)
                        else:
                            line.append(0)

            matrixOfExchange.append(line)

        if self.migr_FromOne:
            for num_PopTo in range(numberOfSubPop):
                listPopFrom = [matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)]
                numberOfExchangeTo = sum(listPopFrom)
                if numberOfExchangeTo > 1:
                    i = random.random()
                    num_PopFrom_Apply = int(i/(1.0/numberOfExchangeTo))
                    num_PopFrom_With1 = 0
                    for num_PopFrom, PopFrom in enumerate(matrixOfExchange):
                        if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                            if num_PopFrom_With1 == num_PopFrom_Apply:
                                pass
                            else:
                                matrixOfExchange[num_PopFrom][num_PopTo] = 0
                            num_PopFrom_With1 += 1

        # How much
        matrix = []
        for num_PopFrom, popFrom in enumerate(self.metaPop.getPops()):
            line = []
            numberOfExchangeFrom = sum(matrixOfExchange[num_PopFrom])
            if numberOfExchangeFrom == 0:
                maxOfExchangeFrom = 0
            else:
                maxOfExchangeFrom = int((numberOfSeed[num_PopFrom] - popFrom.getMigrKeepRate()*popFrom.getCarryingCapacity())/ numberOfExchangeFrom)
            for num_PopTo, popTo in enumerate(self.metaPop.getPops()):
                if matrixOfExchange[num_PopFrom][num_PopTo] == 1:
                    # nombre de don recu
                    numberOfExchangeTo = sum([matrixOfExchange[i][num_PopTo] for i in range(numberOfSubPop)])
                    if numberOfExchangeTo == 0:
                        maxOfExchangeTo = 0
                    else:
                        if numberOfSeed[num_PopTo] < popTo.getCarryingCapacity():
                            maxOfExchangeTo = (popTo.getCarryingCapacity() - numberOfSeed[num_PopTo])/numberOfExchangeTo
                        else:
                            maxOfExchangeTo = int((popTo.getRateReplace() * popTo.getCarryingCapacity()) / numberOfExchangeTo)
                    line.append(min(maxOfExchangeTo, maxOfExchangeFrom))
                else:
                    line.append(0)

            matrix.append(line)

        return matrix

    #
    #   Function during the reproduction
    #

    def reproduction(self, pop):
        """This methods creates the new generation"""
        newGeneration = self.calculNewGeneration(pop)
        return newGeneration

    def calculNewGeneration(self, pop):
        """
        Calculate the final number of seeds created in function of number of potential offsprings and exchange between population. This function allows to aggregate the reproduction with the regulation.
        """

        dataInSimulation = pop.vars()
        extinction = dataInSimulation['extinction']
        numberOfSeed = dataInSimulation['numberOfSeed']
        numberOfSubPop = len(self.metaPop.getPops())

        newSize = []
        for num_subPop, subPop in enumerate(self.metaPop.getPops()):
            if extinction[num_subPop] == 0:
                sizeOfPop = 0
            else:
                seedOUT = 0
                for numPopTo in range(numberOfSubPop):
                    seedOUT += dataInSimulation['colonisation'][num_subPop][numPopTo]
                    seedOUT += dataInSimulation['migration'][num_subPop][numPopTo]
                seedIN = 0
                for numPopFrom in range(numberOfSubPop):
                    seedIN += dataInSimulation['migration'][numPopFrom][num_subPop]
                    seedIN += dataInSimulation['colonisation'][numPopFrom][num_subPop]

                poolDeGraine = numberOfSeed[num_subPop]
                if poolDeGraine >= subPop.getCarryingCapacity():
                    poolDeGraine = subPop.getCarryingCapacity()
                    sizeOfPop = poolDeGraine - seedIN + seedOUT
                elif poolDeGraine < subPop.getCarryingCapacity():
                    sizeOfPop = poolDeGraine

            newSize.append(sizeOfPop)

        return newSize

    #
    #   Fonction in post_ops
    #

    def applyColonisation(self, pop):
        """
        Apply the colonisation in the population
        """
        dataInSimulation = pop.vars()
        matrix = dataInSimulation['colonisation']
        simu.migrate(pop, rate=matrix, mode=simu.BY_COUNTS)
        return True


    def applyMigration(self, pop):
        """
        Apply the migration in the population
        """
        dataInSimulation = pop.vars()
        matrix = dataInSimulation['migration']
        simu.migrate(pop, rate=matrix, mode=simu.BY_COUNTS)
        return True

    #
    # Create of results
    #

    def createResultGenotypeMono(self, pop):
        """
        Store the data of genotype mono locus
        """

        dataInSimulation = pop.vars()
        rep = dataInSimulation['rep']
        gen = dataInSimulation['gen']
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                genotypes = list(dataInSimulation['subPop'][num_pop]['genoNum'][num_marker].keys())
                while len(genotypes) != 0:
                    genotype = genotypes[0]
                    newGenotype = GenotypeLocus(min(genotype), max(genotype))
                    numInd = dataInSimulation['subPop'][num_pop]['genoNum'][num_marker][genotype]
                    genotypes.remove(genotype)

                    genotype2 = (genotype[1], genotype[0])
                    if genotype != genotype2:
                        if genotype2 in genotypes:
                            numInd += dataInSimulation['subPop'][num_pop]['genoNum'][num_marker][genotype2]
                            genotypes.remove(genotype2)

                    self.result.addResultGenoMono(rep, num_pop, num_marker, newGenotype, gen, numInd)
        return True

    def createResultHaplotype(self, pop):
        """
        Store the data of haplotype
        """
        dataInSimulation = pop.vars()
        rep = dataInSimulation['rep']
        gen = dataInSimulation['gen']
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            for haplo in dataInSimulation['subPop'][num_pop]['haploNum'][tuple(range(len(self.metaPop.getMarkers())))]:
                numInd = dataInSimulation['subPop'][num_pop]['haploNum'][tuple(range(len(self.metaPop.getMarkers())))][haplo]
                self.result.addResultHaplotype(rep, num_pop, haplo, gen, numInd)
        return True

    def createResultGenotypeMulti(self, pop):
        """
        Store the data of genotype muti-locus
        """
        dataInSimulation = pop.vars()
        # numberOfSubPop = len(self.metaPop.getPops())
        numberofLoci = len(self.metaPop.getMarkers())

        gen = dataInSimulation['gen']
        rep = dataInSimulation['rep']
        for num_subPop, subPop in enumerate(self.metaPop.getPops()):
            listGenoMulti = []
            for ind in pop.individuals(subPop=num_subPop):
                genotype = ind.genotype()
                listGenoMulti.append(tuple(genotype))
            uniqueListGenoMulti = set(listGenoMulti)
            for genoMulti in uniqueListGenoMulti:
                listGenotypeLocus = {}
                numInd = listGenoMulti.count(genoMulti)
                for indexAllele1 in range(len(genoMulti)//2):
                    indexAllele2 = indexAllele1 + numberofLoci
                    # locus = self.metaPop.getMarkers()[indexAllele1]
                    genotypeOneLocus = GenotypeLocus(genoMulti[indexAllele1], genoMulti[indexAllele2])
                    listGenotypeLocus[indexAllele1] = genotypeOneLocus
                genoMultiLocus = GenotypeMultiLocus(listGenotypeLocus)
                self.result.addResultGenoMulti(rep, num_subPop, genoMultiLocus, gen, numInd)

        return True

    def createResultExchange(self, pop):
        """
        Store the data of exchange between populations
        """
        dataInSimulation = pop.vars()
        # numberOfSubPop = len(self.metaPop.getPops())

        gen = dataInSimulation['gen']
        rep = dataInSimulation['rep']
        matrixColonisation = dataInSimulation['colonisation']
        matrixMigration = dataInSimulation['migration']
        # listeExchange = []
        for num_PopFrom, popFrom in enumerate(self.metaPop.getPops()):
            for num_PopTo, popTo in enumerate(self.metaPop.getPops()):
                indExchangeCol = matrixColonisation[num_PopFrom][num_PopTo]
                indExchangeMig = matrixMigration[num_PopFrom][num_PopTo]
                if indExchangeCol != 0:
                    self.result.addResultExchange("Colonization", rep, num_PopFrom, num_PopTo, gen, indExchangeCol)
                if indExchangeMig != 0:
                    self.result.addResultExchange("Migration", rep, num_PopFrom, num_PopTo, gen, indExchangeMig)
        return True
