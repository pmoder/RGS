import os
import ROOT

if os.path.isfile("FileList.txt"):
    os.system("rm FileList.txt")
File = open("FileList.txt", "w")

for MCdir in os.listdir("/eos/user/p/pmoder/snapshot/preSelection/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/WtMet/Easter/"):
    if MCdir == "MC16d" or MCdir == "MC16e" or MCdir == "MC16a":
        File.write("#" + MCdir + "\n")
        for directory in os.listdir("/eos/user/p/pmoder/snapshot/preSelection/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/WtMet/Easter/" + MCdir + "/"):
            if "signal" in directory or "Fake" in directory:
	        continue
            File.write("#" + str(directory) + "\n")
            for files in os.listdir("/eos/user/p/pmoder/snapshot/preSelection/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/WtMet/Easter/" + MCdir  + "/" + str(directory) + "/"):
	        RootFile = ROOT.TFile.Open("/eos/user/p/pmoder/snapshot/preSelection/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/WtMet/Easter/" + MCdir + "/" + str(directory) + "/" + str(files))
	        Tree = RootFile.Get("nominal")
	        if Tree == None:
		    print(MCdir + "_" + files)
		    continue
	        else:
		    File.write("/eos/user/p/pmoder/snapshot/preSelection/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/WtMet/Easter/" + MCdir + "/" + str(directory) + "/" + str(files) + "\n")
    File.write("\n")

File.close()
