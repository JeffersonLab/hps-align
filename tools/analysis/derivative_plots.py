from base_plotter import BasePlotter
import ROOT as r
import alignment_utils as alignUtils
import os
from index_page import htmlWriter


class DerivativePlots(BasePlotter):

    def __init__(self):
        super().__init__()
        self.outdir = self.outdir + "/derivatives/"

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """! Create legend"""
        # leg = super().do_legend(histos, legend_names, location, leg_location)
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
        for l in range(len(histos)):
            if (len(plot_properties) != len(histos)):
                leg.AddEntry(histos[l], legend_names[l], 'lpf')
            else:
                # splitline{The Data }{slope something }
                entry = "#splitline{" + legend_names[l] + "}{" + plot_properties[l] + "}"
                leg.AddEntry(histos[l], entry, 'lpf')
        leg.SetBorderSize(0)

        return leg

    def plot_derivatives(self, name):

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_derivatives/" + name))

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

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

        c.SaveAs(self.outdir + "/" + name + self.oFext)

        if self.do_HTML:
            hw = htmlWriter(self.outdir)
            hw.add_images(self.outdir)
            hw.close_html()
