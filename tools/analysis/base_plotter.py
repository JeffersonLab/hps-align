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

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
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

        ## legend names
        self.legend_names = legend_names
        ## input file names
        self.infile_names = infile_names
        ## output directory
        self.outdir = outdir
        ## create html page
        self.do_HTML = do_HTML
        ## extension of output files
        self.oFext = oFext
        ## configuration file
        self.config_file = config_file
        ## input dir in root file
        self.indir = indir

        self.parse_args()

        ## input TFiles
        self.input_files = []
        for inFile in self.infile_names:
            self.input_files.append(r.TFile(inFile))

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        print("STORING RESULTS IN::", self.outdir)

    def parse_args(self):
        """! Parse command line arguments

        Possible arguments:
        - -i, --inputFiles: input files
        - -o, --outdir: output directory
        - -t, --html: create html page
        - -l, --legend: names displayed in legend
        - -e, --oFext: extension of output files; default .png
        - -c, --config: configuration file
        """
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
            self.generate_legend_names()

    def generate_legend_names(self):
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
        """! Read configuration file

        Possible options:
        - inputFiles: input files
        - outdir: output directory
        - do_HTML: create html page
        - oFext: extension of output files; default .png
        - legend: names displayed in legend
        """

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

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """!
        Create legend

        @param histos           list of histograms
        @param legend_names     list of names for legend entries
        @param location         location of the legend
        @param plot_properties  list of properties for legend entries
        @param leg_location     more precise location of the legend overwriting simple location

        @return legend
        """
        if len(legend_names) < len(histos):
            raise Exception("WARNING:: size of legends doesn't match the size of histos")

        leg = None
        xshift = 0.3
        yshift = 0.3
        if (location == 1):
            leg = r.TLegend(0.6, 0.35, 0.90, 0.15)
        if (location == 2):
            leg = r.TLegend(0.40, 0.3, 0.65, 0.2)
        if (location == 3):
            leg = r.TLegend(0.20, 0.90, 0.20+xshift, 0.90-yshift)
        if (location == 4):
            xmin = 0.6
            leg = r.TLegend(xmin, 0.90, xmin+xshift, 0.90-yshift)

        if len(leg_location) == 2:
            leg = r.TLegend(leg_location[0], leg_location[1], leg_location[0]+xshift, leg_location[1]-yshift*0.6)
        for ihist in range(len(histos)):
            if (len(plot_properties) != len(histos)):
                leg.AddEntry(histos[ihist], legend_names[ihist], 'lpf')
            else:
                # splitline{The Data }{slope something }
                entry = "#splitline{" + legend_names[ihist] + "}{" + plot_properties[ihist] + "}"
                leg.AddEntry(histos[ihist], entry, 'lpf')
        leg.SetBorderSize(0)

        return leg

    def set_histo_style(self, histo, ihisto, marker_size=4, line_width=5, label_size=0.05):
        """!
        Set histo properties.

        @param histo        histogram
        @param ihisto       index of the histogram in list of histos
        @param marker_size  marker size
        @param line_width   line width
        @param label_size   label size
        """
        histo.SetMarkerStyle(self.markers[ihisto])
        histo.SetMarkerColor(self.colors[ihisto])
        histo.SetMarkerSize(marker_size)
        histo.SetLineColor(self.colors[ihisto])
        histo.GetXaxis().SetLabelSize(label_size)
        histo.GetYaxis().SetLabelSize(label_size)
        histo.SetLineWidth(line_width)

    def make_2D_plots(self, histolist, out_name="output", xtitle="", ytitle="", ztitle="", zrange=[]):
        """!
        Make combined 2D scatter plots from histograms in histolist

        @param histolist  list of histograms to plot
        @param out_name   name of output file
        @param xtitle     x axis title
        @param ytitle     y axis title
        @param ztitle     z axis title
        @param zrange     z axis range
        """
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

        can = r.TCanvas("c1", "c1", 2200, 2000)

        for ih in range(0, len(histolist)):
            histolist[ih].SetMarkerColor(self.colors[ih])
            histolist[ih].SetLineColor(self.colors[ih])

            if len(zrange) == 2:
                histolist[ih].GetZaxis().SetRangeUser(zrange[0], zrange[1])
            if ztitle != "":
                histolist[ih].GetZaxis().SetTitle(ztitle)

            if (ih == 0):
                title_size = histolist[ih].GetXaxis().GetTitleSize()*0.7
                title_offset = histolist[ih].GetXaxis().GetTitleOffset()
                label_size = histolist[ih].GetXaxis().GetLabelSize()*0.75

                histolist[ih].GetXaxis().SetTitle(xtitle)
                histolist[ih].GetXaxis().SetTitleSize(title_size)
                histolist[ih].GetXaxis().SetTitleOffset(title_offset*0.8)
                histolist[ih].GetXaxis().SetLabelSize(label_size)

                histolist[ih].GetYaxis().SetTitle(ytitle)
                histolist[ih].GetYaxis().SetTitleSize(title_size)
                histolist[ih].GetYaxis().SetTitleOffset(title_offset*1.7)
                histolist[ih].GetYaxis().SetLabelSize(label_size)

                histolist[ih].Draw()

            else:
                histolist[ih].Draw("same")

        leg = self.do_legend(histolist, self.legend_names, 3)

        if (leg is not None):
            leg.Draw()

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.16, 0.89, '#bf{#it{HPS}} Work In Progress')

        can.SaveAs(self.outdir + "/" + out_name + self.oFext)
