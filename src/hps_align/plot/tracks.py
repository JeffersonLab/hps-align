import os
from ._plotter import Plotter, plotter
from .index_page import htmlWriter

@plotter()
def tracks(p : Plotter) :
    """
    """
    if not os.path.exists(p.outdir + "/TrackPlots"):
        os.makedirs(p.outdir + "/TrackPlots")

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
                histos = [f.Get(hname) for f in p.input_files]
                p.make_1D_plots(histos, 
                    out_name='TrackPlots/'+var+vol+crg, 
                    xtitle=var + " " + vol + " " + corrcrg, 
                    RebinFactor=1, yrange=[0, 0.05])

    if p.do_HTML:
        img_type = self.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()
