import sys
import ROOT as r

from optparse import OptionParser
from argparse import ArgumentParser

# path = "/u/ea/pbutti/public_html/alignment_monitoring_files/"

colors = [r.kBlue+2, r.kCyan+2, r.kRed+2, r.kOrange+10, r.kYellow+2, r.kGreen-1, r.kAzure-2, r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3]
markers = [r.kFullCircle, r.kFullTriangleUp, r.kFullSquare, r.kOpenSquare, r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle, r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle, r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle, r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle, r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle, r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp]

binLabels = ["", "L1tA", "L1tS", "L2tA", "L2tS", "L3tA", "L3tS", "L4tA", "L4tS", "L5tAh", "L5tSh", "L5tAs", "L5tSs", "L6tAh", "L6tSh", "L6tAs", "L6tSs", "L7tAh", "L7tSh", "L7tAs", "L7tSs"]
binLabels += ["", "", "", "", ""]
binLabels += ["L1bA", "L1bS", "L2bA", "L2bS", "L3bA", "L3bS", "L4bA", "L4bS", "L5bAh", "L5bSh", "L5bAs", "L5bSs", "L6bAh", "L6bSh", "L6bAs", "L6bSs", "L7bAh", "L7bSh", "L7bAs", "L7bSs"]
binLabels += ["", "", "", "", "", ""]
binLabels += ["", "", "", "", "", ""]

parser = ArgumentParser()
parser.add_argument('-i', '--inputFiles', dest='inputFiles', help='input files', nargs='*')
parser.add_argument("-o", "--outdir", dest="outdir", help="output directory", default="AlignmentResults")
parser.add_argument("-t", "--html", dest="doHTML", help="create html page", action='store_true')
parser.add_argument("-l", "--legend", dest="legend", help="names displayed in legend", nargs='*')
parser.add_argument("-e", "--oFext", dest="oFext", help="extension of output files; default .png", default=".png")
# parser.add_argument('baz', nargs='*')

# parser = OptionParser()
# parser.add_option("-i", "--indir", dest="indir", help="inputdir", metavar="indir", default="nominal_10031")
# parser.add_option("-f", "--inputFile", dest="inputFile", help="inputFile", metavar="inputFile", default="")
# parser.add_option("-o", "--outdir", dest="outdir", help="outdir", metavar="outdir", default="")
# parser.add_option("-t", "--html", dest="doHTML", help="doHTML", metavar="doHTML", default=False)
# (config, sys.argv[1:]) = parser.parse_args()
args = parser.parse_args()
legend = []
if not len(args.legend) == len(args.inputFiles):
    print("SETUP::Generating legend names from input names.")
    for file in args.inputFiles:
        pos1 = file.find('HPS')
        pos2 = file.find('iter') + 5

        if pos1==-1 or pos2==-1:
            raise Exception("Detector naming pattern deviates from default; the legend names have to be entered manually")

        legName = file[pos1:pos2]
        legend.append(legName)
else:
    legend = args.legend
        

# legName = (args.inputFile.split("/")[-1]).strip("_gblmon.root")
# if ("_AlignmentMonitoring" in legName):
#     legName = (legName).replace("_AlignmentMonitoring", "")
# if ("_MPIIdata" in legName):
#     legName = legName.replace("_MPIIdata", "")
# if ("_projections" in legName):
#     legName = legName.replace("_projections", "")

# refName = (args.indir)
# if ("/" in refName):
#     refName = (refName.strip("/")).split("/")[-1]
# legends = [refName, legName]
# outdir = args.outdir
# inputFiles = []
