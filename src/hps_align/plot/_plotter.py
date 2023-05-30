"""Plotter object which is passed into plotting functions"""


import json
import os
import ROOT as r

from . import alignment_utils
from .index_page import htmlWriter


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


    Attributes
    ----------
    __registry__ : dict
        Dictionary of registered plotters
    colors : List[int]
        list of ROOT colors to iterate through as we plot
    markers : List[int]
        list of ROOT markers to iterate through as we plot
        in parallel with colors
    binLabels : List[str]
        list of bin labels for kink and ures summary plots
    input_files : List[TFile]
        list of ROOT files we are going to pull histograms from
    """

    def __init__(self,
                 legend_names=[],
                 infile_names=[],
                 outdir="",
                 do_HTML=False,
                 oFext=".png",
                 is2016=False,
                 plot_list_file=None):
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

        self.legend_names = legend_names
        self.infile_names = infile_names
        self.outdir = outdir
        self.do_HTML = do_HTML
        self.oFext = oFext
        self.is2016 = is2016

        # input TFiles
        self.input_files = [r.TFile(inf) for inf in self.infile_names]

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        with open(plot_list_file) as plf:
            self._plot_list = json.load(plf)

        alignment_utils.set_style()
        print("STORING RESULTS IN::", self.outdir)

    def plot_list(self, name=None):
        """Get the plot listing

        If a name is not provided, the full plot listing is returned.
        If a name is provided, only that category of plots is returned
        and if that category of plots is separated by year, we only
        return the group of plots from that category for the configured
        year.

        Parameter
        ---------
        name : str, optional
            optional name of plot category to pull

        Returns
        -------
        dict
            plot listing
        """
        if name is None:
            # provide whole plot list
            return self._plot_list
        elif name not in self._plot_list:
            raise ValueError(
                f'{name} not a category in plot listing.')
        elif '2016' in self._plot_list[name]:
            # provide currently-configured year of that category
            year = '2016' if self.is2016 else 'not2016'
            return self._plot_list[name][year]
        else:
            # year-separation not available
            return self._plot_list[name]

    def get(self, hist_name, indir=""):
        """Get a histogram from each ROOT file

        Parameters
        ----------
        hist_name : str
            name of histogram to get
        indir : str, optional
            optional ROOT directory histogram is contained in

        Returns
        -------
        List[TH1]
            list of histograms, one from each file

        Raises
        ------
        KeyError
            if hist_name is not found in any of the files
        """

        # deduce full in-file path to histogram
        path = indir + '/' + hist_name

        # do not use list expansion since we want to handle errors
        histos = []
        for f in self.input_files:
            h = f.Get(path)
            if h is None or not isinstance(h, r.TH1):
                raise KeyError(f'Histogram {path} not found in {f.GetName()}')
            histos.append(h)

        return histos

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """Create legend

        Parameters
        ----------
        histos : List[TH1]
            of histograms to do legend for
        legend_names : List[str]
            names for the histograms in the legend
        location : int
            location short ID
        plot_properties : List[str]
            list of properties to include along with legend entries
        leg_location : List[float]
            more precise legend location, overwriting predefined one

        Returns
        -------
        TLegend :
            created TLegend ready to Draw at your convenience
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
        """Set histo properties.

        Parameters
        ----------
        histo : r.TH1
            histogram to style
        ihisto : int
            index of histogram in list of histograms, sets the style
        marker_size : int
            size of marker in ROOT units
        line_width : int
            with of line in ROOT units
        label_size : float
            size of label in ROOT units
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

    def make_1D_plots_with_fit(self, histopath, xtitle="", ytitle="", fit=True, scale_histos=False):
        """Plot the histograms with an iterative gaussian fit

        Parameters
        ----------
        histopath : str
            path to the histogram in the ROOT files
        fit : bool or dict, optional
            do the iterative gaussing fit and plot the result
            if dictionary, use those settings as keyword arguments to make_fit
        xtitle : str
            title of x-axis
        ytitle : str
            title of y-axis
        scale_histos : bool
            scale the histograms to unity

        See Also
        --------
        alignment_utils.make_fit
            for how fitting of histograms is done
        """

        canv = r.TCanvas("c", "c", 2200, 2000)

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get(histopath))

        fitList = []
        plotProperties = []

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto, line_width=3)

            # Scale the histogram to unity
            if scale_histos:
                histos[ihisto].Scale(1./histos[ihisto].Integral())
            histos[ihisto].SetLineWidth(3)

            if fit or isinstance(fit, dict):
                fitting_kwargs = dict(
                    color=self.colors[ihisto]
                )
                if isinstance(fit, dict):
                    for k, v in fit.items():
                        fitting_kwargs[k] = v
                fitList.append(alignment_utils.make_fit(
                    histos[ihisto], "singleGausIterative",
                    **fitting_kwargs
                ))

            if (ihisto == 0):
                histos[ihisto].Draw("h")
                histos[ihisto].GetXaxis().SetTitle(xtitle)
                histos[ihisto].GetXaxis().SetTitleSize(0.05)
                histos[ihisto].GetXaxis().SetTitleOffset(1.)
                histos[ihisto].GetXaxis().SetLabelSize(0.06)

                histos[ihisto].GetYaxis().SetTitle(ytitle)
                histos[ihisto].GetYaxis().SetLabelSize(0.06)
                histos[ihisto].GetYaxis().SetTitleSize(0.05)
                histos[ihisto].GetYaxis().SetTitleOffset(1.4)

            else:
                histos[ihisto].Draw("hsame")

            if len(fitList) > 0:
                fitList[ihisto].Draw("same")
                mu = fitList[ihisto].GetParameter(1)
                mu_err = fitList[ihisto].GetParError(1)
                sigma = fitList[ihisto].GetParameter(2)
                sigma_err = fitList[ihisto].GetParError(2)

                plotProperties.append((" #mu=%.3f" % round(mu, 3)) + ("+/- %.3f" % round(mu_err, 3))
                                      + (" #sigma=%.3f" % round(sigma, 3)) + ("+/- %.3f" % round(sigma_err, 3)))

        leg = self.do_legend(histos, self.legend_names, 3,
                             plotProperties, leg_location=[0.6, 0.80])

        leg.Draw("same")

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.62, 0.82, '#bf{#it{HPS}} Work In Progress')

        saveName = self.outdir + "/" + histopath.split("/")[-1] + self.oFext

        canv.SaveAs(saveName)

    def plot_profileY(self, name,
                      indir='res/',
                      xtitle="hit position [mm]",
                      ytitle="<ures> [mm]",
                      rangeX=[], rangeY=[], do_fit=False,
                      fitrange=[-2e5, 2e5], fit="[0]*x + [1]",
                      num_bins=1, rebin=1, do_sigma_profile=False):
        """!
        Plot y profile of distribution

        @param name              name of the histogram
        @param xtitle            x axis title
        @param ytitle            y axis title
        @param rangeX            x axis range
        @param rangeY            y axis range
        @param do_fit            if true, fit is performed
        @param fitrange          range for fit
        @param fit               fit function
        @param num_bins          number of bins for profile
        @param rebin             rebinning factor
        @param do_sigma_profile  if true, sigma profile plots are added
        """

        histos = []
        histos_mu = []
        histos_sigma = []

        for infile in self.input_files:
            if not infile.Get(indir+name):
                raise Exception(indir + name + "   NOT FOUND")

            histos.append(infile.Get(indir+name))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        plotProperties = []

        for ihisto in range(0, len(histos)):
            histos[ihisto].Rebin(rebin)

            histos_mu.append(r.TH1F(histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetName() + "_mu" + str(
                ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            histos_sigma.append(r.TH1F(histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetName() + "_sigma" + str(
                ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            alignment_utils.profile_y_with_iterative_gauss_fit(
                histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], num_bins, fitrange=fitrange)

            self.set_histo_style(histos_mu[ihisto], ihisto)

            hist = histos_mu[ihisto]
            hmin = hist.GetBinLowEdge(1)
            hmax = (hist.GetBinLowEdge(hist.GetNbinsX())) + \
                hist.GetBinWidth(hist.GetNbinsX())

            fitPars = []

            if do_fit:
                fitF = r.TF1("fit" + str(ihisto), fit, hmin, hmax)
                string = ""
                for i in range(fitF.GetNpar()):
                    fitPars.append(fitF.GetParameter(i))
                    string += str(round(fitPars[i], 4)) + ","
                plotProperties.append(string)

            histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")

            if (ihisto == 0):
                histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
                histos_mu[ihisto].GetYaxis().SetTitle(ytitle)
                histos_mu[ihisto].GetYaxis().SetTitleSize(
                    histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos_mu[ihisto].GetYaxis().SetTitleOffset(
                    histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

                histos_mu[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
                if len(rangeY) > 1:
                    histos_mu[ihisto].GetYaxis().SetRangeUser(
                        rangeY[0], rangeY[1])
                histos_mu[ihisto].Draw("P")
                if len(rangeX) > 1:
                    histos_mu[ihisto].GetXaxis().SetRangeUser(
                        rangeX[0], rangeX[1])
            else:
                histos_mu[ihisto].Draw("P SAME")

            if do_fit:
                fitF.SetLineColor(self.colors[ihisto])
                fitF.Draw("SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2, plotProperties)

        if (leg is not None):
            leg.Draw()

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.66, 0.89, '#bf{#it{HPS}} Work In Progress')

        canv.SaveAs(self.outdir + "/" + name + "_profiled" + self.oFext)

        if do_sigma_profile:
            canv_sigma = r.TCanvas("c1", "c1", 2200, 2000)
            canv_sigma.SetGridx()
            canv_sigma.SetGridy()
            canv_sigma.cd()

            for ihisto in range(0, len(histos_sigma)):
                self.set_histo_style(histos_sigma[ihisto], ihisto)
                if (ihisto == 0):
                    histos_sigma[ihisto].GetXaxis().SetTitle(xtitle)
                    histos_sigma[ihisto].GetYaxis().SetTitle(ytitle)
                    histos_sigma[ihisto].GetYaxis().SetTitleSize(
                        histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                    histos_sigma[ihisto].GetYaxis().SetTitleOffset(
                        histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                    histos_sigma[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
                    if len(rangeY) > 1:
                        histos_sigma[ihisto].GetYaxis().SetRangeUser(
                            rangeY[0], rangeY[1])
                    histos_sigma[ihisto].Draw("P")
                    if len(rangeX) > 1:
                        histos_sigma[ihisto].GetXaxis().SetRangeUser(
                            rangeX[0], rangeX[1])
                else:
                    histos_sigma[ihisto].Draw("P SAME")

            leg = self.do_legend(
                histos_sigma, self.legend_names, 2, plotProperties)

            if (leg is not None):
                leg.Draw()

            canv_sigma.SaveAs(self.outdir + "/" + name +
                              "_sigma_profiled" + self.oFext)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()

    __registry__ = dict()

    def user(func):
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
        Register a plotter::

            @Plotter.user
            def my_hist_plotter(d) :
                # d will be a Plotter object
        """
        if func.__module__ == 'hps_align.plot':
            func_name = func.__name__
        else:
            func_name = func.__module__.replace('hps_align.plot.', '')+'.'+func.__name__
        Plotter.__registry__[func_name] = func
        return func
