import os, sys, re
from array import array
from rgsutil import *
from string import *
from math import *
from ROOT import *
import ROOT
# -----------------------------------------------------------------------
# used in examples
# -----------------------------------------------------------------------

# execfile('scales.py')

def fillZ1massZ2mass(cut):
    xbins = 40
    xmin  = 150.0
    xmax  = 350.0

    ybins = 40
    ymin  = 150.0
    ymax  = 350.0    

    # Make a canvas and set its margins
    cmass = TCanvas("cmass", "cmass", 10,10, 425, 400)
    cmass.SetBottomMargin(0.15)
    cmass.SetLeftMargin(0.15)
    
    # -- background
    hb = mkhist2("hb",
                 "#font[12]{m}_{t} (GeV)",
                 "#font[12]{m}_{t} (GeV)",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kMagenta+1)
    hb.GetYaxis().SetTitleOffset(1.25)
   
    print("Processing Events...") 
    bntuple = Ntuple('ttbar.root', 'nominal')
    total = 0
    counter = 0
    for ii, event in enumerate(bntuple):
	counter += 1
        if cut(event): continue

        hb.Fill(event.mt, event.mt)
        if total % 1000 == 0:
            cmass.cd()
            hb.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
        if counter % 10000 == 0:
            print("Processed " + str(counter) + " events...")
        total += 1

    cmass.cd()
    hb.Draw('box')
    cmass.Update()
    gSystem.ProcessEvents()
    
    # -- signal
    hs = mkhist2("hs",
                 "#font[12]{m}_{t} (GeV)",
                 "#font[12]{m}_{t} (GeV)",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kAzure+1)
    hs.GetYaxis().SetTitleOffset(1.25)
    
    sntuple = Ntuple(['ttbar.root',
                      'a250_DM10_H800_tb1.root'], 'nominal')

    print("Processing Singal+Bkg...")
    total   = 0
    counter = 0
    for event in sntuple:
	counter += 1
        if cut(event): continue

        hs.Fill(event.mt, event.mt, event.xsec)
        if total % 1000 == 0:
            cmass.cd()
            hs.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()    
	if counter % 10000 == 0:
	    print("Processed " + str(counter) + " events...")
        total  += 1
        
    cmass.cd()
    hs.Draw('box')
    cmass.Update()
    gSystem.ProcessEvents()
    hs.Scale(1.0/hs.Integral())
    hb.Scale(1.0/hb.Integral())
    return (cmass, hs, hb)

