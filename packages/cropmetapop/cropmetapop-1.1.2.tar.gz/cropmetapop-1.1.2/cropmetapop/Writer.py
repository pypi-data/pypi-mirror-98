#!/usr/bin/env python3

""" This file contains the Writer class attributes and methods"""
#
# Writer.py
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
import time

from operator import attrgetter

class Writer:

    """
    It's the writer for the output files.
    """

    def __init__(self):

        self.results = None
        self.metaPop = None
        self.simulation = None

        self.settingsFile = None
        self.externFile = {}

        self.warnings = []
        self.separate_replicate = 0

    def createFileResult(self, results, metaPop, simulation, listTime):
        """This methods creates all the results to write in the files"""
        self.results = results
        self.metaPop = metaPop
        self.simulation = simulation
        self.timeSimul = listTime
        self.folder = self.createFolder(listTime['init'])

        self.createNumGenoMonoLocus()
        if self.results.getMulti():
            self.createNumGenoMultiLocus()
        if self.results.getExchange():
            self.createNumExchange()
        if self.results.getHaplo():
            self.createNumHaplo()

        self.copySettingsFile()
        self.copyExternalFile()
        self.timeSimul['afterWriteFile'] = time.time()
        self.createSettings()

    def addWarning(self, warning):
        """This methods shows the warnings raised during the simulation"""
        self.warnings.append(warning)

    def setSeparateReplicate(self, value):
        """This methods sets the separate_replicate attribute"""
        self.separate_replicate = value

    def setSettingsFile(self, text):
        """This methods sets the name of the settingsFile"""
        self.settingsFile = text

    def addExternalFile(self, name, text):
        """This method adds an external file name"""
        self.externFile[name] = text

    def createFolder(self, initTime):
        """This method create the output folder"""
        nameFolder = self.results.getFolder()
        timeFolder = self.results.getFolderTime()
        initTime = time.localtime(initTime)
        if timeFolder == 0:
            pass
        else:
            nameFolder = nameFolder +'_'+ str(initTime.tm_year)+'_'+str(initTime.tm_mon)+'_'+str(initTime.tm_mday)+'_'+str(initTime.tm_hour)+':'+str(initTime.tm_min)+':'+str(initTime.tm_sec)
        if nameFolder != '':
            os.mkdir(nameFolder)
            return nameFolder+'/'
        else:
            return nameFolder

    def copySettingsFile(self):
        """This method copies the settingsFile to the output folder"""
        fileSettings = open(self.folder+'settingsFile', 'w')
        fileSettings.write(self.settingsFile)
        fileSettings.close()

    def copyExternalFile(self):
        """This method copies the external file to the output folder"""

        for nameFile in self.externFile:
            fileSettings = open(self.folder+nameFile, 'w')
            fileSettings.write(self.externFile[nameFile])
            fileSettings.close()

    def createSettings(self):

        """
        Create the setting.log file
        """

        file_log = open(self.folder+'setting.log', 'w')

        file_log.write('=====================================================================\n')
        file_log.write('=====================================================================\n')
        file_log.write('                       CropMetaPop Verion 1.1.0.6                    \n')
        file_log.write('=====================================================================\n')
        file_log.write('=====================================================================\n')
        file_log.write('\n')
        file_log.write('\n')

        file_log.write('SIMULATION\n')
        file_log.write('---------------------------------------------------------------------\n')
        file_log.write('\n')
        file_log.write('  TIME \n')
        file_log.write('    Global time: '+str(round(self.timeSimul['afterWriteFile']-self.timeSimul['init'], 4))+'s\n')
        file_log.write('      Time of read settings: '+str(round(self.timeSimul['beforeRun']-self.timeSimul['init'], 4))+'s\n')
        file_log.write('      Time of run: '+str(round(self.timeSimul['afterRun']-self.timeSimul['beforeRun'], 4))+'s\n')
        file_log.write('      Time of write result: '+str(round(self.timeSimul['afterWriteFile']-self.timeSimul['afterRun'], 4))+'s\n')
        file_log.write('\n')
        if self.warnings:
            file_log.write('  Warning\n')
            for warning in self.warnings:
                file_log.write('    '+warning+'\n')
        file_log.write('\n')

        goodFinal = 1
        for rep in range(self.simulation.getReplicate()):
            if (self.simulation.getGenerations() -1) != self.simulation.getFinalGeneration()[rep]:
                file_log.write('  In the replicate '+str(rep)+', your run is terminated before the end of generations (at '+str(self.simulation.getFinalGeneration()[rep])+' generation). The metapopulation is empty.\n')
                goodFinal = 0

        if goodFinal:
            file_log.write('  Your run is terminated successfully\n')

        file_log.write('--------------------------------------------------------------------\n')
        file_log.write('\n')
        file_log.write('SETTINGS\n')
        file_log.write('--------------------------------------------------------------------\n')
        file_log.write('  Simulation\n')
        file_log.write('    Generation: '+str(self.simulation.getGenerations())+'\n')
        file_log.write('    Replicate: '+str(self.simulation.getReplicate())+'\n')
        file_log.write('    Seed: '+str(self.simulation.getSeed())+'\n')
        file_log.write('\n')
        file_log.write('  Bredding\n')
        file_log.write('    Percent Self: '+str(self.metaPop.getSelfing())+' \n')
        file_log.write('    Fecundity: '+str(self.metaPop.getFecundity())+' \n')
        file_log.write('\n')
        file_log.write('  Meta-Population\n')
        file_log.write('    Number of population: '+str(len(self.metaPop.getPops())) +'\n\n')

        text = []
        col_friendly = 0
        migr_friendly = 0
        if self.simulation.getColModel() == 'friendly':
            col_friendly = 1
        if self.simulation.getMigrModel() == 'friendly':
            migr_friendly = 1

        line1 = ' Number | Init Size | Carrying capacity | Optimum | Extinction rate | Replace rate '
        if col_friendly:
            line1 += '| Col Keep Rate '
        if migr_friendly:
            line1 += '| Migr Keep Rate '

        text.append(line1)
        for num_pop, pop in enumerate(self.metaPop.getPops()):
            line = 'Pop '+str(num_pop)
            line += ' |'+str(pop.getInitSize())
            line += ' |'+str(pop.getCarryingCapacity())
            line += ' |'+str(pop.getOptimum())
            line += ' |'+str(pop.getRateExtinction())
            line += ' |'+str(pop.getRateReplace())
            if col_friendly:
                line += ' |'+str(pop.getColKeepRate())
            if migr_friendly:
                line += ' |'+str(pop.getMigrKeepRate())
            line += ' '
            text.append(line)

        maxSize = [0 for i in range(len(text[0].split('|')))]
        for line in text:
            elems = line.split('|')
            for num_elem, elem in enumerate(elems):
                if maxSize[num_elem] < len(elem):
                    maxSize[num_elem] = len(elem)

        newText = []
        for line in text:
            newline = []
            elems = line.split('|')
            for num_elem, elem in enumerate(elems):
                for i in range(maxSize[num_elem] - len(elem)):
                    elem = ' '+ elem
                newline.append(elem)
            newline = '|'.join(newline)
            newText.append(newline)

        for line in newText:
            file_log.write('    |'+line+'|\n')

        file_log.write('\n')
        file_log.write('  Markers\n')
        file_log.write('    Number of markers: '+str(len(self.metaPop.getMarkers())) +'\n\n')

        text = []
        line1 = ' Number | Selected | number Allele | Chromosome | Distance | Mutation rate '
        text.append(line1)
        for num_marker, marker in enumerate(self.metaPop.getMarkers()):
            line = ' Marker '+str(num_marker)+' |'
            if marker.getSelected():
                line += 'Yes |'
            else:
                line += 'No |'
            line += str(marker.getAlleles())+' |'
            line += str(marker.getChrom())+' |'
            line += str(marker.getDistance())+' |'
            line += str(marker.getRateMutation())+' '
            text.append(line)

        maxSize = [0 for i in range(len(text[0].split('|')))]
        for line in text:
            elems = line.split('|')
            for num_elem, elem in enumerate(elems):
                if maxSize[num_elem] < len(elem):
                    maxSize[num_elem] = len(elem)

        newText = []
        for num_line, line in enumerate(text):
            newline = []
            elems = line.split('|')
            for num_elem, elem in enumerate(elems):
                for i in range(maxSize[num_elem] - len(elem)):
                    elem = ' '+ elem
                newline.append(elem)
            newline = '|'.join(newline)
            newText.append(newline)

        for line in newText:
            file_log.write('    |'+line+'|\n')

        file_log.write('\n')

        networkColonisation = self.metaPop.getNetworkColonisation()
        networkMigration = self.metaPop.getNetworkMigration()
        if networkColonisation != 0 or networkMigration != 0:
            file_log.write('  Network\n')
            if networkColonisation != 0:
                file_log.write('    Colonisation\n')
                file_log.write('      Model of Colonisation:\n')
                file_log.write('      Adjacency matrix:\n\n')

                text = []
                line = ' '
                for num_popFrom in range(len(self.metaPop.getPops())):
                    line += '|'
                    line += ' Pop '+str(num_popFrom)+' '
                text.append(line)
                for num_popFrom, popFrom in enumerate(networkColonisation):
                    line = ' Pop '+str(num_popFrom)
                    for num_popTo in range(len(networkColonisation[num_popFrom])):
                        line += ' |'
                        line += str(networkColonisation[num_popFrom][num_popTo])+ ' '
                    text.append(line)

                maxSize = [0 for i in range(len(self.metaPop.getPops())+1)]
                for line in text:
                    elems = line.split('|')
                    for num_elem, elem in enumerate(elems):
                        if maxSize[num_elem] < len(elem):
                            maxSize[num_elem] = len(elem)

                newText = []
                for num_line, line in enumerate(text):
                    newline = []
                    elems = line.split('|')
                    for num_elem, elem in enumerate(elems):
                        for i in range(maxSize[num_elem] - len(elem)):
                            elem = ' '+ elem
                        newline.append(elem)
                    newline = '|'.join(newline)
                    newText.append(newline)

                for line in newText:
                    file_log.write('      |'+line+'|\n')

                file_log.write('\n')

            else:
                file_log.write("    No Colonisation\n\n")

            if networkMigration != 0:
                file_log.write('    Migration\n')
                file_log.write('      Model of Migration:\n')
                file_log.write('      Adjacency matrix:\n\n')

                text = []
                line = ' '
                for num_popFrom in range(len(self.metaPop.getPops())):
                    line += '|'
                    line += ' Pop '+str(num_popFrom)
                text.append(line)
                for num_popFrom, popFrom in enumerate(networkMigration):
                    line = ' Pop '+str(num_popFrom)
                    for num_popTo in range(len(networkMigration[num_popFrom])):
                        line += '|'
                        line += str(networkMigration[num_popFrom][num_popTo])+' '
                    text.append(line)

                maxSize = [0 for i in range(len(self.metaPop.getPops())+1)]
                for line in text:
                    elems = line.split('|')
                    for num_elem, elem in enumerate(elems):
                        if maxSize[num_elem] < len(elem):
                            maxSize[num_elem] = len(elem)

                newText = []
                for num_line, line in enumerate(text):
                    newline = []
                    elems = line.split('|')
                    for num_elem, elem in enumerate(elems):
                        for i in range(maxSize[num_elem] - len(elem)):
                            elem = ' '+ elem
                        newline.append(elem)
                    newline = '|'.join(newline)
                    newText.append(newline)

                for line in newText:
                    file_log.write('      |'+line+' |\n')

            else:

                file_log.write("    No Migration \n")
        else:
            file_log.write("  No seed circulation\n")

        file_log.write('\n')
        file_log.write('--------------------------------------------------------------------\n')
        file_log.close()


    def createNumGenoMonoLocus(self):
        """
        Create the file GenotypeMono.csv.
        """
        if not self.separate_replicate:
            generations = self.simulation.getGenerations()
            file_mono = open(self.folder+'GenotypeMono.csv', 'w')
            file_mono.write('Replicate,Population,Marker,Genotype')
            for generation in range(generations):
                file_mono.write(", Gen "+str(generation))
            file_mono.write('\n')

            numResult = 0
            resultPrec = None
            for resultMono in sorted(self.results.getResultGenoMono(), key=attrgetter("replicat", "subPop", "locus", "genotype", "gen")):
                if numResult == 0:
                    file_mono.write(str(resultMono.getReplicat()))
                    file_mono.write(','+str(resultMono.getSubPop()))
                    file_mono.write(','+str(resultMono.getLocus()))
                    genoMono = resultMono.getGenotype()
                    file_mono.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                    for i in range(resultMono.getGeneration()):
                        file_mono.write(','+str(0))
                    file_mono.write(','+str(resultMono.getValue()))
                    resultPrec = resultMono
                    numResult = 1
                else:
                    if resultPrec.getReplicat() == resultMono.getReplicat() and  resultPrec.getSubPop() == resultMono.getSubPop() and resultPrec.getLocus() == resultMono.getLocus() and resultPrec.getGenotype() == resultMono.getGenotype():
                        for i in range(resultMono.getGeneration() - resultPrec.getGeneration() -1):
                            file_mono.write(','+str(0))
                        file_mono.write(','+str(resultMono.getValue()))
                        resultPrec = resultMono
                    else:
                        for i in range(generations - resultPrec.getGeneration()-1):
                            file_mono.write(','+str(0))
                        file_mono.write("\n")
                        file_mono.write(str(resultMono.getReplicat()))
                        file_mono.write(','+str(resultMono.getSubPop()))
                        file_mono.write(','+str(resultMono.getLocus()))
                        genoMono = resultMono.getGenotype()
                        file_mono.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                        for i in range(resultMono.getGeneration()):
                            file_mono.write(','+str(0))
                        file_mono.write(','+str(resultMono.getValue()))
                        resultPrec = resultMono

            for i in range(generations - resultPrec.getGeneration()-1):
                file_mono.write(','+str(0))
            file_mono.close()

        else:
            for rep in range(self.simulation.getReplicate()):
                generations = self.simulation.getGenerations()
                file_mono = open(self.folder+'GenotypeMono_Rep'+str(rep)+'.csv', 'w')
                file_mono.write('Replicate,Population,Marker,Genotype')
                for generation in range(generations):
                    file_mono.write(", Gen "+str(generation))
                file_mono.write('\n')

                numResult = 0
                resultPrec = None
                for resultMono in sorted(self.results.getResultGenoMono(), key=attrgetter("replicat", "subPop", "locus", "genotype", "gen")):
                    if resultMono.getReplicat() == rep:
                        if numResult == 0:
                            file_mono.write(str(resultMono.getReplicat()))
                            file_mono.write(','+str(resultMono.getSubPop()))
                            file_mono.write(','+str(resultMono.getLocus()))
                            genoMono = resultMono.getGenotype()
                            file_mono.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                            for i in range(resultMono.getGeneration()):
                                file_mono.write(','+str(0))
                            file_mono.write(','+str(resultMono.getValue()))
                            resultPrec = resultMono
                            numResult = 1
                        else:
                            if resultPrec.getReplicat() == resultMono.getReplicat() and  resultPrec.getSubPop() == resultMono.getSubPop() and resultPrec.getLocus() == resultMono.getLocus() and resultPrec.getGenotype() == resultMono.getGenotype():
                                for i in range(resultMono.getGeneration() - resultPrec.getGeneration() -1):
                                    file_mono.write(','+str(0))
                                file_mono.write(','+str(resultMono.getValue()))
                                resultPrec = resultMono
                            else:
                                for i in range(generations - resultPrec.getGeneration()-1):
                                    file_mono.write(','+str(0))
                                file_mono.write("\n")
                                file_mono.write(str(resultMono.getReplicat()))
                                file_mono.write(','+str(resultMono.getSubPop()))
                                file_mono.write(','+str(resultMono.getLocus()))
                                genoMono = resultMono.getGenotype()
                                file_mono.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                                for i in range(resultMono.getGeneration()):
                                    file_mono.write(','+str(0))
                                file_mono.write(','+str(resultMono.getValue()))
                                resultPrec = resultMono

                for i in range(generations - resultPrec.getGeneration()-1):
                    file_mono.write(','+str(0))
                file_mono.close()


    def createNumGenoMultiLocus(self):
        """
        Create the file GenotypeMulti.csv.
        """
        if not self.separate_replicate:
            generations = self.simulation.getGenerations()
            file_multi = open(self.folder+'GenotypeMulti.csv', 'w')
            file_multi.write('Replicate,Population')
            for num_locus in range(len(self.metaPop.getMarkers())):
                file_multi.write(", Marker "+str(num_locus))
            for generation in range(generations):
                file_multi.write(", Gen "+str(generation))
            file_multi.write('\n')

            numResult = 0
            resultPrec = None
            for resultMulti in sorted(self.results.getResultGenoMulti(), key=attrgetter("replicat", "subPop", "genotypeMulti", "gen")):
                #print resultMulti
                if numResult == 0:
                    file_multi.write(str(resultMulti.getReplicat()))
                    file_multi.write(','+str(resultMulti.getSubPop()))
                    genoMulti = resultMulti.getGenoMulti().getLocusGenotype()
                    for locus in genoMulti:
                        genoMono = genoMulti[locus]
                        file_multi.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                    for i in range(resultMulti.getGeneration()):
                        file_multi.write(','+str(0))
                    file_multi.write(','+str(resultMulti.getValue()))
                    resultPrec = resultMulti
                    numResult = 1
                else:
                    if resultPrec.getGenoMulti() == resultMulti.getGenoMulti():
                        for i in range(resultMulti.getGeneration() - resultPrec.getGeneration() -1):
                            file_multi.write(','+str(0))
                        file_multi.write(','+str(resultMulti.getValue()))
                        resultPrec = resultMulti
                    else:
                        for i in range(generations - resultPrec.getGeneration()-1):
                            file_multi.write(','+str(0))
                        file_multi.write("\n")
                        file_multi.write(str(resultMulti.getReplicat()))
                        file_multi.write(','+str(resultMulti.getSubPop()))
                        genoMulti = resultMulti.getGenoMulti().getLocusGenotype()
                        for locus in genoMulti:
                            genoMono = genoMulti[locus]
                            file_multi.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                        for i in range(resultMulti.getGeneration()):
                            file_multi.write(','+str(0))
                        file_multi.write(','+str(resultMulti.getValue()))
                        resultPrec = resultMulti

            for i in range(generations - resultPrec.getGeneration()-1):
                file_multi.write(','+str(0))

            file_multi.close()

        else:
            for rep in range(self.simulation.getReplicate()):
                generations = self.simulation.getGenerations()
                file_multi = open(self.folder+'GenotypeMulti_Rep'+str(rep)+'.csv', 'w')
                file_multi.write('Replicate,Population')
                for num_locus in range(len(self.metaPop.getMarkers())):
                    file_multi.write(", Marker "+str(num_locus))
                for generation in range(generations):
                    file_multi.write(", Gen "+str(generation))
                file_multi.write('\n')

                numResult = 0
                resultPrec = None
                for resultMulti in sorted(self.results.getResultGenoMulti(), key=attrgetter("replicat", "subPop", "genotypeMulti", "gen")):
                    #print resultMulti
                    if resultMulti.getReplicat() == rep:
                        if numResult == 0:
                            file_multi.write(str(resultMulti.getReplicat()))
                            file_multi.write(','+str(resultMulti.getSubPop()))
                            genoMulti = resultMulti.getGenoMulti().getLocusGenotype()
                            for locus in genoMulti:
                                genoMono = genoMulti[locus]
                                file_multi.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                            for i in range(resultMulti.getGeneration()):
                                file_multi.write(','+str(0))
                            file_multi.write(','+str(resultMulti.getValue()))
                            resultPrec = resultMulti
                            numResult = 1
                        else:
                            if resultPrec.getGenoMulti() == resultMulti.getGenoMulti():
                                for i in range(resultMulti.getGeneration() - resultPrec.getGeneration() -1):
                                    file_multi.write(','+str(0))
                                file_multi.write(','+str(resultMulti.getValue()))
                                resultPrec = resultMulti
                            else:
                                for i in range(generations - resultPrec.getGeneration()-1):
                                    file_multi.write(','+str(0))
                                file_multi.write("\n")
                                file_multi.write(str(resultMulti.getReplicat()))
                                file_multi.write(','+str(resultMulti.getSubPop()))
                                genoMulti = resultMulti.getGenoMulti().getLocusGenotype()
                                for locus in genoMulti:
                                    genoMono = genoMulti[locus]
                                    file_multi.write(','+str(genoMono.getAll1())+'/'+str(genoMono.getAll2()))
                                for i in range(resultMulti.getGeneration()):
                                    file_multi.write(','+str(0))
                                file_multi.write(','+str(resultMulti.getValue()))
                                resultPrec = resultMulti

                for i in range(generations - resultPrec.getGeneration()-1):
                    file_multi.write(','+str(0))
                file_multi.close()

    def createNumHaplo(self):
        """
        Create the file Haplotype.csv.
        """

        if not self.separate_replicate:
            generations = self.simulation.getGenerations()
            file_haplo = open(self.folder+'Haplotype.csv', 'w')
            file_haplo.write('Replicate,Population ')
            for num_locus in range(len(self.metaPop.getMarkers())):
                file_haplo.write(", Marker "+str(num_locus))
            for generation in range(generations):
                file_haplo.write(", Gen "+str(generation))
            file_haplo.write('\n')

            numResult = 0
            resultPrec = None
            for resultHaplo in sorted(self.results.getResultHaplotype(), key=attrgetter("replicat", "subPop", "haplotype", "gen")):
                #print resultMulti
                if numResult == 0:
                    file_haplo.write(str(resultHaplo.getReplicat()))
                    file_haplo.write(','+str(resultHaplo.getSubPop()))
                    haplotype = resultHaplo.getHaplotype()
                    for allele in haplotype:
                        file_haplo.write(','+str(allele))
                    for i in range(resultHaplo.getGeneration()):
                        file_haplo.write(','+str(0))
                    file_haplo.write(','+str(resultHaplo.getValue()))
                    resultPrec = resultHaplo
                    numResult = 1
                else:
                    if resultPrec.getReplicat() == resultHaplo.getReplicat() and resultPrec.getSubPop() == resultHaplo.getSubPop() and resultPrec.getHaplotype() == resultHaplo.getHaplotype():
                        for i in range(resultHaplo.getGeneration() - resultPrec.getGeneration() -1):
                            file_haplo.write(','+str(0))
                        file_haplo.write(','+str(resultHaplo.getValue()))
                        resultPrec = resultHaplo
                    else:
                        for i in range(generations - resultPrec.getGeneration()-1):
                            file_haplo.write(','+str(0))
                        file_haplo.write("\n")
                        file_haplo.write(str(resultHaplo.getReplicat()))
                        file_haplo.write(','+str(resultHaplo.getSubPop()))
                        haplotype = resultHaplo.getHaplotype()
                        for allele in haplotype:
                            file_haplo.write(','+str(allele))
                        for i in range(resultHaplo.getGeneration()):
                            file_haplo.write(','+str(0))
                        file_haplo.write(','+str(resultHaplo.getValue()))
                        resultPrec = resultHaplo

            for i in range(generations - resultPrec.getGeneration()-1):
                file_haplo.write(','+str(0))
            file_haplo.close()

        else:
            for rep in range(self.simulation.getReplicate()):
                generations = self.simulation.getGenerations()
                file_haplo = open(self.folder+'Haplotype_Rep'+str(rep)+'.csv', 'w')
                file_haplo.write('Replicate,Population')
                for num_locus in range(len(self.metaPop.getMarkers())):
                    file_haplo.write(", Marker "+str(num_locus))
                for generation in range(generations):
                    file_haplo.write(", Gen "+str(generation))
                file_haplo.write('\n')

                numResult = 0
                resultPrec = None
                for resultHaplo in sorted(self.results.getResultHaplotype(), key=attrgetter("replicat", "subPop", "haplotype", "gen")):
                    #print resultMulti
                    if resultHaplo.getReplicat() == rep:
                        if numResult == 0:
                            file_haplo.write(str(resultHaplo.getReplicat()))
                            file_haplo.write(','+str(resultHaplo.getSubPop()))
                            haplotype = resultHaplo.getHaplotype()
                            for allele in haplotype:
                                file_haplo.write(','+str(allele))
                            for i in range(resultHaplo.getGeneration()):
                                file_haplo.write(','+str(0))
                            file_haplo.write(','+str(resultHaplo.getValue()))
                            resultPrec = resultHaplo
                            numResult = 1
                        else:
                            if resultPrec.getReplicat() == resultHaplo.getReplicat() and resultPrec.getSubPop() == resultHaplo.getSubPop() and resultPrec.getHaplotype() == resultHaplo.getHaplotype():
                                for i in range(resultHaplo.getGeneration() - resultPrec.getGeneration() -1):
                                    file_haplo.write(','+str(0))
                                file_haplo.write(str(resultHaplo.getValue())+',')
                                resultPrec = resultHaplo
                            else:
                                for i in range(generations - resultPrec.getGeneration()-1):
                                    file_haplo.write(','+str(0))
                                file_haplo.write("\n")
                                file_haplo.write(str(resultHaplo.getReplicat()))
                                file_haplo.write(','+str(resultHaplo.getSubPop()))
                                haplotype = resultHaplo.getHaplotype()
                                for allele in haplotype:
                                    file_haplo.write(','+str(allele))
                                for i in range(resultHaplo.getGeneration()):
                                    file_haplo.write(','+str(0))
                                file_haplo.write(','+str(resultHaplo.getValue()))
                                resultPrec = resultHaplo

                for i in range(generations - resultPrec.getGeneration()-1):
                    file_haplo.write(','+str(0))
                file_haplo.close()

    def createNumExchange(self):
        """
        Create the files of seed transfer.
        """

        if len(self.results.getResultExchangeColonisation()):
            self.createNumExchangeSpe("Colonization")
        if len(self.results.getResultExchangeMigration()):
            self.createNumExchangeSpe("Migration")

    def createNumExchangeSpe(self, typeExchange):
        """
        Create one file of seed transfer for a type of exchange.

        :param typeExchange: type of exchange (Migration or Colonization)
        :type typeExchange: String
        """

        if not self.separate_replicate:
            generations = self.simulation.getGenerations()
            file_exchange = open(self.folder+'numTransfert'+typeExchange+'.csv', 'w')
            file_exchange.write('Replicate,Source,Target')
            for generation in range(self.simulation.getGenerations()):
                file_exchange.write(", Gen "+str(generation+1))
            file_exchange.write('\n')

            if typeExchange == "Colonization":
                listeResult = self.results.getResultExchangeColonisation()
            else:
                listeResult = self.results.getResultExchangeMigration()

            numResult = 0
            resultPrec = None
            for resultExchange in sorted(listeResult, key=attrgetter("replicat", "popFrom", "popTo", "gen")):
                if numResult == 0:
                    file_exchange.write(str(resultExchange.getReplicat()))
                    file_exchange.write(','+str(resultExchange.getPopFrom()))
                    file_exchange.write(','+str(resultExchange.getPopTo()))
                    for i in range(resultExchange.getGeneration()):
                        file_exchange.write(','+str(0))
                    file_exchange.write(','+str(resultExchange.getValue()))
                    resultPrec = resultExchange
                    numResult = 1
                else:
                    if resultPrec.getReplicat() == resultExchange.getReplicat() and resultPrec.getPopFrom() == resultExchange.getPopFrom() and resultPrec.getPopTo() == resultExchange.getPopTo():
                        for i in range(resultExchange.getGeneration() - resultPrec.getGeneration() -1):
                            file_exchange.write(','+str(0))
                        file_exchange.write(','+str(resultExchange.getValue()))
                        resultPrec = resultExchange
                    else:
                        for i in range(generations - resultPrec.getGeneration()-1):
                            file_exchange.write(','+str(0))
                        file_exchange.write("\n")
                        file_exchange.write(str(resultExchange.getReplicat()))
                        file_exchange.write(','+str(resultExchange.getPopFrom()))
                        file_exchange.write(','+str(resultExchange.getPopTo()))
                        for i in range(resultExchange.getGeneration()):
                            file_exchange.write(','+str(0))
                        file_exchange.write(','+str(resultExchange.getValue()))
                        resultPrec = resultExchange

            for i in range(generations - resultPrec.getGeneration()-1):
                file_exchange.write(','+str(0))
            file_exchange.close()

        else:
            for rep in range(self.simulation.getReplicate()):
                generations = self.simulation.getGenerations()
                file_exchange = open(self.folder+'numTransfert'+typeExchange+'_Rep'+str(rep)+'.csv', 'w')
                file_exchange.write('Replicat,Source,Target')
                for generation in range(self.simulation.getGenerations()):
                    file_exchange.write(", Gen "+str(generation+1))
                file_exchange.write('\n')

                if typeExchange == "Colonization":
                    listeResult = self.results.getResultExchangeColonisation()
                else:
                    listeResult = self.results.getResultExchangeMigration()

                numResult = 0
                resultPrec = None
                for resultExchange in sorted(listeResult, key=attrgetter("replicat", "popFrom", "popTo", "gen")):
                    if resultExchange.getReplicat() == rep:
                        if numResult == 0:
                            file_exchange.write(str(resultExchange.getReplicat()))
                            file_exchange.write(','+str(resultExchange.getPopFrom()))
                            file_exchange.write(','+str(resultExchange.getPopTo()))
                            for i in range(resultExchange.getGeneration()):
                                file_exchange.write(','+str(0))
                            file_exchange.write(','+str(resultExchange.getValue()))
                            resultPrec = resultExchange
                            numResult = 1
                        else:
                            if resultPrec.getReplicat() == resultExchange.getReplicat() and resultPrec.getPopFrom() == resultExchange.getPopFrom() and resultPrec.getPopTo() == resultExchange.getPopTo():
                                for i in range(resultExchange.getGeneration() - resultPrec.getGeneration() -1):
                                    file_exchange.write(','+str(0))
                                file_exchange.write(','+str(resultExchange.getValue()))
                                resultPrec = resultExchange
                            else:
                                for i in range(generations - resultPrec.getGeneration()-1):
                                    file_exchange.write(','+str(0))
                                file_exchange.write("\n")
                                file_exchange.write(str(resultExchange.getReplicat()))
                                file_exchange.write(','+str(resultExchange.getPopFrom()))
                                file_exchange.write(','+str(resultExchange.getPopTo()))
                                for i in range(resultExchange.getGeneration()):
                                    file_exchange.write(','+str(0))
                                file_exchange.write(','+str(resultExchange.getValue()))
                                resultPrec = resultExchange

                for i in range(generations - resultPrec.getGeneration()-1):
                    file_exchange.write(','+str(0))

                file_exchange.close()
