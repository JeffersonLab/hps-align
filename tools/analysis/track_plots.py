import os
import ROOT as r
from tools.analysis.base_plotter import BasePlotter
from tools.analysis.index_page import htmlWriter

r.gROOT.SetBatch(1)


class TrackPlots(BasePlotter):
    """! Class for plotting track plots"""

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
        super().__init__(legend_names=legend_names, infile_names=infile_names, outdir=outdir, do_HTML=do_HTML, oFext=oFext, config_file=config_file, indir=indir)

    def plot_histos(self):
        """!
        Plot the track histograms

        The input root files must contain the trk_params directory.
        """
        if not os.path.exists(self.outdir + "/TrackPlots"):
            os.makedirs(self.outdir + "/TrackPlots")

        inputFiles = []

        for ifile in self.infile_names:
            print("Loading ... ", ifile)
            inf = r.TFile(ifile)
            inputFiles.append(inf)

        plotFolder = "trk_params/"
        charges = ["", "_neg", "_pos"]
        vols = ["_top", "_bottom"]
        variables = ["Chi2",
                     "nHits",
                     "phi",
                     "tanLambda",
                     #  "trk_extr_bs_x",
                     #  "trk_extr_bs_y",
                     #  "trk_extr_bs_x_rk",
                     #  "trk_extr_bs_y_rk",
                     #  "d0",
                     #  "z0",
                     "p"]

        for crg in charges:
            for vol in vols:
                for var in variables:
                    hname = plotFolder + var + vol + crg

                    if ("pos" in crg):
                        corrcrg = "q-"
                    elif ("neg" in crg):
                        corrcrg = "q+"
                    else:
                        corrcrg = "All"

                    # File loop
                    histos = []
                    for i_f in range(len(inputFiles)):
                        histo_u = inputFiles[i_f].Get(hname)
                        histos.append(histo_u)

                    self.make_1D_plots(var + vol + crg, histos, xtitle=var + " " + vol + " " + corrcrg, RebinFactor=1, ymax=0.05)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()

    def make_1D_plots(self, name, histos, xtitle="", ytitle="", ymin=0, ymax=1, RebinFactor=0, LogY=False):
        """! Make 1D plots

        @param name         Name of the plot
        @param histos       List of histograms to plot
        @param xtitle       X-axis title
        @param ytitle       Y-axis title
        @param ymin         Minimum value of the Y-axis
        @param ymax         Maximum value of the Y-axis
        @param RebinFactor  Rebin factor
        @param LogY         Set the Y-axis to log scale
        """
        can = r.TCanvas(name, name, 2200, 2000)
        if LogY:
            can.SetLogy(1)

        means = []
        meansErr = []

        for ih in range(len(histos)):
            means.append(histos[ih].GetMean(2))
            meansErr.append(histos[ih].GetMeanError(2))

            self.set_histo_style(histos[ih], ih)
            histos[ih].GetYaxis().SetRangeUser(ymin, ymax)
            histos[ih].GetXaxis().CenterTitle()
            histos[ih].GetYaxis().CenterTitle()

            if ("pT" in name or "pt" in name):
                histos[ih].GetXaxis().SetRangeUser(1., 20.)
            if RebinFactor > 0:
                histos[ih].Rebin(RebinFactor)

            if ih == 0:
                histos[ih].Draw()
                if xtitle:
                    histos[ih].GetXaxis().SetTitle(xtitle)
                if ytitle:
                    histos[ih].GetYaxis().SetTitle(ytitle)
            else:
                histos[ih].Draw("same")

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.52, 0.87, '#bf{#it{HPS} Work In Progress}')

        leg = self.do_legend(histos, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()

        can.SaveAs(self.outdir + "/TrackPlots/" + name + self.oFext)
