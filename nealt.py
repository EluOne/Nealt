#!/usr/bin/python
'Nova Echo Audit Log Tool'
# Copyright (C) 2013  Tim Cumming
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Tim Cumming aka Elusive One
# Created: 28/02/13

import argparse
import sys
import os
from operator import itemgetter, attrgetter


# Start of main() function
def main():

    parser = argparse.ArgumentParser(description='Nova Echo Audit Log Tool')
    parser.add_argument("log", nargs="+",
                        help="list of log files")
    parser.add_argument("-c", "--compact", action="store_true",
                        help="compact mode. output is reduced to mineral groups")

    args = parser.parse_args()
    logs = args.log

    #Initialise lists
    oreGroups = []
    ice = []
    salvage = []
    commodities = []
    minerals = []
    other = []
    
    pilots = []
    icePilots = []
    orePilots = []
    
    oreTotals = []
    iceTotals = []

    # EVE ore groups as a dictionary
    OreTypes = {'Arkonor': 'Arkonor', 'Crimson Arkonor': 'Arkonor', 'Prime Arkonor': 'Arkonor', 
                'Bistot': 'Bistot', 'Monoclinic Biscot': 'Biscot', 'Triclinic Biscot': 'Biscot',
                'Crokite': 'Crokite', 'Crystalline Crokite': 'Crokite', 'Sharp Crokite': 'Crokite',
                'Dark Ochre': 'Dark Ochre', 'Obsidian Ochre': 'Dark Ochre', 'Onyx Ochre': 'Dark Ochre',
                'Gneiss': 'Gneiss', 'Iridescent Gneiss': 'Gneiss', 'Prismatic Gneiss': 'Gneiss',
                'Hedbergite': 'Hedbergite', 'Glazed Hedbergite': 'Hedbergite', 'Vitric Hedbergite': 'Hedbergite',
                'Hemorphite': 'Hemorphite', 'Radiant Hemorphite': 'Hemorphite', 'Vivid Hemorphite': 'Hemorphite',
                'Jaspet': 'Jaspet', 'Jaspet': 'Pristine Jaspet', 'Pure Jaspet': 'Jaspet',
                'Kernite': 'Kernite', 'Fiery Kernite': 'Kernite', 'Luminous Kernite': 'Kernite',
                'Mercoxit': 'Mercoxit', 'Magma Mercoxit': 'Mercoxit', 'Vitreous Mercoxit': 'Mercoxit',
                'Omber': 'Omber', 'Golden Omber': 'Omber', 'Silvery Omber': 'Omber',
                'Plagioclase': 'Plagioclase', 'Azure Plagioclase': 'Plagioclase', 'Rich Plagioclase': 'Plagioclase',
                'Pyroxeres': 'Pyroxeres', 'Solid Pyroxeres': 'Pyroxeres',
                'Scordite': 'Scordite', 'Condensed Scordite': 'Scordite', 'Massive Scordite': 'Scordite',
                'Spodumain': 'Spodumain', 'Gleaming Spodumain': 'Spodumain', 'Bright Spodumain': 'Spodumain', 
                'Veldspar': 'Veldspar', 'Concentrated Veldspar': 'Veldspar', 'Dense Veldspar': 'Veldspar'}
    # EVE ore and ice volumes per unit as a dictionary
    OreWeights = {'Arkonor': 16, 'Bistot': 16, 'Crokite': 16, 'Dark Ochre': 8,
                  'Gneiss': 5, 'Hedbergite': 3, 'Hemorphite': 3, 'Jaspet': 2,
                  'Kernite': 1.2, 'Mercoxit': 40, 'Omber': 0.6, 'Plagioclase': 0.35,
                  'Pyroxeres': 0.3, 'Scordite': 0.15, 'Spodumain': 16, 'Veldspar': 0.1}
    IceTypes = {'Blue Ice': 1000, 'White Glaze': 1000, 'Pristine White Glaze': 1000,
                'Glacial Mass': 1000, 'Smooth Glacial Mass': 1000, 'Blue Ice': 1000,
                'Thick Blue Ice': 1000, 'Clear Icicle': 1000, 'Enriched Clear Icicle': 1000,
                'Glare Crust': 1000, 'Dark Glitter': 1000, 'Gelidus': 1000, 'Krystallos': 1000}
    SalvageTypes = ['Alloyed Tritanium Bar', 'Metal Scraps','Charred Micro Circuit', 'Tangled Power Conduit', 
                    'Contaminated Lorentz Fluid', 'Tripped Power Circuit','Malfunctioning Shield Emitter',
                    'Armor Plates', 'Conductive Polymer', 'Contaminated Nanite Compound','Damaged Artificial Neural Network',
                    'Scorched Telemetry Processor','Smashed Trigger Unit', 'Burned Logic Circuit','Fried Interface Circuit',
                    'Ward Console', 'Broken Drone Transceiver', 'Defective Current Pump']
    MineralTypes = ['Tritanium', 'Pyerite', 'Mexallon', 'Isogen','Nocxium', 'Zydrine', 'Megacyte', 'Morphite']

    # Planetary Interaction:
    # Raw Materials:
    PiRawMats = ['Aqueous Liquids', 'Autotrophs', 'Base Metals', 'Carbon Compounds', 'Complex Organisms',
                 'Felsic Magma', 'Heavy Metals', 'Ionic Solutions', 'Micro Organisms', 'Noble Gas',
                 'Noble Metals', 'Non-CS Crystals', 'Planktic Colonies', 'Reactive Gas', 'Suspended Plasma']

    # Basic Commodities:
    PiBasic = ['Water', 'Industrial Fibers', 'Reactive Metals', 'Biofuels', 'Proteins', 'Silicon', 'Toxic Metals',
               'Electrolytes', 'Bacteria', 'Oxygen', 'Precious Metals', 'Chiral Structures', 'Biomass',
               'Oxidizing Compound', 'Plasmoids']

    # Advanced: 2 Part Commodities:
    PiAdvanced2P = ['Biocells', 'Construction Blocks', 'Consumer Electronics', 'Coolant', 'Enriched Uranium', 'Fertilizer',
                  'Gen. Enhanced Livestock', 'Livestock', 'Mechanical Parts', 'Microfiber Shielding', 'Miniature Electronics',
                  'Nanites', 'Oxides', 'Polyaramids', 'Polytextiles', 'Rocket Fuel', 'Silicate Glass', 'Superconductors',
                  'Supertensile Plastics', 'Synthetic Oil', 'Test Cultures', 'Transmitter', 'Viral Agent', 'Water-Cooled CPU']

    # Advanced: 3 Part Commodities:
    PiAdvanced3P = ['Biotech Research Reports', 'Camera Drones', 'Condensates', 'Cryoprotectant Solution', 'Data Chips',
                    'Gel-Matrix Biopaste', 'Guidance Systems', 'Hazmat Detection Systems', 'Hermetic Membranes',
                    'High-Tech Transmitters', 'Industrial Explosives', 'Neocoms', 'Nuclear Reactors', 'Planetary Vehicles',
                    'Robotics', 'Smartfab Units', 'Supercomputers', 'Synthetic Synapses', 'Transcranial Microcontroller',
                    'Ukomi Super Conductors', 'Vaccines']

    # High Tech:
    PiHighTech = ['Broadcast Node', 'Integrity Response Drones', 'Nano-Factory', 'Organic Mortar Applicators', 'Recursive Computing Module',
                  'Self-Harmonizing Power Core', 'Sterile Conduits', 'Wetware Mainframe']

    # Lets just combine them all for now, I'm thinking of separating them out later.
    PiTypes = PiRawMats + PiBasic + PiAdvanced2P + PiAdvanced3P + PiHighTech


    for log in logs:
        assert os.path.exists(log), 'I can\'t find the file: %s' % (log)
        obscuredPath = log.rpartition('/')
        print(('Processing Log: %s...' % obscuredPath[2]))

        logFile = open(log, 'r')
        content = logFile.readlines() + ['\r\n']
        logFile.close()

        for lineNum in range(len(content)):
            # Process each line that was in the log file.
            line = content[lineNum].rstrip('\r\n')

            clean = line.strip()   # Removes newline characters
            if len(clean) > 0:
                data = clean.split('\t')   # Drops empty lines and outputs tuple
                # Output: [0] Time, [1] Station, [2] Hanger, [3] Character, [4] Action, [5] Outcome, [6] ItemType, [7] Quantity

                if data[0] != 'Time':   # Skip first line of log
                    if data[3] not in pilots:
                        pilots.append(data[3])
                    if data[4] == 'Lock':
                        # Split ore from other items
                        if data[6] in OreTypes:
                            if data[3] not in orePilots:
                                orePilots.append(data[3])
                            volume = (OreWeights[(OreTypes[(data[6])])] * int(data[7]))
                            itemGroup = OreTypes[(data[6])]
                            oreGroups.append([data[3], data[6], data[7], itemGroup, volume])
                        # Split ice from other items
                        elif data[6] in IceTypes:
                            if data[3] not in icePilots:
                                icePilots.append(data[3])
                            volume = (IceTypes[(data[6])] * int(data[7]))
                            ice.append([data[3], data[6], data[7], volume])
                        elif data[6] in MineralTypes:
                            minerals.append([data[3], data[6], data[7], 0])
                        elif data[6] in SalvageTypes:
                            salvage.append([data[3], data[6], data[7], 0])
                        elif data[6] in PiTypes:
                            commodities.append([data[3], data[6], data[7], 0])
                        # Every thing else
                        else:
                            other.append([data[3], data[6], data[7], 0])
                        

    if args.compact is True:
        print('Compact Mode')
        oreGroups = sorted(oreGroups, key=itemgetter(0,3))
        for item in range(len(oreGroups)):
            if item > 0:
                previous = item -1
                if (oreGroups[item][0] == oreGroups[previous][0]) and (oreGroups[item][3] == oreGroups[previous][3]):
                    newQuantity = (int(oreGroups[item][2]) + int(oreGroups[previous][2]))
                    newVolume = (OreWeights[oreGroups[item][3]] * int(newQuantity))
                    oreGroups[item] = [oreGroups[item][0], oreGroups[item][3], newQuantity, oreGroups[item][3], newVolume]
                    oreGroups[previous] = 'deleted'
        
        for o in oreGroups[:]:
            if o == 'deleted':
                oreGroups.remove(o)
    else:
        oreGroups = sorted(oreGroups, key=itemgetter(0,1))
        for item in range(len(oreGroups)):
            if item > 0:
                previous = item -1
                if (oreGroups[item][0] == oreGroups[previous][0]) and (oreGroups[item][1] == oreGroups[previous][1]):
                    newQuantity = (int(oreGroups[item][2]) + int(oreGroups[previous][2]))
                    newVolume = (OreWeights[oreGroups[item][3]] * int(newQuantity))
                    oreGroups[item] = [oreGroups[item][0], oreGroups[item][1], newQuantity, oreGroups[item][3], newVolume]
                    oreGroups[previous] = 'deleted'
        
        for o in oreGroups[:]:
            if o == 'deleted':
                oreGroups.remove(o)
       

    salvage = sorted(salvage, key=itemgetter(0,1))
    for item in range(len(salvage)):
        if item > 0:
            previous = item -1
            if (salvage[item][0] == salvage[previous][0]) and (salvage[item][1] == salvage[previous][1]):
                newQuantity = (int(salvage[item][2]) + int(salvage[previous][2]))
                salvage[item] = [salvage[item][0], salvage[item][1], newQuantity, 0]
                salvage[previous] = 'deleted'
                
    for s in salvage[:]:
        if s == 'deleted':
            salvage.remove(s)


    minerals = sorted(minerals, key=itemgetter(0,1))
    for item in range(len(minerals)):
        if item > 0:
            previous = item -1
            if (minerals[item][0] == minerals[previous][0]) and (minerals[item][1] == minerals[previous][1]):
                newQuantity = (int(minerals[item][2]) + int(minerals[previous][2]))
                minerals[item] = [minerals[item][0], minerals[item][1], newQuantity, 0]
                minerals[previous] = 'deleted'
                
    for m in minerals[:]:
        if m == 'deleted':
            minerals.remove(m)


    commodities = sorted(commodities, key=itemgetter(0,1))
    for item in range(len(commodities)):
        if item > 0:
            previous = item -1
            if (commodities[item][0] == commodities[previous][0]) and (commodities[item][1] == commodities[previous][1]):
                newQuantity = (int(commodities[item][2]) + int(commodities[previous][2]))
                commodities[item] = [commodities[item][0], commodities[item][1], newQuantity, 0]
                commodities[previous] = 'deleted'
                
    for c in commodities[:]:
        if c == 'deleted':
            commodities.remove(c)


    other = sorted(other, key=itemgetter(0,1))
    for item in range(len(other)):
        if item > 0:
            previous = item -1
            if (other[item][0] == other[previous][0]) and (other[item][1] == other[previous][1]):
                newQuantity = (int(other[item][2]) + int(other[previous][2]))
                other[item] = [other[item][0], other[item][1], newQuantity, 0]
                other[previous] = 'deleted'

    for e in other[:]:
        if e == 'deleted':
            other.remove(e)
    
    
    if ice or oreGroups or salvage or minerals or other:
        if ice:
            totalIce = 0
            for entry in ice:
                totalIce = entry[3] + totalIce

            print('\nIce:')
            for name in sorted(icePilots):
                pilotIce = 0
                print(('\n%s' % name))
                for entry in sorted(ice, key=itemgetter(0,3)):
                    if name == entry[0]:
                        print(('%s x  %s = %sm3' % (entry[2], entry[1], entry[3])))
                        pilotIce = entry[3] + pilotIce
                iceTotals.append([name,pilotIce,((float(pilotIce) / float(totalIce)) * 100)])
    
            iceTotals = sorted(iceTotals, key=itemgetter(2), reverse=True)
            print(('\nPercentage of Ice: (%sm3)\n' % (totalIce)))
            for entry in range(len(iceTotals)):
                if iceTotals[(entry)][1] > 0:
                    print(('%.2f%% %s: %s m3' % ((iceTotals[(entry)][2]), iceTotals[(entry)][0], iceTotals[(entry)][1])))
            print('\n')


        if oreGroups:
            totalOre = 0
            for entry in oreGroups:
                totalOre = entry[4] + totalOre

            print('\nOre:')
            for name in sorted(orePilots):
                pilotOre = 0
                print(('\n%s' % name))
                for entry in sorted(oreGroups, key=itemgetter(0,3)):
                    if name == entry[0]:
                        if args.compact is True:
                            print(('%s x  %s = %.2fm3' % (entry[2], entry[3], entry[4])))
                        else:
                            print(('%s x  %s = %.2fm3' % (entry[2], entry[1], entry[4])))
                        pilotOre = entry[4] + pilotOre
                oreTotals.append([name,pilotOre,((pilotOre / totalOre) * 100)])
    
            oreTotals = sorted(oreTotals, key=itemgetter(2), reverse=True)
            print(('\nPercentage of Ore: (%.2fm3)\n' % (totalOre)))
            for entry in range(len(oreTotals)):
                if oreTotals[(entry)][1] > 0:
                    print(('%.2f%% %s: %.2f m3' % ((oreTotals[(entry)][2]), oreTotals[(entry)][0], oreTotals[(entry)][1])))
            print('\n')


        if salvage:
            print('\nSalvaged Components:')
            pilot = ''
            for entry in sorted(salvage, key=itemgetter(0)):
                if pilot != entry[0]:
                    pilot = entry[0]
                    print(('\n%s' % pilot))
                print(('%s x %s' % (entry[2], entry[1])))
            print('\n')


        if minerals:
            print('\nMinerals:')
            pilot = ''
            for entry in sorted(minerals, key=itemgetter(0)):
                if pilot != entry[0]:
                    pilot = entry[0]
                    print(('\n%s' % pilot))
                print(('%s x %s' % (entry[2], entry[1])))
            print('\n')


        if commodities:
            print('\nPI Items:')
            pilot = ''
            for entry in sorted(commodities, key=itemgetter(0)):
                if pilot != entry[0]:
                    pilot = entry[0]
                    print(('\n%s' % pilot))
                print(('%s x %s' % (entry[2], entry[1])))
            print('\n')


        if other:
            print('\nRecovered Items:')
            pilot = ''
            for entry in sorted(other, key=itemgetter(0)):
                if pilot != entry[0]:
                    pilot = entry[0]
                    print(('\n%s' % pilot))
                print(('%s x %s' % (entry[2], entry[1])))
            print('\n')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
