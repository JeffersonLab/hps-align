import ROOT as r
from argparse import ArgumentParser


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

args = parser.parse_args()
legend = []
if not len(args.legend) == len(args.inputFiles):
    print("SETUP::Generating legend names from input names.")
    for file in args.inputFiles:
        pos1 = file.find('HPS')
        pos2 = file.find('iter') + 5

        if pos1 == -1 or pos2 == -1:
            raise Exception("Detector naming pattern deviates from default; the legend names have to be entered manually")

        legName = file[pos1:pos2]
        legend.append(legName)
else:
    legend = args.legend
