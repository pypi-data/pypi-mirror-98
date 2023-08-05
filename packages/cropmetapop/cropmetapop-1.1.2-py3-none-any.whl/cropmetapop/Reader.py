#!/usr/bin/env python3

"""This is the file in charge of reading the settings file of
CropMetaPop to integrate the settings in the simulation"""

#
# Reader.py
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

import os
import random
import sys
import math
# import shutil

from cropmetapop.MetaPop import MetaPop
from cropmetapop.Population import Population
from cropmetapop.Locus import Locus
from cropmetapop.GenotypeLocus import GenotypeLocus

# Color codes for the terminal output
FAIL = '\033[91m'
WARNING = '\033[93m'
ENDL = '\033[0m'

class Reader:
    """This class is what will parse the settings file to retrieve the parameters"""

    def __init__(self, nameSettingFile, result, simulation, writer):
        self.nameSettingFile = nameSettingFile

        self.directory = os.path.dirname(nameSettingFile)+'/'
        if self.directory == '/':
            self.directory = './'

        self.metaPop = MetaPop()
        self.simulation = simulation
        self.result = result
        self.writer = writer

        self.data = {}
        self.default = {}
        self.settingsFile = None

        self.readFile()

    def readFile(self):
        """
        Read the settings file
        """

        # Parameters by default
        self.default = {
            "generations": 1,
            "replicates": 1,
            "folder": "simulation",
            "folder_time": 1,

            "nb_pop": 1,
            "nb_marker": 1,
            "nb_allele": [2],

            "fecundity": 1,
            "optimum": [1],
            "percentSelf": 0,
            "mut_rate": [0],

            "ext_rate": [0],

            "col_network": 0,
            "col_directed": 0,
            "col_nb_edge": 0,
            "col_nb_cluster": 1,
            "col_prob_inter": 1,
            "col_prob_intra": 1,
            "col_power": 1,
            "col_rate": 0,
            "col_from_one": 0,
            "col_transfer_model": 'excess',
            "col_keepRate": [0.5],

            "migr_network": 0,
            "migr_directed": 0,
            "migr_nb_edge": 0,
            "migr_nb_cluster": 1,
            "migr_prob_inter": 1,
            "migr_prob_intra": 1,
            "migr_power": 1,
            "migr_replace": [0],
            "migr_rate": 0,
            "migr_from_one": 0,
            "migr_carrying": 0,
            "migr_transfer_model": 'excess',
            "migr_keepRate": [0.5],

            "step": 1,
            "separate_replicate": 0
        }

        with open(self.nameSettingFile) as data_file:
            text = data_file.read()
            self.writer.setSettingsFile(text)
            lines = text.split('\n')
            for num_line, line in enumerate(lines):
                if line == '' or '#' in line:
                    continue
                elif ':' in line:
                    key = line.split(':')[0]
                    key = key.replace(' ', '')
                    value = line.split(':')[1]
                    value = value.replace(' ', '')
                    self.data[key] = value
                else:
                    self.printLineError(self.nameSettingFile, num_line)
                    sys.exit(FAIL+"Error : A line must be empty, a comment (#) or a parameter with this value (key:value)"+ENDL)

        self.verification()
        self.transform_in_type(self.data)

        # Simulation
        self.info_simulation()
        # Meta Population
        self.create_MetaPop()
        # Marker
        self.create_Marker()
        # Breeding
        self.create_Breeding()
        # Extinction
        self.create_Extinction()
        # Colonization
        self.create_colonisation()
        # Migration
        self.create_migration()
        # Initialisation
        self.initalisation()
        # Output
        self.outputs()

    def info_simulation(self):
        """
        Recovers simulation information
        """

        # nomber of generation
        nb_generation = self.data_vs_default('generations')
        self.simulation.setGenerations(nb_generation)

        # number of replicate
        nb_replicate = self.data_vs_default('replicates')
        self.simulation.setReplicate(nb_replicate)

        # name of result folder
        nameFolderResult = self.data_vs_default('folder')
        timeFolderResult = self.data_vs_default('folder_time')

        if timeFolderResult == 0 and os.path.isdir(nameFolderResult):
            sys.exit(FAIL+"Error: This folder "+nameFolderResult+" already exists"+ENDL)

        self.result.setFolder(nameFolderResult)
        self.result.setFolderTime(timeFolderResult)

        # seed
        seed = self.data_vs_default('seed')
        self.simulation.setSeed(seed)
        if seed is None:
            seed = random.randint(0, 4294967295)
            random.seed(seed)
        else:
            random.seed(seed)
            if seed > 4294967295:
                sys.exit(FAIL+"Error: This seed is above the maximal value accepted by simuPOP. Please set a seed lower than 4294967295."+ENDL)
        self.simulation.setSeed(seed)

    def create_MetaPop(self):
        """
        Creation of the metapopulation

        """
        nb_pop = self.data_vs_default('nb_pop')
        try:
            carrying = self.data['carr_capacity']
            carrying = self.accomodat_list('carr_capacity', 'population', nb_pop, carrying)
        except Exception:
            sys.exit(FAIL+"Error : The parameter carr_capacity must be given"+ENDL)

        try:
            initSize = self.data['init_size']
            initSize = self.accomodat_list('init_size', 'population', nb_pop, initSize)
        except Exception:
            initSize = carrying

        for num_pop in range(nb_pop):
            pop = Population()
            pop.setInitSize(initSize[num_pop])
            pop.setCarryingCapacity(carrying[num_pop])
            self.metaPop.addPop(pop)

    def create_Marker(self):
        """
        Creation of the  markers

        """
        nb_marker = self.data_vs_default('nb_marker')
        nb_allele = self.data_vs_default('nb_allele')
        nb_allele = self.accomodat_list('nb_allele', 'marker', nb_marker, nb_allele)

        mut_rate = self.data_vs_default('mut_rate')
        mut_rate = self.accomodat_list('mut_rate', 'marker', nb_marker, mut_rate)

        for num_marker in range(nb_marker):
            marker = Locus()
            marker.setAlleles(nb_allele[num_marker])
            if nb_allele[num_marker] == 1:
                if mut_rate[num_marker] != 0:
                    sys.exit(FAIL+'The mutation rate of the marker '+str(num_marker)+' must be 0 because its number of alleles is 1'+ENDL)
            else:
                marker.setRateMutation(mut_rate[num_marker])
            self.metaPop.addMarker(marker)

        fileGenetic = self.data_vs_default('geneticMap')
        if fileGenetic is None:
            pass
        else:
            self.read_geneticMap(fileGenetic)

    def create_Breeding(self):
        """This function is responsible of retrieving the breeding parameters"""
        fecundity = self.data_vs_default('fecundity')
        if fecundity < 1:
            sys.exit(FAIL+"The fecundity must be superior to 1"+ENDL)
        self.metaPop.setFecundity(fecundity)


        percentSelf = self.data_vs_default('percentSelf')
        self.metaPop.setSelfing(percentSelf)

        optimum = self.data_vs_default('optimum')
        optimum = self.accomodat_list('optimum', 'population', self.data_vs_default('nb_pop'), optimum)
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            pop.setOptimum(optimum[num_pop])


        namefilefitness = self.data_vs_default('fitness')
        namefilefitness_equal = self.data_vs_default('fitness_equal')
        if namefilefitness is None and namefilefitness_equal is None:
            return
        elif namefilefitness is None:
            self.read_fitness_equal(namefilefitness_equal)
        elif namefilefitness_equal is None:
            self.read_fitness(namefilefitness)

    def create_Extinction(self):
        """ This function is responsible of retrieving the extinction rate in the file"""
        extRate = self.data_vs_default('ext_rate')
        extRate = self.accomodat_list('ext_rate', 'population', self.data_vs_default('nb_pop'), extRate)
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            pop.setRateExtinction(extRate[num_pop])

    def create_colonisation(self):
        """ Create the network of Colonization"""
        nb_pop = self.data_vs_default('nb_pop')

        col_exchange_model = self.data_vs_default('col_transfer_model')
        self.simulation.setColModel(col_exchange_model)

        col_keepRate = self.data_vs_default('col_keepRate')
        col_keepRate = self.accomodat_list('col_keepRate', 'population', nb_pop, col_keepRate)

        fecundity = self.data_vs_default('fecundity')

        for num_pop, pop in enumerate(self.metaPop.getPops()):
            pop.setColKeepRate(col_keepRate[num_pop])

        col_network = self.data_vs_default('col_network')
        col_rate = self.data_vs_default('col_rate')
        if self.data_vs_default('col_directed'):
            col_directed = True
        else:
            col_directed = False

        if self.data_vs_default('col_from_one'):
            self.simulation.setCol_FromOne()


        if nb_pop == 1:
            print(WARNING+"Warning : the number of population is set to 1, there will be no colonization events"+ENDL)
            self.writer.addWarning("Warning : the number of population is set to 1, there will be no colonization events")

        if fecundity == 1:
            print(WARNING+"Warning : the fecundity is set to 1, there will be no colonization"+ENDL)
            self.writer.addWarning("Warning : the fecundity is set to 1, there will be no colonization")


        if type(col_network) == str:
            #nameFile = col_network[1:len(col_network)]
            network = self.read_network(col_network, 'colonization')
            if col_rate is None:
                pass
            else:
                for num_line in range(nb_pop):
                    for num_col in range(nb_pop):
                        if network[num_line][num_col] == 1:
                            network[num_line][num_col] = col_rate
        else:
            import igraph
            G = igraph.Graph()
            if col_network == 0:
                # No colonisation
                return

            elif col_network == 1:
                # Stepping stone 1D model
                G = G.Lattice([1, nb_pop], 1, circular=False)

            elif col_network == 2:
                # Stepping stone 2D model
                largeur = int(math.sqrt(nb_pop))
                if largeur*largeur != nb_pop:
                    sys.exit(FAIL+"Error : In the colonisation, the number of population is not correct to create a network Lattice 2D"+ENDL)
                G = G.Lattice([largeur, largeur], 1, circular=False)

            elif col_network == 3:
                # Island
                G = G.Full(nb_pop, directed=col_directed)

            elif col_network == 4:
                # Erdos-Renyi model
                nbedge = self.data_vs_default('col_nb_edge')
                if col_directed:
                    nb_edge_max = (nb_pop*(nb_pop-1))
                else:
                    nb_edge_max = (nb_pop*(nb_pop-1))/2
                if nbedge == 0:
                    G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=col_directed, loops=False)
                elif nbedge < nb_pop-1:
                    sys.exit(FAIL+"Error : In the colonisation, the number of edge must be greater than the number of population"+ENDL)
                elif nbedge > nb_edge_max:
                    sys.exit(FAIL+"Error: In the colonisation, the number of edge maximum for a network with "+str(nb_pop)+" node is "+str(nb_edge_max)+ENDL)

                G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=col_directed, loops=False)
                test_network = 0
                while G.clusters(mode="weak").__len__() != 1 and test_network < 1000:
                    G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=col_directed, loops=False)
                    test_network += 1
                if G.clusters(mode="weak").__len__() != 1:
                    sys.exit(FAIL+'Error: In the colonisation, the number of edges is too small to create a connected graph'+ENDL)

            elif col_network == 5:
                # Community model
                nb_cluster = self.data_vs_default('col_nb_cluster')
                prob_inter = self.data_vs_default('col_prob_inter')
                prob_intra = self.data_vs_default('col_prob_intra')

                listVert = []
                for i in range(nb_cluster):
                    listVert.append(1.0/nb_cluster)
                pref = []
                for i in range(nb_cluster):
                    line = []
                    for j in range(nb_cluster):
                        if i == j:
                            line.append(prob_intra)
                        else:
                            line.append(prob_inter)
                    pref.append(line)

                G = G.Preference(n=nb_pop, type_dist=listVert, pref_matrix=pref, attribute=None, directed=col_directed, loops=False)
                test_network = 0
                while G.clusters(mode="weak").__len__() != 1 and test_network < 1000:
                    G = G.Preference(n=nb_pop, type_dist=listVert, pref_matrix=pref, attribute=None, directed=col_directed, loops=False)
                    test_network += 1
                if G.clusters(mode="weak").__len__() != 1:
                    sys.exit(FAIL+'Error: In the colonisation, the probabilities of connection are too small to create a connected graph'+ENDL)

            elif col_network == 6:
                # Barabasi-Albert model
                col_power = self.data_vs_default('col_power')
                G = G.Barabasi(n=nb_pop, outpref=False, directed=col_directed, power=col_power, zero_appeal=1, implementation="psumtree_multiple", start_from=None)

            network = []
            adjacency = G.get_adjacency()
            for num_line in range(nb_pop):
                line = []
                for num_col in range(nb_pop):
                    if adjacency[num_line][num_col] == 1:
                        line.append(col_rate)
                    else:
                        line.append(0)
                network.append(line)

        self.metaPop.setNetworkColonisation(network)

    def create_migration(self):
        """
        Create the network of Migration
        """
        nb_pop = self.data_vs_default('nb_pop')

        migr_exchange_model = self.data_vs_default('migr_transfer_model')
        self.simulation.setMigrModel(migr_exchange_model)

        migr_carrying = self.data_vs_default('migr_carrying')
        self.simulation.setMigrCarrying(migr_carrying)

        migr_replace = self.data_vs_default('migr_replace')
        migr_replace = self.accomodat_list('migr_replace', 'population', nb_pop, migr_replace)
        migr_keepRate = self.data_vs_default('migr_keepRate')
        migr_keepRate = self.accomodat_list('migr_keepRate', 'population', nb_pop, migr_keepRate)

        fecundity = self.data_vs_default('fecundity')

        if self.data_vs_default('migr_from_one'):
            self.simulation.setMigr_FromOne()

        for num_pop, pop in enumerate(self.metaPop.getPops()):
            pop.setRateReplace(migr_replace[num_pop])
            pop.setMigrKeepRate(migr_keepRate[num_pop])

        if nb_pop == 1:
            print(WARNING+"Warning : the number of population is set to 1, there will be no migration events"+ENDL)
            self.writer.addWarning("Warning : the number of population is set to 1, there will be no migration events")

        if fecundity == 1:
            print(WARNING+"Warning : the fecundity is set to 1, there will be no migration"+ENDL)
            self.writer.addWarning("Warning : the fecundity is set to 1, there will be no migration")


        migr_network = self.data_vs_default('migr_network')
        migr_rate = self.data_vs_default('migr_rate')
        if self.data_vs_default('migr_directed'):
            migr_directed = True
        else:
            migr_directed = False


        if type(migr_network) == str:
            #nameFile = migr_network[1:len(migr_network)]
            network = self.read_network(migr_network, 'migration')
            if migr_rate is None:
                pass
            else:
                for num_line in range(nb_pop):
                    for num_col in range(nb_pop):
                        if network[num_line][num_col] == 1:
                            network[num_line][num_col] = migr_rate
        else:
            import igraph
            G = igraph.Graph()
            if migr_network == 0:
                # No migration
                return

            elif migr_network == 1:
                # Stepping stone 1D model
                G = G.Lattice([1, nb_pop], 1, circular=False)

            elif migr_network == 2:
                # Stepping stone 2D model
                largeur = int(math.sqrt(nb_pop))
                if largeur*largeur != nb_pop:
                    sys.exit(FAIL+"Error : In the migration, the number of population is not correct to create a network Lattice 2D"+ENDL)
                G = G.Lattice([largeur, largeur], 1, circular=False)

            elif migr_network == 3:
                # Island
                G = G.Full(nb_pop)

            elif migr_network == 4:
                # Erdos-Renyi model
                nbedge = self.data_vs_default('migr_nb_edge')
                if migr_directed:
                    nb_edge_max = (nb_pop)*(nb_pop -1)
                else:
                    nb_edge_max = (nb_pop*(nb_pop - 1))/2

                if nbedge == 0:
                    G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=migr_directed, loops=False)
                elif nbedge < nb_pop-1:
                    sys.exit(FAIL+"Error : In the migration, the number of edge must be greater than the number of population"+ENDL)
                elif nbedge > nb_edge_max:
                    sys.exit(FAIL+"Error: In the migration, the number of edge maximum for a network with "+str(nb_pop)+" node is "+str(nb_edge_max)+ENDL)

                G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=migr_directed, loops=False)
                test_network = 0
                while G.clusters(mode="weak").__len__() != 1 and test_network < 1000:
                    G = G.Erdos_Renyi(n=nb_pop, m=nbedge, directed=migr_directed, loops=False)
                    test_network += 1
                if G.clusters(mode="weak").__len__() != 1:
                    sys.exit(FAIL+'Error: In the migration, the number of edges is smaller to create a connected graph'+ENDL)

            elif migr_network == 5:
                # Community model
                nb_cluster = self.data_vs_default('migr_nb_cluster')
                prob_inter = self.data_vs_default('migr_prob_inter')
                prob_intra = self.data_vs_default('migr_prob_intra')

                listVert = []
                for i in range(nb_cluster):
                    listVert.append(1.0/nb_cluster)
                pref = []
                for i in range(nb_cluster):
                    line = []
                    for j in range(nb_cluster):
                        if i == j:
                            line.append(prob_intra)
                        else:
                            line.append(prob_inter)
                    pref.append(line)

                G = G.Preference(n=nb_pop, type_dist=listVert, pref_matrix=pref, attribute=None, directed=migr_directed, loops=False)
                test_network = 0
                while G.clusters(mode="weak").__len__() != 1 and test_network < 1000:
                    G = G.Preference(n=nb_pop, type_dist=listVert, pref_matrix=pref, attribute=None, directed=migr_directed, loops=False)
                    test_network += 1
                if G.clusters(mode="weak").__len__() != 1:
                    sys.exit(FAIL+'Error: In the migration, the probabilities of connection are smaller to create a connected graph'+ENDL)

            elif migr_network == 6:
                # Barabasi-Albert model
                migr_power = self.data_vs_default('migr_power')
                G = G.Barabasi(n=nb_pop, outpref=False, directed=migr_directed, power=migr_power, zero_appeal=1, implementation="psumtree_multiple", start_from=None)

            network = []
            adjacency = G.get_adjacency()
            for num_line in range(nb_pop):
                line = []
                for num_col in range(nb_pop):
                    if adjacency[num_line][num_col] == 1:
                        line.append(migr_rate)
                    else:
                        line.append(0)
                network.append(line)

        self.metaPop.setNetworkMigration(network)


    def initalisation(self):
        """
        Initialisation of genotype of individuals
        """

        init_alleleFrequency = self.data_vs_default('init_AlleleFrequency')
        if init_alleleFrequency is None:
            init_alleleFrequency_equal = self.data_vs_default('init_AlleleFrequency_equal')
            if init_alleleFrequency_equal is None:
                init_GenotypeFrequency = self.data_vs_default('init_GenotypeFrequency')
                if init_GenotypeFrequency is None:
                    init_GenotypeFrequency_equal = self.data_vs_default('init_GenotypeFrequency_equal')
                    if init_GenotypeFrequency_equal is None:
                        # initalisation identique pour tous les marqueurs
                        for pop in self.metaPop.getPops():
                            for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                                nb_allele = marker.getAlleles()
                                value = []
                                for allele in range(nb_allele):
                                    value.append(1.0/nb_allele)
                                pop.addFreqAllele(num_marker, value)
                    else:
                        # genotype frequency equal
                        self.metaPop.setByFreq()
                        self.read_genotype_equal(init_GenotypeFrequency_equal)
                else:
                    # Frequence genotipique differentielle
                    self.metaPop.setByFreq()
                    self.read_genotype(init_GenotypeFrequency)
            else:
                # Frequence allelique identique
                self.read_allele_equal(init_alleleFrequency_equal)
        else:
            # Frequence allelique differentielle
            self.read_allele(init_alleleFrequency)

    def outputs(self):
        """This function is reponsible to retrieve the output parameters in
the settings file"""
        step = self.data_vs_default('step')
        self.result.setStep(step)

        folder = self.data_vs_default('folder')
        self.result.setFolder(folder)

        outputs = self.data_vs_default('outputs')
        if outputs is None:
            return
        else:
            if 'genotype' in outputs:
                self.result.setMulti()
            if 'haplotype' in outputs:
                self.result.setHaplo()
            if 'seed_transfert' in outputs:
                self.result.setExchange()

        sep_rep = self.data_vs_default('separate_replicate')
        self.writer.setSeparateReplicate(sep_rep)


    def read_geneticMap(self, nameFile):
        """
        Reading of file in the parameter geneticMap
        """

        nb_marker = self.data_vs_default('nb_marker')
        with open(nameFile) as file_genetic:
            text = file_genetic.read()
            self.writer.addExternalFile("geneticMap", text)
            lines = text.split('\n')

            num_line_effective = 0
            listChromosome = []
            chromosomePrec = ''
            distancePrec = 0
            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue
                if len(line) != 3:
                    sys.exit(FAIL+"Error: The file "+nameFile+" is not correct. Each line must have only 3 elements."+ENDL)

                try:
                    num_marker = int(line[0])
                    if num_marker < 0 or num_marker >= nb_marker:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of markers is "+str(nb_marker)+". The marker"+str(num_marker)+"doesn't exist"+ENDL)
                    if num_line_effective != int(line[0]):
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The markers must be given in order of number and distance"+ENDL)
                    marker = self.metaPop.getMarkers()[num_line_effective]
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The first element of a line must be an integer which corresponds to the number of the marker"+ENDL)

                chromosome = line[1]
                try:
                    distance = float(line[2])
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The data for the distance must be a double"+ENDL)

                if chromosome == chromosomePrec:
                    if distance < distancePrec:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The markers must be in order of number and distance. The distance cannot be lower to the previous distance."+ENDL)
                else:
                    if chromosome in listChromosome:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The markers must be in order."+ENDL)

                marker.setChrom(chromosome)
                marker.setDistance(distance)

                num_line_effective += 1
                chromosomePrec = chromosome
                distancePrec = distance

        for marker in self.metaPop.getMarkers():
            if marker.getDistance() is None or marker.getChrom() == '':
                sys.exit(FAIL+"Error: The chromosomes and the distances of all markers must be given."+ENDL)


    def read_fitness(self, nameFile):
        """
        Reading of file in the parameter fitness
        """
        nb_marker = self.data_vs_default('nb_marker')
        nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_fitness:
            text = file_fitness.read()
            self.writer.addExternalFile("fitness", text)
            lines = text.split('\n')

        for num_line, line in enumerate(lines):
            line = line.replace(' ', '')
            line = line.split(',')
            if line == ['']:
                continue
            if len(line) != 4:
                sys.exit(FAIL+"Error: The file "+nameFile+" is not correct. Each line must have only 4 elements."+ENDL)

            # Test on the population number
            try:
                num_pop = int(line[0])
                if num_pop < 0 or num_pop >= nb_pop:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The number of populations is "+str(nb_pop)+". The population"+str(num_pop)+"doesn't exist"+ENDL)
                pop = self.metaPop.getPops()[num_pop]
            except ValueError:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The first element of a line must be a integer which correspond to the number of the population"+ENDL)

            # Test on the marker number
            try:
                num_marker = int(line[1])
                if num_marker < 0 or num_marker >= nb_marker:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The number of markers is "+str(nb_marker)+". The marker "+str(num_marker)+" doesn't exist"+ENDL)
                marker = self.metaPop.getMarkers()[num_marker]
                marker.setSelected()
            except ValueError:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The second element of a line must be a integer which correspond to the number of the marker"+ENDL)

            genotype = line[2].split('/')
            if len(genotype) != 2:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The genotypes must be written as allele/allele"+ENDL)
            nb_allele = marker.getAlleles()

            try:
                genotype[0] = int(genotype[0])
                genotype[1] = int(genotype[1])
            except ValueError:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The alleles must be a integer which correspond to the number of the allele"+ENDL)

            if genotype[0] < 0 or genotype[0] >= nb_allele:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The number of alleles for the marker "+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotype[0])+" doesn't exist"+ENDL)
            if genotype[1] < 0 or genotype[1] >= nb_allele:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The number of alleles for the marker "+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotype[1])+" doesn't exist"+ENDL)
            geno = GenotypeLocus(genotype[0], genotype[1])
            genoInv = GenotypeLocus(genotype[1], genotype[0])

            try:
                pop.addFitness(marker, geno, float(line[3]))
                pop.addFitness(marker, genoInv, float(line[3]))
                if float(line[3]) < 0 or float(line[3]) > 1:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The fitness value must be a double between 0 and 1"+ENDL)
            except ValueError:
                self.printLineError(nameFile, num_line)
                sys.exit(FAIL+"Error: The fitness value must be a double"+ENDL)

    def read_fitness_equal(self, nameFile):
        """
        Reading of file in the parameter fitness_equal
        """
        nb_marker = self.data_vs_default('nb_marker')
        # nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_fitness:
            text = file_fitness.read()
            self.writer.addExternalFile("fitness", text)
            lines = text.split('\n')

            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue
                if len(line) != 3:
                    sys.exit(FAIL+"Error: The file "+nameFile+" is not correct. Each line must have only 3 elements."+ENDL)

                try:
                    num_marker = int(line[0])
                    if num_marker < 0 or num_marker >= nb_marker:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of markers is "+str(nb_marker)+". The marker "+str(num_marker)+" doesn't exist"+ENDL)
                    marker = self.metaPop.getMarkers()[num_marker]
                    marker.setSelected()
                    nb_allele = marker.getAlleles()
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The first element of a line must be a integer which correspond to the number of the marker"+ENDL)

                genotype = line[1].split('/')
                if len(genotype) != 2:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The genotypes must be written as allele/allele"+ENDL)

                try:
                    genotype[0] = int(genotype[0])
                    genotype[1] = int(genotype[1])
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The alleles must be a integer which correspond to the number of the allele"+ENDL)


                if genotype[0] < 0 or genotype[0] >= nb_allele:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The number of alleles for the marker "+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotype[0])+" doesn't exist"+ENDL)
                if genotype[1] < 0 or genotype[1] >= nb_allele:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The number of alleles for the marker "+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotype[1])+" doesn't exist"+ENDL)
                geno = GenotypeLocus(genotype[0], genotype[1])
                genoInv = GenotypeLocus(genotype[1], genotype[0])

                for pop in  self.metaPop.getPops():
                    try:
                        pop.addFitness(marker, geno, float(line[2]))
                        pop.addFitness(marker, genoInv, float(line[2]))
                        if float(line[2]) < 0 or float(line[2]) > 1:
                            self.printLineError(nameFile, num_line)
                            sys.exit(FAIL+"Error: The fitness value must be a double between 0 and 1"+ENDL)
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The fitness values must be a double"+ENDL)

    def read_network(self, nameFile, typeTransfert):
        """
        Reading of file in the parameters col_network or migr_network
        """
        nb_pop = self.data_vs_default('nb_pop')
        network = []
        with open(nameFile) as file_network:
            text = file_network.read()
            self.writer.addExternalFile("network_"+typeTransfert, text)
            lines = text.split('\n')

            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue

                if len(line) != nb_pop:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: Each line of the file must have a element number equal to population number."+ENDL)
                for num_elem, elem in enumerate(line):
                    try:
                        line[num_elem] = float(line[num_elem])
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The elements in the matrix of exchange must be double"+ENDL)
                network.append(line)

        if len(network) != nb_pop:
            sys.exit(FAIL+"Error: In the file "+nameFile+", the number of line must be equal to number of population."+ENDL)

        return network

    def read_genotype_equal(self, nameFile):
        """
        Reading of file in the parameter init_GenotypeFrequency_equal
        """
        nb_marker = self.data_vs_default('nb_marker')
        # nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_genotype:
            text = file_genotype.read()
            self.writer.addExternalFile("init_genotype", text)
            lines = text.split('\n')

            freq = 0
            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue
                if len(line) != 1 + nb_marker:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The file "+nameFile+" is not correct. Each line must have "+str(1+nb_marker)+" elements."+ENDL)

                genotypeMulti = []
                for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                    genotypeMarker = line[num_marker]
                    genotypeMarker = genotypeMarker.split('/')
                    if len(genotypeMarker) != 2:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The genotypes in the file "+nameFile+" must be written as allele/allele"+ENDL)
                    nb_allele = marker.getAlleles()

                    try:
                        genotypeMarker[0] = int(genotypeMarker[0])
                        genotypeMarker[1] = int(genotypeMarker[1])
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The alleles must be a integer which correspond to the number of the allele" +ENDL)

                    if genotypeMarker[0] < 0 or genotypeMarker[0] >= nb_allele:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of alleles for the marker"+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotypeMarker[0])+" doesn't exist"+ENDL)
                    if genotypeMarker[1] < 0 or genotypeMarker[1] >= nb_allele:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of alleles for the marker"+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotypeMarker[1])+" doesn't exist"+ENDL)

                    genotypeMono = GenotypeLocus(genotypeMarker[0], genotypeMarker[1])
                    genotypeMulti.append(genotypeMono)

                try:
                    freqGeno = float(line[len(line)-1])
                    freq += freqGeno
                    if freqGeno < 0 or freqGeno > 1:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The genotype frequencies must be a double between 0 and 1."+ENDL)
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The frequency values must be a double"+ENDL)

                for pop in self.metaPop.getPops():
                    pop.addGenotype(genotypeMulti, freqGeno)

            if round(freq, 3) != 1:
                sys.exit(FAIL+"Error: In the file "+nameFile+", the sum of frequencies of genotype multilocus must be 1"+ENDL)

    def read_genotype(self, nameFile):
        """
        Reading of file in the parameter init_GenotypeFrequency
        """
        nb_marker = self.data_vs_default('nb_marker')
        nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_genotype:
            text = file_genotype.read()
            self.writer.addExternalFile("init_genotype", text)
            lines = text.split('\n')

            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue
                if len(line) != 2 + nb_marker:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The file "+nameFile+" is not correct. Each line must have only "+str(2+nb_marker)+" elements."+ENDL)


                try:
                    num_pop = int(line[0])
                    if num_pop < 0 or num_pop >= nb_pop:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of populations is "+str(nb_pop)+". The population number "+str(num_pop)+" doesn't exist"+ENDL)
                    pop = self.metaPop.getPops()[num_pop]
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The first element of a line must be a integer which correspond to the number of the population"+ENDL)

                genotypeMulti = []
                for num_marker, marker in enumerate(self.metaPop.getMarkers()):
                    genotypeMarker = line[num_marker+1]
                    genotypeMarker = genotypeMarker.split('/')
                    if len(genotypeMarker) != 2:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The genotypes must be written as allele/allele"+ENDL)
                    nb_allele = marker.getAlleles()

                    try:
                        genotypeMarker[0] = int(genotypeMarker[0])
                        genotypeMarker[1] = int(genotypeMarker[1])
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The alleles must be a integer which correspond to the number of the allele"+ENDL)

                    if genotypeMarker[0] < 0 or genotypeMarker[0] >= nb_allele:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of alleles for the marker"+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotypeMarker[0])+" doesn't exist"+ENDL)

                    if genotypeMarker[1] < 0 or genotypeMarker[1] >= nb_allele:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of alleles for the marker"+str(num_marker)+" is "+str(nb_allele)+". The allele "+str(genotypeMarker[1])+" doesn't exist"+ENDL)

                    genotypeMono = GenotypeLocus(genotypeMarker[0], genotypeMarker[1])
                    genotypeMulti.append(genotypeMono)


                try:
                    freq = float(line[len(line)-1])
                    pop.addGenotype(genotypeMulti, freq)
                    if freq < 0 or freq > 1:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The genotype frequencies must be a double between 0 and 1."+ENDL)
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The frequency values must be a double"+ENDL)

        for num_pop, pop in enumerate(self.metaPop.getPops()):
            freq = 0
            if pop.getInitialisation() == [] and pop.getInitSize() != 0:
                sys.exit(FAIL+"Error: In the file "+nameFile+", all population must be initialized"+ENDL)
            for genoMulti in pop.getInitialisation():
                freq += genoMulti.getFreq()

            if round(freq, 5) != 1 and pop.getInitSize() != 0:
                sys.exit(FAIL+"Error: In the file "+nameFile+", the sum of frequencies of genotype multilocus for the population "+str(num_pop)+" doesn't equal to 1."+ENDL)


    def read_allele_equal(self, nameFile):
        """
        Reading of file in the parameter init_alleleFrequency_equal
        """
        nb_marker = self.data_vs_default('nb_marker')
        # nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_allele:
            text = file_allele.read()
            self.writer.addExternalFile("init_allele", text)
            lines = text.split('\n')

            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue

                try:
                    num_marker = int(line[0])
                    if num_marker < 0 or num_marker >= nb_marker:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of markers is "+str(nb_marker)+". The population number "+str(num_marker)+" doesn't exist"+ENDL)

                    marker = self.metaPop.getMarkers()[num_marker]
                    nb_allele = marker.getAlleles()
                    if nb_allele < len(line)-1:
                        print(WARNING+"Warning: In the file "+nameFile+" at the line "+str(num_line+1)+" there are more element than the number of allele"+ENDL)
                        self.writer.addWarning("In the file "+nameFile+" at the line "+str(num_line+1)+" there are more element than the number of allele")
                    if nb_allele > len(line)-1:
                        print(WARNING+"Warning: In the file "+nameFile+" at the line "+str(num_line+1)+" there are less element than the number of allele"+ENDL)
                        self.writer.addWarning("In the file "+nameFile+" at the line "+str(num_line+1)+" there are less element than the number of allele")

                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The first element of a line must be a integer which correspond to the number of the marker"+ENDL)

                freqAll = [0 for i in range(nb_allele)]
                for num_allele in range(len(line)-1):
                    if num_allele >= nb_allele:
                        break
                    try:
                        freqAll[num_allele] = float(line[num_allele+1])
                        if float(line[num_allele+1]) < 0 or float(line[num_allele+1]) > 1:
                            self.printLineError(nameFile, num_line)
                            sys.exit(FAIL+"Error: The allele frequencies must be between 0 and 1"+ENDL)
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The allele frequencies must be a double"+ENDL)

                if round(sum(freqAll), 3) != 1:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The sum of allele frequencies must be equal to 1."+ENDL)

                for pop in self.metaPop.getPops():
                    pop.addFreqAllele(num_marker, freqAll)

        pop = self.metaPop.getPops()[0]
        if len(pop.getInitialisation()) != nb_marker:
            sys.exit(FAIL+"Error: In the file "+nameFile+", all marker must be initialized"+ENDL)


    def read_allele(self, nameFile):
        """
        Reading of file in the parameter init_alleleFrequency
        """
        nb_marker = self.data_vs_default('nb_marker')
        nb_pop = self.data_vs_default('nb_pop')
        with open(nameFile) as file_allele:
            text = file_allele.read()
            self.writer.addExternalFile("init_allele", text)
            lines = text.split('\n')

            for num_line, line in enumerate(lines):
                line = line.replace(' ', '')
                line = line.split(',')
                if line == ['']:
                    continue

                try:
                    num_pop = int(line[0])
                    if num_pop < 0 or num_pop >= nb_pop:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of populations is "+str(nb_pop)+". The population number "+str(num_pop)+" doesn't exist"+ENDL)
                    pop = self.metaPop.getPops()[num_pop]
                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The first element of a line must be a integer which correspond to the number of the population"+ENDL)

                try:
                    num_marker = int(line[1])
                    if num_marker < 0 or num_marker >= nb_marker:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The number of markers is "+str(nb_marker)+". The population number "+str(num_marker)+" doesn't exist"+ENDL)
                    marker = self.metaPop.getMarkers()[num_marker]
                    nb_allele = marker.getAlleles()

                    if nb_allele < len(line)-2:
                        print(WARNING+"Warning: In the file "+nameFile+" at the line "+str(num_line+1)+" there are more element than the number of allele"+ENDL)
                        self.writer.addWarning("In the file "+nameFile+" at the line "+str(num_line+1)+" there are more element than the number of allele")
                    if nb_allele > len(line)-2:
                        print(WARNING+"Warning: In the file "+nameFile+" at the line "+str(num_line+1)+" there are less element than the number of allele"+ENDL)
                        self.writer.addWarning("In the file "+nameFile+" at the line "+str(num_line+1)+" there are less element than the number of allele")

                except ValueError:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The second element of a line must be a integer which correspond to the number of the marker"+ENDL)

                freqAll = [0 for i in range(nb_allele)]
                for num_allele in range(len(line)-2):
                    if num_allele >= nb_allele:
                        break
                    try:
                        freqAll[num_allele] = float(line[num_allele+2])
                        if float(line[num_allele+2]) < 0 or float(line[num_allele + 2]) > 1:
                            self.printLineError(nameFile, num_line)
                            sys.exit(FAIL+"Error: The allele frequencies must be between 0 and 1"+ENDL)
                    except ValueError:
                        self.printLineError(nameFile, num_line)
                        sys.exit(FAIL+"Error: The allele frequencies must be double"+ENDL)

                if round(sum(freqAll), 3) != 1:
                    self.printLineError(nameFile, num_line)
                    sys.exit(FAIL+"Error: The sum of allele frequencies must be equal to 1."+ENDL)

                pop.addFreqAllele(num_marker, freqAll)

        for pop in self.metaPop.getPops():
            if len(pop.getInitialisation()) != nb_marker and pop.getInitSize() != 0:
                sys.exit(FAIL+"Error: In the file"+nameFile+", all populations must be initialized"+ENDL)


    def printLineError(self, nameFile, num_line):
        """
        Print the line of file where a Error is detected.
        """
        print(FAIL+"Error in the file"+nameFile+"at the line"+str(num_line+1)+ENDL)


    def transform_in_type(self, dico):
        """
        Transform the value of parameters in the appropriate type
        """

        list_Int_Positive = ['col_nb_edge', 'migr_nb_edge', 'col_nb_cluster', 'migr_nb_cluster']
        list_Vector_Int_Positive = ['init_size', 'carr_capacity', 'nb_allele']

        list_Int_Sup_0 = ['seed', 'generations', 'replicates', 'nb_pop', 'nb_marker', 'step']

        list_0_or_1 = ['folder_time', 'col_directed', 'migr_directed', 'col_from_one', 'migr_from_one', 'migr_carrying', 'separate_replicate']

        list_Double_Positive = ['fecundity', 'col_power', 'migr_power']

        list_between_0_1 = ['percentSelf', 'col_prob_inter', 'migr_prob_inter', 'col_prob_intra', 'migr_prob_intra', 'col_rate', 'migr_rate']
        list_Vector_between_0_1 = ['optimum', 'mut_rate', 'ext_rate', 'migr_replace', 'col_keepRate', 'migr_keepRate']

        list_file = ['init_AlleleFrequency', 'init_AlleleFrequency_equal', 'init_GenotypeFrequency', 'init_GenotypeFrequency_equal', 'geneticMap', 'fitness', 'fitness_equal']

        list_string = ['folder', "col_transfer_model", "migr_transfer_model"]
        list_Vector_string = ['outputs']

        list_Network = ['col_network', 'migr_network']

        for key in dico:
            if key in list_Int_Positive:
                self.transform_Int_Positive(dico, key)

            elif key in list_Vector_Int_Positive:
                self.transform_Vector_Int_Positive(dico, key)

            elif key in list_Int_Sup_0:
                self.transform_Int_Positive(dico, key)
                self.verification_Sup_0(dico, key)

            elif key in list_0_or_1:
                self.transform_Int_Positive(dico, key)
                self.verification_0_or_1(dico, key)

            elif key in list_Double_Positive:
                self.transform_Double_Positive(dico, key)

            elif key in list_between_0_1:
                self.transform_Double_Positive(dico, key)
                self.verification_between_0_and_1(dico, key)

            elif key in list_Vector_between_0_1:
                self.transform_Vector_Double_Positive(dico, key)
                self.verification_Vector_between_0_and_1(dico, key)

            elif key in list_file:
                nameFile = dico[key]
                nameFile = nameFile.replace('*', self.directory)
                try:
                    with open(nameFile): pass
                except IOError:
                    sys.exit(FAIL+"Error! The file "+dico[key]+" doesn't open" + ENDL)
                dico[key] = nameFile

            elif key in list_string:
                if key == 'folder':
                    dico[key] = dico[key].replace('*', self.directory)

                elif key in ('col_transfer_model', 'migr_transfer_model'):
                    if dico[key] in ["excess", "friendly"]:
                        pass
                    else:
                        sys.exit(FAIL+"Error: The parameter "+key+" must be 'excess'"+ENDL)

            elif key in list_Vector_string:
                self.transform_Vector_String(dico, key)
                if key == 'outputs':
                    for elem in dico[key]:
                        if elem in ['genotype', 'haplotype', 'seed_transfert']:
                            pass
                        else:
                            sys.exit(FAIL+"Error: The parameter "+key+" must be a list component Genotype, Haplotype or Seed_transfert"+ENDL)

            elif key in list_Network:
                try:
                    dico[key] = int(dico[key])
                    if dico[key] <= 6 and dico[key] >= 0:
                        pass
                    else:
                        sys.exit(FAIL+"Error: The parameter "+key+" must be a integer between 0 and 6 or a external file"+ENDL)
                except ValueError:
                    nameFile = dico[key].replace('*', self.directory)
                    try:
                        with open(nameFile): pass
                        dico[key] = nameFile
                    except IOError:
                        sys.exit(FAIL+"Error! The file "+dico[key]+" doesn't open"+ENDL)

            else:
                sys.exit(FAIL+"Error: The key "+key+" doesn't exist."+ENDL)

    def transform_Int_Positive(self, dico, key):
        """
        Transform the value of the key in positive integer. Raise a error if is not possible
        """
        try:
            dico[key] = int(dico[key])
            if dico[key] < 0:
                sys.exit(FAIL+"Error: The parameter "+key+" must be a POSITIVE integer"+ENDL)
        except ValueError:
            sys.exit(FAIL+"Error: The parameter "+key+" must be a integer" +ENDL)

    def transform_Vector_Int_Positive(self, dico, key):
        """
        Transform the value of the key in a list of positive double. Raise a error if is not possible
        """
        elem = dico[key]
        elem = elem.replace('{', '')
        elem = elem.replace('}', '')
        listElem = elem.split(',')

        for num_elem, elem in enumerate(listElem):
            try:
                listElem[num_elem] = int(listElem[num_elem])
                if listElem[num_elem] < 0:
                    sys.exit(FAIL+"Error: The parameter "+key+" must be a list of POSITIVE integer or a POSITIVE integer"+ENDL)
            except ValueError:
                sys.exit(FAIL+"Error: The parameter "+key+" must be a list of integer or a integer"+ENDL)
        dico[key] = listElem


    def verification_Sup_0(self, dico, key):
        """
        Verification that the value is greater than 1
        """
        if dico[key] == 0:
            sys.exit(FAIL+"Error: The parameter "+key+" must be a integer greater than 1"+ENDL)


    def verification_0_or_1(self, dico, key):
        """
        Verification that the value is 0 or 1
        """
        if dico[key] != 0 and dico[key] != 1:
            sys.exit(FAIL+"Error: The parameter "+key+" must be 0 or 1"+ENDL)


    def transform_Double_Positive(self, dico, key):
        """
        Transform the value of the key in positive Double. Raise a error if is not possible
        """
        try:
            dico[key] = float(dico[key])
            if dico[key] < 0:
                sys.exit(FAIL+"Error: The parameter "+key+" must be a POSITIVE double"+ENDL)
        except ValueError:
            sys.exit(FAIL+"Error: The parameter "+key+" must be a double"+ENDL)

    def transform_Vector_Double_Positive(self, dico, key):
        """
        Transform the value of the key in a list of positive Double between 0 and 1. Raise a error if is not possible
        """
        elem = dico[key]
        elem = elem.replace('{', '')
        elem = elem.replace('}', '')
        liste = elem.split(',')

        for num_elem, elem in enumerate(liste):
            try:
                liste[num_elem] = float(liste[num_elem])
                if liste[num_elem] < 0:
                    sys.exit(FAIL+"Error: The parameter "+key+" must be a list of POSITIVE double or a POSITIVE double"+ENDL)
            except ValueError:
                sys.exit(FAIL+"Error: The parameter "+key+" must be a list of double or a double"+ENDL)

        dico[key] = liste

    def verification_between_0_and_1(self, dico, key):
        """
        Verification that the value is between 0 and 1
        """
        if dico[key] < 0 and dico[key] > 1:
            sys.exit(FAIL+"Error: The parameter "+key+" must be a double between 0 and 1"+ENDL)

    def verification_Vector_between_0_and_1(self, dico, key):
        """This function verifies if the given element is a list of elements between 0 and 1"""
        for elem in dico[key]:
            if int(elem) < 0 and int(elem) > 1:
                sys.exit(FAIL+"Error: The parameter "+key+" must be a list of double between 0 and 1"+ENDL)

    def transform_Vector_String(self, dico, key):
        """
        Transform the value of the key in list of string. Raise a error if is not possible
        """
        elem = dico[key]
        elem = elem.replace('{', '')
        elem = elem.replace('}', '')
        liste = elem.split(',')

        for num_elem, elem in enumerate(liste):
            liste[num_elem] = liste[num_elem].lower()

        dico[key] = liste

    def accomodat_list(self, key, key_elem, nb_elem, liste):
        """
        Transform the value of the key in list of string. Raise a error if is not possible
        """
        try:
            # data_key = self.data[key]
            if len(liste) < nb_elem:
                print(WARNING+"Warning: The number of "+key_elem+" is "+str(nb_elem)+". So, the vector for the parameter "+key+" is not properly defined and it was accomodated."+ENDL)
                self.writer.addWarning("The number of "+key_elem+" is "+str(nb_elem)+". So, the vector for the parameter "+key+" is not properly defined and it was accomodated.")
            elif len(liste) > nb_elem:
                print(WARNING+"Warning: The number of "+key_elem+" is "+str(nb_elem)+". So, There is too much values in the vector for the parameter "+key+" and it was accomodated."+ENDL)
                self.writer.addWarning("The number of "+key_elem+" is "+str(nb_elem)+". So, There is too much values in the vector for the parameter "+key+" and it was accomodated.")
        except KeyError:
            pass

        newList = []
        for i in range(nb_elem):
            newList.append(liste[i%len(liste)])
        return newList

    def verification(self):
        """
        Some parameters should not appear in the same settings file. This function check that.
        """
        parameter_with_equal = ['fitness', 'init_alleleFrequency', 'init_GenotypeFrequency']
        for key in parameter_with_equal:
            if key in self.data.keys():
                if key+'_equal' in self.data.keys():
                    sys.exit(FAIL+"Error: The parameters "+key+" and "+key+"_equal souldn't be present in the same time" +ENDL)

        elemInData = 0
        paramUnique = ['init_alleleFrequency', 'init_GenotypeFrequency', 'init_alleleFrequency_equal', 'init_GenotypeFrequency_equal']
        for elem in paramUnique:
            if elem in self.data:
                elemInData += 1

        if elemInData > 1:
            sys.exit(FAIL+"Error: The parameters init_AlleleFrequency and init_GenotypeFrequency souldn't be present in the same time"+ENDL)

    def data_vs_default(self, key):
        """
        Return the value of the key in the dictionnary data. If the key don't exist, the value by default is returned. If there are not value default, None is returned.
        """
        try:
            return self.data[key]
        except KeyError:
            try:
                return self.default[key]
            except KeyError:
                return None
