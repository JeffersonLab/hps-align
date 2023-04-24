import os
import ROOT as r
from .base_plotter import BasePlotter
from .index_page import htmlWriter


class DerivativePlots(BasePlotter):
    """!
    Class for plotting derivative plots

    The input root files must contain the gbl_derivatives directory.
    """

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
        super().__init__(legend_names=legend_names, infile_names=infile_names, outdir=outdir, do_HTML=do_HTML, oFext=oFext, config_file=config_file, indir=indir)
        ## add /derivatives/ to output directory
        self.outdir = self.outdir + "/derivatives/"

    def plot_derivatives(self, name):
        """!
        Plot the derivatives

        The input root files must contain the gbl_derivatives directory.

        @param name  name of the derivative plot
        """

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_derivatives/" + name))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        titleName = name
        maximum = -1.

        for histo in histos:
            print(type(histo))
            if abs(histo.Integral()) > 1e-8:
                histo.Scale(1./histo.Integral())

            # Get the maximum
            if (histo.GetMaximum() > maximum):
                maximum = histo.GetMaximum()

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto)

            if (ihisto == 0):
                histos[ihisto].GetXaxis().SetTitle(titleName + " global derivative")
                histos[ihisto].GetXaxis().SetTitleSize(0.05)
                histos[ihisto].GetXaxis().SetTitleOffset(0.9)
                histos[ihisto].SetMaximum(maximum*1.5)
                histos[ihisto].Draw("P")

                if "223" in name or "123" in name:
                    if int(name[-2:]) < 4:
                        histos[ihisto].GetXaxis().SetRangeUser(-25, 25)
                    else:
                        histos[ihisto].GetXaxis().SetRangeUser(-100, 100)
                else:
                    histos[ihisto].GetXaxis().SetRangeUser(-5, 5)
            else:
                histos[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 3)

        if (leg is not None):
            leg.Draw()

        canv.SaveAs(self.outdir + "/" + name + self.oFext)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
