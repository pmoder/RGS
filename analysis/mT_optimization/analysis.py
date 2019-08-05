#!/usr/bin/env python
# ---------------------------------------------------------------------
#  File:        analysis.py
#  Description: HO2: Analyze the results of RGS and find the best cuts.
#               Definitions:
#                 1. A one-sided cut is a threshold on a single
#                    variable.
#                    e.g., x > xcut
#                 2. A cut-point is the AND of a sequence of cuts. This
#                    can be visualized as a point in the space of cuts.
#                 3. A two-sided cut is a two-sided threshold.
#                    e.g., (x > xlow) and (x < xhigh)
#                 4. A staircase cut is the OR of cut-pooints.
# ---------------------------------------------------------------------
#  Created:     10-Jan-2015 Harrison B. Prosper and Sezen Sekmen
# ---------------------------------------------------------------------
import os, sys, re
from string import *
from rgsutil import *
from time import sleep
from ROOT import *
from math import *

sys.path.append('../../python')
from rgsanalysis import *
# --------------------------------------------------------------------
def cut(event):
    return (event.n_lep_signal != 1) or (event.n_lep != 1) or (event.Trigger_SingleLep != 1) or (event.lep1_pt < 25000) or (event.n_jet < 3) or (event.n_bjet < 1) or (event.jet1_pt < 50000) or (event.jet2_pt < 50000) (event.jet3_pt < 20000) or (event.bjet1_pt < 50000) or (event.met < 150000) or (event.mt < 120000) or (event.mt > 1000000) or (event.mb1l < 160000)
# ---------------------------------------------------------------------
def main():
    NAME = 'Test'
    print "="*80
    print "\t=== %s ===" % NAME
    print "="*80

    resultsfilename = "%s.root" % NAME
    treename = "RGS"
    print "\n\topen RGS file: %s"  % resultsfilename
    ntuple = Ntuple(resultsfilename, treename)
    
    variables = ntuple.variables()
    for name, count in variables:
        print "\t\t%-30s\t%5d" % (name, count)
    print "\tnumber of cut-points: ", ntuple.size()

    # -------------------------------------------------------------
    # Plot results of RGS, that is, the fraction of events that
    # pass a given cut-point.
    #  1. Loop over cut points and compute a significance measure
    #     for each cut-point.
    #  2. Find cut-point with highest significance.
    # -------------------------------------------------------------
    # Set up a standard Root graphics style (see histutil.py in the
    # python directory).
    setStyle()

#    print "Plotting histograms..."
#    cmass, hs, hb = fillmt(cut)

    # Create a 2-D histogram for ROC plot
    msize = 0.30  # marker size for points in ROC plot
    
    xbins =  100  # number of bins in x (background)
    xmin  =  0.0  # lower bound of x
    xmax  =  1.0  # upper bound of y

    ybins = 100
    ymin  = 0.0
    ymax  = 1.0

    color = kBlue+1
    hist  = mkhist2("hroc",
                    "#font[12]{#epsilon_{B}}",
                    "#font[12]{#epsilon_{S}}",
                    xbins, xmin, xmax,
                    ybins, ymin, ymax,
                    color=color)
    hist.SetMinimum(0)
    hist.SetMarkerSize(msize)

    # loop over all cut-points, compute a significance measure Z
    # for each cut-point, and find the cut-point with the highest
    # significance and the associated cuts.
    print "\tfilling ROC plot..."	
    bestZ = -1      # best Z value
    bestrow = -1    # row with best cut-point

    totals = ntuple.totals()

    t_signal, et1 = totals[0]
#    t_background, et2 = totals[1]
#    t_ZZ,  et3 = totals[2]

    ts = t_signal
    tb = 0
    tbError2 = 0
    for i in xrange(len(totals)-1):
	t_background, et2 = totals[i+1]
        tb += t_background
    for row, cuts in enumerate(ntuple):
        c_signal = cuts.count_signal
	c_background = 0
        c_count = 0
	c_fract = 0
	with open("tagNumber.txt") as f:
            tagNumber = f.readlines()
	tagNumber = [x.strip() for x in tagNumber]
        nr = 0
        tbError = 0.0
	for line in tagNumber:
            string = "c_count = cuts.count_" + line
            exec(string)
            string2 = "c_fract = cuts.fraction_" + line
            exec(string2)
            c_background += c_count
            string3 = "c_sqrdWeight = cuts.sqrdWeight_" + line
	    exec(string3)
	    tbError += c_sqrdWeight
        s  = c_signal
        b  = c_background

        if b < 0:
            continue
        
        fs = s / ts
        fb = b / tb
                
        #  Plot fs vs fb
        hist.Fill(fb, fs)

#	sigma = sqrt(tbError)
#	sigma = sqrt(tbError + (0.2*b)**2)
#	sigma = 0.0
	sigma = 0.2*b
        	
        # Compute measure of significance
        #   Z  = sign(LR) * sqrt(2*|LR|)
        # where LR = log(Poisson(s+b|s+b)/Poisson(s+b|b))
        Z = signalSignificance(s, b, sigma)
#	if s == 0:
#	    Z = 0.0
#	if (sqrt(tbError)/b + 0.2 > 0.5):
#	    Z = 0.0
#	ntuple.read(row)
#	if ntuple("mb1j1") < 160000: Z = -20.0
	if Z > bestZ:
	    bestZ = Z
	    bestrow = row
	    bestsigma = sigma
	    signal_sqrdWeight = cuts.sqrdWeight_signal

    # -------------------------------------------------------------            
    # Write out best cut
    # -------------------------------------------------------------
    bestcuts = writeHZZResults('r_%s.txt' % NAME,
                                   '%s.cuts' % NAME,
                                ntuple, variables,
                                bestrow, bestZ, bestsigma, signal_sqrdWeight,
                                totals)

    # -------------------------------------------------------------
    # Save plots
    # -------------------------------------------------------------
    print "\t== plot ROC ==="	
    croc = TCanvas("fig_%s_ROC" % NAME,
                   "ROC", 520, 10, 500, 500)
    croc.cd()
    hist.Draw()
    croc.Update()
    gSystem.ProcessEvents()    
    croc.Print("h_%s_ROC.pdf" % NAME)    

#    print "\t=== two-sided cuts ==="
    
#    xbins= hs.GetNbinsX()
#    xmin = hs.GetXaxis().GetBinLowEdge(1)
#    xmax = hs.GetXaxis().GetBinUpEdge(xbins)

#    ybins = hs.GetNbinsY()
#    ymin  = hs.GetYaxis().GetBinLowEdge(1)
#    ymax  = hs.GetYaxis().GetBinUpEdge(ybins)

#    print (bestcuts)
#    hcut = TH2Poly('hcut', '', xmin, xmax, ymin, ymax)
#    hcut.AddBin(bestcuts['mt'], bestcuts['mt'], bestcuts['mt'], bestcuts['mt'])
#    hcut.SetLineWidth(2)
    
#    cmass.cd()
#    hs.Draw('box')
#    hb.Draw('boxsame')
#    hcut.Draw('same')
#    drawHZZLegend()    
#    cmass.Update()
#    gSystem.ProcessEvents()
#    cmass.Print("h_%s.pdf" % NAME)    
    
    sleep(5)
# ---------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "bye!"


