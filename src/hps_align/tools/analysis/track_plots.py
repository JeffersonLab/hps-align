import os
import ROOT as r
from .base_plotter import BasePlotter
from .index_page import htmlWriter

r.gROOT.SetBatch(1)


class TrackPlots(BasePlotter):
    """! Class for plotting track plots"""

    def __init__(self, **kwargs) :
        super().__init__(**kwargs)

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

                    self.make_1D_plots(histos, out_name=var+vol+crg, xtitle=var + " " + vol + " " + corrcrg, RebinFactor=1, yrange=[0, 0.05])

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
