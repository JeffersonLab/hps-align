import os
import ROOT as r
from tools.analysis.base_plotter import BasePlotter
from tools.analysis.index_page import htmlWriter


class DerivativePlots(BasePlotter):
    """! Class for plotting derivative plots

    The input root files must contain the gbl_derivatives directory.
    """

    def __init__(self):
        super().__init__()
        self.outdir = self.outdir + "/derivatives/"  ## add /derivatives/ to output directory

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """! Create legend

        @param histos list of histograms
        @param legend_names list of names for legend entries
        @param location location of the legend
        @param plot_properties list of properties for legend entries
        @param leg_location more precise location of the legend overwriting simple location

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

    def plot_derivatives(self, name):
        """! Plot the derivatives

        The input root files must contain the gbl_derivatives directory.

        @param name name of the derivative plot
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