def writeHZZResults(filename, varfilename, ntuple, variables,
                    bestrow, bestZ, bestsigma, signal_sqrdWeight, totals, outerhull=None):
    
    cutdir  = {}
    cutdirs = []
    for t in getCutDirections(varfilename):
        token = t[0]
        if token == '\\':
            continue
        else:
            cutdirs.append(t)
            cutdir[token] = t[1]
            
    ntuple.read(bestrow)
    
    out = open(filename, 'w')

    s = totals[0][0]
    print len(totals)
    b = 0
    bErr = 0
    diboson = 0
    singletop = 0
    qcd = 0
    ttV = 0
    ttbar = 0
    wjets = 0
    zjets = 0
    for i in xrange(len(totals)-1):
        b += totals[i+1][0]
        bErr += totals[i+1][1]**2
	if (0 <= i and i <= 4) or (64 <= i and i <= 68) or (130 <= i and i <= 134):
	    diboson += totals[i+1][0]
	if (i <= 5 and i <= 13) or (69 <= i and i <= 77):
	    qcd += totals[i+1][0]
	elif (14 <= i and i <= 19) or (78 <= i and i <= 83) or (135 <= i and i <= 140):
	    singletop += totals[i+1][0]
	elif (20 <= i and i <= 21) or (84 <= i and i <= 85) or (141 <= i and i <= 142):
	    ttV += totals[i+1][0]
	elif (22 <= i and i <= 26) or (86 <= i and i <= 90) or (143 <= i and i <= 147):
	    ttbar += totals[i+1][0]
	elif (27 <= i and i <= 49) or (91 <= i and i <= 114) or (148 <= i and i <= 189):
	    wjets += totals[i+1][0]
	elif (50 <= i and i <= 63) or (115 <= i and i <= 129) or (190 <= i and i <= 229):
	    zjets += totals[i+1][0]
    bErr = sqrt(bErr)

    print("diboson  : " + str(diboson))
    print("qcd:     : " + str(qcd))
    print("singletop: " + str(singletop))
    print("ttV      : " + str(ttV))
    print("ttbar    : " + str(ttbar))
    print("wjets    : " + str(wjets))
    print("zjets    : " + str(zjets))
    record = "Yields before optimization"
    out.write('%s\n' % record); print record

    record = "\tsignal:    %10.3f +/- %-10.1f" % (totals[0][0],
                                                   totals[0][1])
    out.write('%s\n' % record); print record

    record = "\tbackground:     %10.3f +/- %-10.1f" % (b,
                                                       bErr)

    out.write('%s\n' % record); print record

    Z = signalSignificance(s, b, 0.2*b)

    record = "\nZ values"
    out.write('%s\n' % record); print record
    
    record = "  before optimization:  %10.3f" % Z
    out.write('%s\n' % record); print record

    record = "  after optimization:   %10.3f" % bestZ
    out.write('%s\n' % record); print record    


    record = "Best cuts"
    out.write('\n%s\n' % record); print; print record

    bestcuts = {}
    
    if outerhull:
        OR = ''
        for ii, cutpoint in enumerate(outerhull):
            xname, xdir = cutdirs[0]
            yname, ydir = cutdirs[1]
            xcut = cutpoint[0]
            ycut = cutpoint[1]
            record = "\t%4s\t(%s %s %8.3f)\tAND\t(%s %s %8.3f)" % (OR,
                                                                xname,
                                                                xdir, xcut,
                                                                yname,
                                                                ydir, ycut)
            OR = 'OR'
            out.write('%s\n' % record); print record

        out.write('\n' % record); print
        
    for name, count in variables:    
        if name[0:5] in ['count', 'fract', 'cutpo', 'sqrdW']: continue
        var = ntuple(name)
        bestcuts[name] = var
        if type(var) == type(0.0):
            rec = '%3s %6.2f' % (cutdir[name], var)
            record = "\t%-10s\t%10s" % (name, rec)
            out.write('%s\n' % record); print record
        else:
            record = "\t%-10s\t%10.2f\t%10.2f" % (name,
                                                    min(var[0], var[1]),
                                                    max(var[0], var[1]))
            out.write('%s\n' % record); print record            
    print
    out.write('\n')

    record = "Yields after optimization (and relative efficiencies)"
    out.write('%s\n' % record); print record

    record = "\tsigma:    %10.3f" % bestsigma
    out.write('%s\n' % record); print record
    

    bkg = 0
    signal = 0
    test = False
    sqrd_stat = 0
    for name, count in variables:        
        if not (name[0:5] in ['count', 'fract', 'sqrdW']): continue
        var = ntuple(name)
	if name == "count_signal":
            signal = var
	    test = False
	else:
	    test = True
	if "sqrdW" in name and name != 'sqrdWeight_signal':
	    sqrd_stat += ntuple(name)
        record = "\t%-15s %10.3f" % (name, var)
        out.write('%s\n' % record); print record                    
        if name[0:5] == "fract":
            print
            out.write('\n')
        else:
	    if test and "count" in name:
		bkg += var
    record = "Signal = " + str(signal) + " +/- " + str(sqrt(signal_sqrdWeight)) + "_stat +/- " + str(0.2*signal) + "_sys"
    out.write('%s\n' % record); print record
    stat = sqrt(sqrd_stat)
    record = "Background = " + str(bkg) + " +/- " + str(stat) + "_stat +/- " + str(0.2*bkg) + "_sys"
    out.write('%s\n' % record); print record
    out.close()
    return bestcuts
# ---------------------------------------------------------------------
def drawHZZLegend(stitle="signal",
                    btitle="ttbar",
                left=True,
                      postfix=''):                       
    lgoffset1 = 0.595
    lgoffset2 = 0.583
    if left:
        lgoffset1 = 0.23
        lgoffset2 = 0.21
        
    # Title
    t = TLatex(lgoffset1, 0.85, "njets #geq 2")
    t.SetTextSize(0.045)
    t.SetTextFont(42)
    t.SetNDC()
    t.Draw("same")
    SetOwnership(t, 0)    

    # Make the histogram legend    
    hs_d = TH1D('hs_d%s' % postfix, '', 4,0,4)
    hs_d.SetMarkerStyle(20)
    hs_d.SetMarkerColor(kMagenta+1)
    hs_d.SetMarkerSize(0.8)
    SetOwnership(hs_d, 0)
    
    hb_d = TH1D('hb_d%s' % postfix, '', 4,0,4)
    hb_d.SetMarkerStyle(20)    
    hb_d.SetMarkerColor(kAzure+1)
    hb_d.SetMarkerSize(0.8)    
    SetOwnership(hb_d, 0)
    
    l = TLegend(lgoffset2, 0.67, 0.90, 0.82)
    l.SetBorderSize(0)
    l.SetFillStyle(0000)
    l.SetTextSize(0.045)
    l.SetTextFont(42)
    l.AddEntry(hs_d, stitle, 'p')
    l.AddEntry(hb_d, btitle, 'p')
    l.Draw("same")
    SetOwnership(l, 0)
