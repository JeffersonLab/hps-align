import json
import os
import ROOT as r
from argparse import ArgumentParser


class BasePlotter:
    """! Base class for plotting alignment results

    This class contains the basic functionality and setup for plotting alignment results.
    It is intended to be inherited by other classes that implement specific plotting.

    The class is initialized with the following arguments:
    - input_file_list: list of file names containing the alignment results
    - outdir: directory where the plots will be saved
    - legend_names: list of names for the legend entries
    - do_html: if True, an index page with links to the plots will be created
    - oFext: extension of the output files
    """

    def __init__(self):
        ## ROOT plot colors
        self.colors = [r.kBlue+2, r.kCyan+2, r.kRed+2, r.kOrange+10,
                       r.kYellow+2, r.kGreen-1, r.kAzure-2, r.kGreen-8,
                       r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2,
                       r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2,
                       r.kBlue+2, r.kGreen-8, r.kOrange+3, r.kYellow+2,
                       r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3,
                       r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8,
                       r.kOrange+3]
        ## ROOT markers
        self.markers = [r.kFullCircle, r.kFullTriangleUp, r.kFullSquare,
                        r.kOpenSquare, r.kOpenTriangleUp, r.kOpenCircle,
                        r.kFullCircle, r.kOpenSquare, r.kFullSquare,
                        r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle,
                        r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp,
                        r.kOpenCircle, r.kFullCircle, r.kOpenSquare,
                        r.kFullSquare, r.kOpenTriangleUp, r.kOpenCircle,
                        r.kFullCircle, r.kOpenSquare, r.kFullSquare,
                        r.kOpenTriangleUp, r.kOpenCircle, r.kFullCircle,
                        r.kOpenSquare, r.kFullSquare, r.kOpenTriangleUp]
        ## bin labels for kink and ures summary plots
        self.binLabels = ["", "L1tA", "L1tS", "L2tA", "L2tS", "L3tA", "L3tS",
                          "L4tA", "L4tS", "L5tAh", "L5tSh", "L5tAs", "L5tSs",
                          "L6tAh", "L6tSh", "L6tAs", "L6tSs", "L7tAh", "L7tSh",
                          "L7tAs", "L7tSs", "", "", "", "", "", "L1bA", "L1bS",
                          "L2bA", "L2bS", "L3bA", "L3bS", "L4bA", "L4bS",
                          "L5bAh", "L5bSh", "L5bAs", "L5bSs", "L6bAh",
                          "L6bSh", "L6bAs", "L6bSs", "L7bAh", "L7bSh",
                          "L7bAs", "L7bSs", "", "", "", "", "", "", "", "", "", "", "", ""]

        self.legend_names = []  # legend names
        self.infile_names = []  # input file names
        self.outdir = ""  # output directory
        self.do_HTML = False  # create html page
        self.oFext = ".png"  # extension of output files
        self.config_file = ""  # configuration file
        self.input_files = []  # input TFiles

        self.parse_args()

        for inFile in self.infile_names:
            self.input_files.append(r.TFile(inFile))

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        print("STORING RESULTS IN::", self.outdir)

    def parse_args(self):
        """! Parse command line arguments"""
        parser = ArgumentParser()
        parser.add_argument('-i', '--inputFiles', dest='input_files', help='input files', nargs='*')
        parser.add_argument("-o", "--outdir", dest="outdir", help="output directory", default="AlignmentResults")
        parser.add_argument("-t", "--html", dest="do_HTML", help="create html page", action='store_true')
        parser.add_argument("-l", "--legend", dest="legend", help="names displayed in legend", nargs='*')
        parser.add_argument("-e", "--oFext", dest="oFext", help="extension of output files; default .png", default=".png")
        parser.add_argument("-c", "--config", dest="config", help="configuration file", default="")

        args = parser.parse_args()

        if args.config:
            self.config_file = args.config
            self.read_config()
        else:
            self.infile_names = args.input_files
            self.outdir = args.outdir
            self.legend_names = args.legend
            self.do_HTML = args.do_HTML
            self.oFext = args.oFext

        if self.infile_names == []:
            raise Exception("No input files given")

        if not len(self.legend_names) == len(self.infile_names):
            self.generate_legend()

    def generate_legend(self):
        """! Generate legend names from input file names"""

        print("SETUP:: Generating legend names from input names.")
        for file in self.infile_names:
            pos1 = file.find('HPS')
            pos2 = file.find('iter') + 5

            if pos1 == -1 or pos2 == -1:
                raise Exception("Detector naming pattern deviates from default; the legend names have to be entered manually")

            legName = file[pos1:pos2]
            self.legend_names.append(legName)

    def read_config(self):
        """! Read configuration file"""

        f = open(self.config_file, 'r')
        config = json.load(f)

        if config['inputFiles']:
            self.infile_names = config['inputFiles']
        if config['outdir']:
            self.outdir = config['outdir']
        if config['do_HTML']:
            self.do_HTML = config['do_HTML']
        if config['oFext']:
            self.oFext = config['oFext']
        if config['legend']:
            self.legend_names = config['legend']

    def do_legend(histos, legend_names, location=1, leg_location=[]):
        """! Create legend

        @param histos list of histograms
        @param legend_names list of legend names
        @param location location of the legend
        @param leg_location location of the legend
        """

        if len(legend_names) < len(histos):
            raise Exception("WARNING:: size of legends doesn't match the size of histos")

        legend = None
        xshift = 0.3
        yshift = 0.3
        if (location == 1):
            legend = r.TLegend(0.6, 0.35, 0.90, 0.15)
        if (location == 2):
            legend = r.TLegend(0.40, 0.3, 0.65, 0.2)
        if (location == 3):
            legend = r.TLegend(0.20, 0.90, 0.20+xshift, 0.90-yshift)
        if (location == 4):
            xmin = 0.6
            legend = r.TLegend(xmin, 0.90, xmin+xshift, 0.90-yshift)

        if len(leg_location) == 2:
            legend = r.TLegend(leg_location[0], leg_location[1], leg_location[0]+xshift, leg_location[1]-yshift*0.6)

        return legend

    def set_histo_style(self, histo, ihisto, marker_size=4, line_width=5, label_size=0.05):
        """! Set histo properties

        @param histo histogram
        @param ihisto index of the histogram in list of histos
        @param marker_size marker size
        @param line_width line width
        @param label_size label size
        """
        histo.SetMarkerStyle(self.markers[ihisto])
        histo.SetMarkerColor(self.colors[ihisto])
        histo.SetMarkerSize(marker_size)
        histo.SetLineColor(self.colors[ihisto])
        histo.GetXaxis().SetLabelSize(label_size)
        histo.GetYaxis().SetLabelSize(label_size)
        histo.SetLineWidth(line_width)
