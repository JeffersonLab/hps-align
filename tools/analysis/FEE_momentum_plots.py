import ROOT as r
from alignment_utils import *
from base_plotter import BasePlotter
from index_page import htmlWriter


class FeeMomentumPlots(BasePlotter):
    """! Plot the FEE momentum plots"""

    def __init__(self):
        super().__init__()

    def plot_histos(self, histopath, do_fit=True, xtitle="", ytitle="", scale_histos=False):

        c = r.TCanvas("c", "c", 2400, 2000)

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

            if do_fit:
                fitList.append(make_fit(histos[ihisto], "singleGausIterative", color=self.colors[ihisto]))

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

        leg = self.do_legend(histos, self.legend_names, 3, plotProperties)
                            #  , legLocation=[0.6, 0.80]) ## \todo: FIXME add this to do_legend

        leg.Draw("same")

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.62, 0.82, '#bf{#it{HPS}} Work In Progress')

        saveName = self.outdir + "/" + histopath.split("/")[-1] + self.oFext

        c.SaveAs(saveName)

        if self.do_HTML:
            hw = htmlWriter(self.outdir)
            hw.add_images(self.outdir)
            hw.close_html()

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
