import os
import ROOT as r
from tools.analysis.base_plotter import BasePlotter
from tools.analysis.index_page import htmlWriter

r.gROOT.SetBatch(1)


class TrackPlots(BasePlotter):
    """! Class for plotting track plots"""

    def __init__(self):
        super().__init__()

    def plot_histos(self):
        """! Plot the track histograms

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

                    self.Make1Dplots(var + vol + crg, histos, xtitle=var + " " + vol + " " + corrcrg, RebinFactor=1, ymax=0.05)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()

    def Make1Dplots(self, name, histos, xtitle="", ytitle="", ymin=0, ymax=1, RebinFactor=0, LogY=False):

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

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """! Create legend

        @param histos  list of histograms
        @param legend_names  list of names for legend entries
        @param location  location of the legend
        @param plot_properties  list of properties for legend entries
        @param leg_location  more precise location of the legend overwriting simple location

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