# -----------------------------------------------------------------------
# SUSY
# -----------------------------------------------------------------------
def fill_MR_R2(Cut, name='SUSY'):

    xbins =   50
    xmin  =    0.0
    xmax  = 3000.0

    ybins =   50
    ymin  =    0.0
    ymax  =    0.5    
    
    cmass = TCanvas("h_%s" % name, name, 10, 10, 500, 500)    
    
    # -- background
    hb = mkhist2("hb",
                 "M_{R} (GeV)",
                 "R^{2}",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kMagenta+1)
    hb.GetYaxis().SetTitleOffset(1.80)
    
    bntuple = Ntuple('../../data/ttbar.root', 'RGSinput')
    count = 0
    for event in bntuple:
        if Cut(event): continue
            
        hb.Fill(event.MR, event.R2, event.weight)
        if count % 1000 == 0:
            cmass.cd()
            hb.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
        count += 1
        if count >= 10000: break
            
    # -- signal
    hs = mkhist2("hs",
                 "M_{R} (GeV)",
                 "R^{2}",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kAzure+1)
    hs.GetYaxis().SetTitleOffset(1.80)
    
    sntuple = Ntuple('../../data/SUSY_gluino_m1354.root', 'RGSinput')
    count = 0
    for event in sntuple:
        if Cut(event): continue
            
        hs.Fill(event.MR, event.R2, event.weight)
        if count % 1000 == 0:
            cmass.cd()
            hs.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
        count += 1
        if count >= 10000: break
            
    cmass.cd(2)
    hs.Draw('box')
    hb.Draw('box same')
    cmass.Update()
    gSystem.ProcessEvents()    
    return (cmass, hs, hb)

def writeSUSYResults(filename, varfilename, ntuple, variables,
                     bestrow, bestZ, outerhull):
    
    cutdir  = {}
    cutdirs = []
    for t in getCutDirections(varfilename):
        token = t[0]
        if token[0] == '\\':
            continue
        else:
            cutdirs.append(t)
            cutdir[token] = t[1]

    totals = ntuple.totals()
    ntuple.read(bestrow)
    
    out = open(filename, 'w')

    print 
    record = "Yields before optimization"
    out.write('%s\n' % record); print record
    
    record = "\tttbar:   %12.1f +/- %-10.1f" % (totals[0][0],
                                                   totals[0][1])
    out.write('%s\n' % record); print record

    record = "\tSUSY:    %12.1f +/- %-10.1f" % (totals[1][0],
                                                   totals[1][1])
    out.write('%s\n' % record); print record    

    b = totals[0][0]
    s = totals[1][0]
    Z = signalSignificance(s, b)

    record = "\nZ values"
    out.write('%s\n' % record); print record
    
    record = "  before optimization:  %10.3f" % Z
    out.write('%s\n' % record); print record

    record = "  after optimization:   %10.3f" % bestZ
    out.write('%s\n' % record); print record    

    record = "Best cuts"
    out.write('\n%s\n' % record); print; print record

    bestcuts = {}
    
    OR = ''
    for ii, cutpoint in enumerate(outerhull):
        xname, xdir = cutdirs[0]
        yname, ydir = cutdirs[1]
        xcut = cutpoint[0]
        ycut = cutpoint[1]
        record = "\t%4s\t(%s %s %8.3f)\tAND\t(%s %s %8.3f)" % (OR,
                                                            xname,
                                                            xdir, xcut,
                                                            yname,
                                                            ydir, ycut)
        OR = 'OR'
        out.write('%s\n' % record); print record

    out.write('%s\n' % record); print

    for name, cdir in cutdirs[2:]:    
        var = ntuple(name)
        bestcuts[name] = var
        #print name, var
        if type(var) == type(0.0):
            rec = '%3s %6.2f' % (cutdir[name], var)
            record = "\t%-10s\t%10s" % (name, rec)
            out.write('%s\n' % record); print record
        else:
            record = "\t%-10s\t%10.2f\t%10.2f" % (name,
                                                    min(var[0], var[1]),
                                                    max(var[0], var[1]))
            out.write('%s\n' % record); print record            
    print
    out.write('\n')

    record = "Yields after optimization (and relative efficiencies)"
    out.write('%s\n' % record); print record

    for name, count in variables:        
        if not (name[0:5] in ['count', 'fract']): continue
        var = ntuple(name)
        record = "\t%-15s %10.3f" % (name, var)
        out.write('%s\n' % record); print record                    
        if name[0:5] == "fract":
            print
            out.write('\n')
    out.close()
    return bestcuts
