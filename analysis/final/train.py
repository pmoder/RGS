#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  File:        train.py
#  Description: HO2 optimization example
#  Created:     10-Jan-2015 Harrison B. Prosper and Sezen Sekmen
#  Updated:     17-Jun-2017 HBP get ready for release
# -----------------------------------------------------------------------------
import os, sys, re
from rgsutil import *
from string import *
from ROOT import *
import ROOT
import multiprocessing as mp
from functools import partial
# -----------------------------------------------------------------------------
# read scale factors
# execfile('scales.py')

def addFiles(FileList, MCTagList, tagList, numberList, rgs, start, numrows, tagNumberList, counter):
    tagFile = open(tagNumberList, "a")
    tagFile.write(MCTagList[counter] + "_" + tagList[counter] + str(numberList[counter]) + "\n")
    tagFile.close()
    return rgs.add(FileList[counter], start, numrows, "_" + MCTagList[counter] + "_" + tagList[counter] + str(numberList[counter]))

def main():
    NAME = "Test"
    print "="*80
    print "\t=== %s ===" % NAME
    print "="*80

    
    # Load the RGS shared library and check that the various input files
    # exist.
    # ---------------------------------------------------------------------
    gSystem.AddDynamicPath('$RGS_PATH/lib')
    if gSystem.Load("libRGS") < 0: error("unable to load libRGS")

    # Name of file containing cut definitions
    # Format of file:
    #   variable-name  cut-type (>, <, <>, |>, |<, ==)
    varfilename = "%s.cuts" % NAME
    if not os.path.exists(varfilename):
        error("unable to open variables file %s" % varfilename)

    # Files to be processed
    filename1 = "a100_DM10_H500_tb1/a100_DM10_H500_tb1.root"
    if not os.path.exists(filename1):
        error("unable to open file %s" % filename1)

    # ---------------------------------------------------------------------
    #  Create RGS object
    #  
    #   The file (cutdatafilename) of cut-points is usually a signal file,
    #   which ideally differs from the signal file on which the RGS
    #   algorithm is run.
    # ---------------------------------------------------------------------
    cutdatafilename = filename1
    start      = 0           # start row 
    maxcuts    = 100000       # maximum number of cut-points to consider
    treename   = "nominal"   # name of Root tree
    weightname = "KiSelectorWeightsSelectionpreSelection"
    selection  = "(n_lep_signal == 1) && (n_lep == 1) && (Trigger_SingleLep == 1) && (lep1_pt > 25000) && (n_jet >= 3) && (n_bjet >= 1) && (jet1_pt > 50000) && (jet2_pt > 50000) && (jet3_pt > 20000) && (bjet1_pt > 50000) && (met > 200000) && (mt > 100000) && (mb1l > 160000) && (dPhimin_4 > 0.4) && (PassTruthMetFilter == 1) "
    rgs = RGS(cutdatafilename, start, maxcuts, treename,
                  weightname, selection)

    # ---------------------------------------------------------------------
    #  Add signal and background data to RGS object.
    #  Weight each event using the value in the field weightname, if
    #  present.
    #  NB: We asssume all files are of the same format.
    # ---------------------------------------------------------------------
    # 1) The first optional argument is a string, which, if given, will be
    # appended to the "count" and "fraction" variables. The "count" variable
    # contains the number of events that pass per cut-point, while "fraction"
    # is count / total, where total is the total number of events per file.
    # If no string is given, the default is to append an integer to the
    # "count" and "fraction" variables, starting at 0, in the order in which
    # the files are added to the RGS object.
    # 2) The second optional argument is the weight to be assigned per file. If
    # omitted the default weight is 1.
    # 3) The third optional argument is the selection string. If omitted, the
    # selection provided in the constructor is used.
    
    start    = 0   #  start row
    numrows  =-1   #  scan all the data from the files

#    scale = 139000./58500.
    scale = 1.0

    rgs.add(filename1, start, numrows, "_signal", scale)
    with open("FileList.txt") as f:
        samples = f.readlines()
    samples = [x.strip() for x in samples]
    tagNumberList = open("tagNumber.txt", "w")
    for line in samples:
	if line == "":
	    continue
	elif line.startswith("#"):
	    if "MC" in line:
		MCtag = line[1:]
	    else:
		tag = line[1:]
		tagNumber = 1
	else:
	    tagNumberList.write(MCtag + "_" + tag + str(tagNumber) + "\n")
	    rgs.add(line, start, numrows, "_" + MCtag + "_" + tag + str(tagNumber), scale)
	    tagNumber += 1
    tagNumberList.close()

    # ---------------------------------------------------------------------	
    #  Run RGS and write out results
    # ---------------------------------------------------------------------	    
    rgs.run(varfilename)

    # Write to a root file
    rgsfilename = "%s.root" % NAME
    rgs.save(rgsfilename)
# -----------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\tciao!\n"
