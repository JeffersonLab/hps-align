"""Plotter object which is passed into plotting functions"""


import json
import os
import ROOT as r


class Plotter:
    """class for plotting alignment results

    This class contains the basic functionality and setup for plotting alignment results.
    It is intended to be inherited by other classes that implement specific plotting.

    The class is initialized with the following arguments:
    - input_file_list: list of file names containing the alignment results
    - outdir: directory where the plots will be saved
    - legend_names: list of names for the legend entries
    - do_html: if True, an index page with links to the plots will be created
    - oFext: extension of the output files

    This class holds the open TFiles and is then passed to future plotting functions
    in order to provide access to the histograms within the files being held.

    Parameters
    ----------
    legend_names : List[str]
        list of legend names aligned with the input files
    infile_names : List[str]
        list of ROOT files to open
    outdir : str
        path to output directory to dump plots
    do_HTML : bool
        whether to write html file or not
    oFext : str
        extension to use for writing plots ('.png' or '.pdf')
    indir : str
        directory inside ROOT files to access plots from
    """

    def __init__(self,
                 legend_names=[],
                 infile_names=[],
                 outdir="",
                 do_HTML=False,
                 oFext=".png",
                 indir="",
                 ):
        # ROOT plot colors
        self.colors = [r.kBlue+2, r.kCyan+2, r.kRed+2, r.kOrange+10,
                       r.kYellow+2, r.kGreen-1, r.kAzure-2, r.kGreen-8,
                       r.kOrange+3, r.kYellow+2, r.kRed+2, r.kBlue+2,
                       r.kGreen-8, r.kOrange+3, r.kYellow+2, r.kRed+2,
                       r.kBlue+2, r.kGreen-8, r.kOrange+3, r.kYellow+2,
                       r.kRed+2, r.kBlue+2, r.kGreen-8, r.kOrange+3,
                       r.kYellow+2, r.kRed+2, r.kBlue+2, r.kGreen-8,
                       r.kOrange+3]
        # ROOT markers
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
        # bin labels for kink and ures summary plots
        self.binLabels = ["", "L1tA", "L1tS", "L2tA", "L2tS", "L3tA", "L3tS",
                          "L4tA", "L4tS", "L5tAh", "L5tSh", "L5tAs", "L5tSs",
                          "L6tAh", "L6tSh", "L6tAs", "L6tSs", "L7tAh", "L7tSh",
                          "L7tAs", "L7tSs", "", "", "", "", "", "L1bA", "L1bS",
                          "L2bA", "L2bS", "L3bA", "L3bS", "L4bA", "L4bS",
                          "L5bAh", "L5bSh", "L5bAs", "L5bSs", "L6bAh",
                          "L6bSh", "L6bAs", "L6bSs", "L7bAh", "L7bSh",
                          "L7bAs", "L7bSs", "", "", "", "", "", "", "", "", "", "", "", ""]

        # legend names
        self.legend_names = legend_names
        # input file names
        self.infile_names = infile_names
        # output directory
        self.outdir = outdir
        # create html page
        self.do_HTML = do_HTML
        # extension of output files
        self.oFext = oFext
        # internal directory histograms are in
        self.indir = indir

        # input TFiles
        self.input_files = []
        for inFile in self.infile_names:
            self.input_files.append(r.TFile(inFile))

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        print("STORING RESULTS IN::", self.outdir)

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
            raise Exception(
                "WARNING:: size of legends doesn't match the size of histos")

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
            leg = r.TLegend(leg_location[0], leg_location[1],
                            leg_location[0]+xshift, leg_location[1]-yshift*0.6)
        for ihist in range(len(histos)):
            if (len(plot_properties) != len(histos)):
                leg.AddEntry(histos[ihist], legend_names[ihist], 'lpf')
            else:
                # splitline{The Data }{slope something }
                entry = "#splitline{" + \
                    legend_names[ihist] + "}{" + plot_properties[ihist] + "}"
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

    def make_1D_plots(self, histolist, out_name="output", xtitle="", ytitle="", yrange=[], logy=False, RebinFactor=0):
        """!
        Make 1D plots

        @param histolist    List of histograms to plot
        @param out_name     Name of the plot
        @param xtitle       X-axis title
        @param ytitle       Y-axis title
        @param yrange       Y-axis range
        @param logy         Set the Y-axis to log scale
        @param RebinFactor  Rebin factor
        """
        can = r.TCanvas("c1", "c1", 2200, 2000)
        if logy:
            can.SetLogy(1)

        means = []
        meansErr = []

        for ih in range(len(histolist)):
            means.append(histolist[ih].GetMean(2))
            meansErr.append(histolist[ih].GetMeanError(2))

            self.set_histo_style(histolist[ih], ih)
            if len(yrange) == 2:
                histolist[ih].GetYaxis().SetRangeUser(yrange[0], yrange[1])
            histolist[ih].GetXaxis().CenterTitle()
            histolist[ih].GetYaxis().CenterTitle()

            if ("pT" in out_name or "pt" in out_name):
                histolist[ih].GetXaxis().SetRangeUser(1., 20.)
            if RebinFactor > 0:
                histolist[ih].Rebin(RebinFactor)

            if ih == 0:
                histolist[ih].Draw()
                if xtitle:
                    histolist[ih].GetXaxis().SetTitle(xtitle)
                if ytitle:
                    histolist[ih].GetYaxis().SetTitle(ytitle)
            else:
                histolist[ih].Draw("same")

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.52, 0.87, '#bf{#it{HPS} Work In Progress}')

        leg = self.do_legend(histolist, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()

        can.SaveAs(self.outdir + out_name + self.oFext)


def plotter():
    """decorator for registering plotters

    This is the wackiest python thing in this package and is
    used to allow the CLI to have a list of all plotters in
    submodules. In order for this to function, a plotting function
    needs...

    1. to be in a module imported in __init__.py. This is required
       so that the function is imported when the parent module is
       imported
    2. to be decorated by the 'plotter' decorator below.

    Examples
    --------
    Register a plotter

        @plotter
        def my_hist_plotter(d) :
            # d will be a Plotter object

    Attributes
    ----------
    __registry__ : dict
        Dictionary of registered plotters
    """
    def plotter_decorator(func):
        func_name = func.__module__.replace('hps_align.plot.', '')+'.'+func.__name__
        plotter.__registry__[func_name] = func
        return func
    return plotter_decorator


plotter.__registry__ = dict()
