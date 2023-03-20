import utilities as utils
import ROOT as r
import os
from base_plotter import BasePlotter

r.gROOT.SetBatch(1)


class TrackPlots(BasePlotter):

    def __init__(self):
        super().__init__()

    def plot_histos(self):
        if not os.path.exists(self.outdir+"/TrackPlots"):
            os.makedirs(self.outdir+"/TrackPlots")

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
                    hname = plotFolder+var+vol+crg

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

                    utils.Make1Dplots(var+vol+crg, self.outdir, histos, self.colors, self.markers, self.legend_names, self.oFext, xtitle=var+" "+vol+" "+corrcrg, ytitle="tracks", RebinFactor=1, ymax=0.05)