# ---------------------------------------------------------------------
def drawSUSYLegend(lgtitle='',
                   stitle="pp #rightarrow #tilde{g}#tilde{g}",
                   btitle="pp #rightarrow t#bar{t}",
                   left=True,
                      postfix=''):                       
    lgoffset1 = 0.595
    lgoffset2 = 0.583
    if left:
        lgoffset1 = 0.23
        lgoffset2 = 0.21
        
    # Title
    t = TLatex(lgoffset1, 0.85, lgtitle)
    t.SetTextSize(0.045)
    t.SetTextFont(42)
    t.SetNDC()
    t.Draw("same")
    SetOwnership(t, 0)    

    # Make the histogram legend    
    hs_d = TH1D('hs_d%s' % postfix, '', 4,0,4)
    hs_d.SetMarkerStyle(20)
    hs_d.SetMarkerColor(kMagenta+1)
    hs_d.SetMarkerSize(0.8)
    SetOwnership(hs_d, 0)
    
    hb_d = TH1D('hb_d%s' % postfix, '', 4,0,4)
    hb_d.SetMarkerStyle(20)    
    hb_d.SetMarkerColor(kAzure+1)
    hb_d.SetMarkerSize(0.8)    
    SetOwnership(hb_d, 0)
    
    l = TLegend(lgoffset2, 0.67, 0.90, 0.82)
    l.SetBorderSize(0)
    l.SetFillStyle(0000)
    l.SetTextSize(0.045)
    l.SetTextFont(42)
    l.AddEntry(hs_d, stitle, 'p')
    l.AddEntry(hb_d, btitle, 'p')
    l.Draw("same")
    SetOwnership(l, 0)

# ---------------------------------------------------------------------

def fillmt(cut):
    xbins = 91
    xmin  = 90000.0
    xmax  = 1000000.0

    # Make a canvas and set its margins
    cmass = TCanvas("cmass", "cmass", 10,10, 425, 400)
    cmass.SetBottomMargin(0.15)
    cmass.SetLeftMargin(0.15)

    # -- background
    FileList = []
    with open("FileList.txt") as f:
        samples = f.readlines()
    samples = [x.strip() for x in samples]
    for line in samples:
        if line == "" or line.startswith("#"):
            continue
        else:
            FileList.append(line)

    hb = mkhist1("hb",
                 "#font[12]{m}_{t} (GeV)",
                 "entries",
                 xbins, xmin, xmax,
                 color=kMagenta+1)
    hb.GetYaxis().SetTitleOffset(1.25)

    print("Processing Events...")
    
    bntuple = Ntuple(FileList, 'nominal')
    total = 0
    counter = 0
    for ii, event in enumerate(bntuple):
        counter += 1
        if cut(event): continue

#        weight = event.WeightEvents * event.WeightEventsSherpa * event.WeightPileUp * event.bTagSF * event.jvfSF * event.WeightSF_mu * event.WeightSF_e * event.WeightTrigger_SingleLep * event.xsec * 139000 * scale
        hb.Fill(event.mt)
        if total % 1000 == 0:
            cmass.cd()
            hb.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
        if counter % 10000 == 0:
            print("Processed " + str(counter) + " events...")
        total += 1

    cmass.cd()
    hb.Draw('box')
    cmass.Update()
    gSystem.ProcessEvents()

     # -- signal
    hs = mkhist1("hs",
                 "#font[12]{m}_{t} (MeV)",
                 "entries",
                 xbins, xmin, xmax,
                 color=kAzure+1)
    hs.GetYaxis().SetTitleOffset(1.25)

    print("Processing Signal...")
    SignalList = ['a250_DM10_H800_tb1.root']
    sntuple = Ntuple(SignalList, 'nominal')
    total   = 0
    counter = 0
    for event in sntuple:
        counter += 1
        if cut(event): continue

#        weight = event.WeightEvents * event.WeightEventsSherpa * event.WeightPileUp * event.bTagSF * event.jvfSF * event.WeightSF_mu * event.WeightSF_e * event.WeightTrigger_SingleLep * event.xsec * 139000 * signal_scale
        hs.Fill(event.mt)
        if total % 1000 == 0:
            cmass.cd()
            hs.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
        if counter % 10000 == 0:
            print("Processed " + str(counter) + " events...")
        total  += 1

    cmass.cd()
    hs.Draw('box')
    cmass.Update()
    gSystem.ProcessEvents()
    hs.Scale(1.0/hs.Integral())
    hb.Scale(1.0/hb.Integral())
    return (cmass, hs, hb)
