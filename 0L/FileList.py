import os
import ROOT

if os.path.isfile("FileList.txt"):
    os.system("rm FileList.txt")
File = open("FileList.txt", "w")

for MCdir in os.listdir("/afs/cern.ch/work/p/pmoder/private/0L_snapshot/0L_tar_Min/eos/home-b/bbrueers/tW0LBoosted/ntuple/Rall/"):
    if MCdir == "MC16d" or MCdir == "MC16e" or MCdir == "MC16a":
        File.write("#" + MCdir + "\n")
        for directory in os.listdir("/afs/cern.ch/work/p/pmoder/private/0L_snapshot/0L_tar_Min/eos/home-b/bbrueers/tW0LBoosted/ntuple/Rall/" + MCdir + "/"):
            if "signal" in directory or "Fake" in directory:
	        continue
            File.write("#" + str(directory) + "\n")
            for files in os.listdir("/afs/cern.ch/work/p/pmoder/private/0L_snapshot/0L_tar_Min/eos/home-b/bbrueers/tW0LBoosted/ntuple/Rall/" + MCdir  + "/" + str(directory) + "/"):
	        RootFile = ROOT.TFile.Open("/afs/cern.ch/work/p/pmoder/private/0L_snapshot/0L_tar_Min/eos/home-b/bbrueers/tW0LBoosted/ntuple/Rall/" + MCdir + "/" + str(directory) + "/" + str(files))
	        Tree = RootFile.Get("nominal")
	        if Tree == None:
		    print(MCdir + "_" + files)
		    continue
	        else:
		    File.write("/afs/cern.ch/work/p/pmoder/private/0L_snapshot/0L_tar_Min/eos/home-b/bbrueers/tW0LBoosted/ntuple/Rall/" + MCdir + "/" + str(directory) + "/" + str(files) + "\n")
    File.write("\n")

File.close()
